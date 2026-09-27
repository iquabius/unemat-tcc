import { Component, computed, signal } from '@angular/core';
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

@Component({
  selector: 'app-formulario',
  template: `
    <form class="formulario" novalidate (submit)="reservar($event)">
      <label>
        Nome do passageiro
        <input
          name="nome"
          autocomplete="name"
          [value]="nome()"
          [aria-invalid]="!!erroVisivel.nome()"
          (input)="nome.set($event.target.value)"
          (blur)="tocar('nome')"
        />
      </label>
      @if (erroVisivel.nome(); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        E-mail
        <input
          name="email"
          type="email"
          autocomplete="email"
          [value]="email()"
          [aria-invalid]="!!erroVisivel.email()"
          (input)="email.set($event.target.value)"
          (blur)="tocar('email')"
        />
      </label>
      @if (erroVisivel.email(); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        Tipo de voo
        <select name="tipo" [value]="tipo()" (change)="tipo.set($any($event.target).value)">
          <option value="ida">Só ida</option>
          <option value="ida-e-volta">Ida e volta</option>
        </select>
      </label>

      <label>
        Data de ida
        <input
          name="ida"
          placeholder="DD/MM/AAAA"
          [value]="ida()"
          [aria-invalid]="!!erroVisivel.ida()"
          (input)="ida.set($event.target.value)"
          (blur)="tocar('ida')"
        />
      </label>
      @if (erroVisivel.ida(); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <label>
        Data de volta
        <input
          name="volta"
          placeholder="DD/MM/AAAA"
          [value]="volta()"
          [disabled]="!idaEVolta()"
          [aria-invalid]="!!erroVisivel.volta()"
          (input)="volta.set($event.target.value)"
          (blur)="tocar('volta')"
        />
      </label>
      @if (erroVisivel.volta(); as erro) {
        <p class="erro">{{ erro }}</p>
      }

      <button type="submit" [disabled]="temErro()">Reservar</button>
    </form>
    <p class="confirmacao" role="status">{{ confirmacao() }}</p>
  `,
})
export class FormularioDeReserva {
  protected readonly nome = signal('');
  protected readonly email = signal('');
  protected readonly tipo = signal<TipoDeVoo>('ida');
  protected readonly ida = signal(hoje());
  protected readonly volta = signal(hoje());
  private readonly tocados = signal<ReadonlySet<Campo>>(new Set());
  protected readonly confirmacao = signal('');

  // Cada erro é um valor derivado: recalcula só quando os sinais que ele lê
  // mudam, e atualiza só os pontos da tela que o leem.
  protected idaEVolta() {
    return this.tipo() === 'ida-e-volta';
  }
  private readonly erroNome = computed(() => erroDoNome(this.nome()));
  private readonly erroEmail = computed(() => erroDoEmail(this.email()));
  private readonly erroIda = computed(() => erroDaData(this.ida()));
  private readonly erroVolta = computed(() => (this.idaEVolta() ? erroDaData(this.volta()) : null));
  private readonly erroOrdem = computed(() =>
    this.idaEVolta() ? erroDaOrdem(this.ida(), this.volta()) : null,
  );
  protected readonly temErro = computed(() =>
    [this.erroNome(), this.erroEmail(), this.erroIda(), this.erroVolta(), this.erroOrdem()].some(
      Boolean,
    ),
  );

  private tocado(campo: Campo) {
    return this.tocados().has(campo);
  }
  protected tocar(campo: Campo) {
    this.tocados.update((anteriores) => new Set(anteriores).add(campo));
  }

  protected readonly erroVisivel: Record<Campo, () => string | null> = {
    nome: () => (this.tocado('nome') ? this.erroNome() : null),
    email: () => (this.tocado('email') ? this.erroEmail() : null),
    ida: () => (this.tocado('ida') ? this.erroIda() : null),
    volta: () =>
      (this.tocado('volta') ? this.erroVolta() : null) ??
      (this.tocado('ida') || this.tocado('volta') ? this.erroOrdem() : null),
  };

  protected reservar(evento: SubmitEvent) {
    evento.preventDefault();
    this.confirmacao.set(
      mensagemDeConfirmacao({
        nome: this.nome(),
        email: this.email(),
        tipo: this.tipo(),
        ida: this.ida(),
        volta: this.volta(),
      }),
    );
  }
}
