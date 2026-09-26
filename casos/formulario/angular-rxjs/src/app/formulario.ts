import { AsyncPipe } from '@angular/common';
import { Component } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
} from '@angular/forms';
import { Subject, map, startWith } from 'rxjs';
import {
  erroDaData,
  erroDaOrdem,
  erroDoEmail,
  erroDoNome,
  hoje,
  mensagemDeConfirmacao,
  type TipoDeVoo,
} from '../../../dominio';

type Campo = 'nome' | 'email' | 'ida' | 'volta';

// Adapta uma regra do domínio (texto → mensagem ou null) a um validador.
function validadorDe(regra: (valor: string) => string | null): ValidatorFn {
  return (controle: AbstractControl): ValidationErrors | null => {
    const mensagem = regra(controle.value);
    return mensagem ? { mensagem } : null;
  };
}

// Validador do grupo: a ordem das datas envolve dois campos.
const ordemDasDatas: ValidatorFn = (grupo: AbstractControl): ValidationErrors | null => {
  const { tipo, ida, volta } = grupo.getRawValue();
  if (tipo !== 'ida-e-volta') return null;
  const ordem = erroDaOrdem(ida, volta);
  return ordem ? { ordem } : null;
};

// RxJS de propósito: valueChanges, statusChanges e um Subject para os
// envios, embora o Angular atual recomende signals.
@Component({
  selector: 'app-formulario',
  imports: [ReactiveFormsModule, AsyncPipe],
  template: `
    <form class="formulario" novalidate [formGroup]="formulario" (ngSubmit)="envios.next()">
      <label>
        Nome do passageiro
        <input formControlName="nome" autocomplete="name"
               [attr.aria-invalid]="!!erroVisivel('nome')" />
      </label>
      @if (erroVisivel('nome'); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        E-mail
        <input formControlName="email" type="email" autocomplete="email"
               [attr.aria-invalid]="!!erroVisivel('email')" />
      </label>
      @if (erroVisivel('email'); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        Tipo de voo
        <select formControlName="tipo">
          <option value="ida">Só ida</option>
          <option value="ida-e-volta">Ida e volta</option>
        </select>
      </label>

      <label>
        Data de ida
        <input formControlName="ida" placeholder="DD/MM/AAAA"
               [attr.aria-invalid]="!!erroVisivel('ida')" />
      </label>
      @if (erroVisivel('ida'); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        Data de volta
        <input formControlName="volta" placeholder="DD/MM/AAAA"
               [attr.aria-invalid]="!!erroVisivel('volta')" />
      </label>
      @if (erroVisivel('volta'); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <button type="submit" [disabled]="invalido$ | async">Reservar</button>
    </form>
    <p class="confirmacao" role="status">{{ confirmacao$ | async }}</p>
  `,
})
export class FormularioDeReserva {
  protected readonly formulario = new FormGroup(
    {
      nome: new FormControl('', { nonNullable: true, validators: validadorDe(erroDoNome) }),
      email: new FormControl('', { nonNullable: true, validators: validadorDe(erroDoEmail) }),
      tipo: new FormControl<TipoDeVoo>('ida', { nonNullable: true }),
      ida: new FormControl(hoje(), { nonNullable: true, validators: validadorDe(erroDaData) }),
      volta: new FormControl(
        { value: hoje(), disabled: true },
        { nonNullable: true, validators: validadorDe(erroDaData) },
      ),
    },
    { validators: ordemDasDatas },
  );

  // Fluxo com o estado de validade do formulário inteiro
  protected readonly invalido$ = this.formulario.statusChanges.pipe(
    startWith(this.formulario.status),
    map((status) => status !== 'VALID'),
  );

  // Fluxo de envios, convertido na mensagem de confirmação
  protected readonly envios = new Subject<void>();
  protected readonly confirmacao$ = this.envios.pipe(
    map(() => mensagemDeConfirmacao(this.formulario.getRawValue())),
  );

  constructor() {
    // Habilita a data de volta só em "ida e volta"
    this.formulario.controls.tipo.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((tipo) => {
        const volta = this.formulario.controls.volta;
        if (tipo === 'ida-e-volta') volta.enable();
        else volta.disable();
      });
  }

  protected erroVisivel(campo: Campo): string | null {
    const { controls, errors } = this.formulario;
    const controle = controls[campo];
    if (controle.disabled) return null;
    const erroDoCampo = controle.touched ? (controle.errors?.['mensagem'] ?? null) : null;
    if (campo !== 'volta') return erroDoCampo;
    const datasTocadas = controls.ida.touched || controls.volta.touched;
    return erroDoCampo ?? (datasTocadas ? (errors?.['ordem'] ?? null) : null);
  }
}
