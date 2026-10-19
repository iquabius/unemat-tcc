import { Component, DestroyRef, effect, inject, signal } from "@angular/core";
import {
  DURACAO_DA_SESSAO,
  MENSAGENS,
  autenticar,
  ignorarCancelamento,
  iniciarRelogio,
  podeEntrar,
  tempoDeSessao,
} from "../../../dominio";

type Situacao = keyof typeof MENSAGENS;

@Component({
  selector: "app-painel-de-login",
  template: `
    <section class="painel">
      <label>
        Nome
        <input
          name="nome"
          autocomplete="username"
          [value]="nome()"
          (input)="nome.set($event.target.value)"
        />
      </label>
      <label>
        Senha
        <input
          name="senha"
          type="password"
          autocomplete="current-password"
          [value]="senha()"
          (input)="senha.set($event.target.value)"
        />
      </label>
      <button
        type="button"
        class="entrar"
        [disabled]="!podeEntrar(nome(), senha())"
        (click)="tentar()"
      >
        Entrar
      </button>
      <p class="situacao" role="status">{{ MENSAGENS[situacao()] }}</p>
      @if (situacao() === "conectado") {
        <p class="relogio">{{ tempoDeSessao(segundos()) }}</p>
        <button
          type="button"
          class="sair"
          (click)="situacao.set('desconectado')"
        >
          Sair
        </button>
      }
    </section>
  `,
})
export class PainelDeLogin {
  // O template só alcança o que a classe expõe: o domínio entra por aqui.
  protected readonly MENSAGENS = MENSAGENS;
  protected readonly podeEntrar = podeEntrar;
  protected readonly tempoDeSessao = tempoDeSessao;

  protected readonly nome = signal("");
  protected readonly senha = signal("");
  protected readonly situacao = signal<Situacao>("desconectado");
  protected readonly segundos = signal(0);
  private controlador: AbortController | undefined;

  constructor() {
    // O relógio vive enquanto a situação for "conectado": qualquer outra
    // situação, inclusive uma tentativa nova, e a saída da página o param
    // pela limpeza.
    effect((onCleanup) => {
      if (this.situacao() !== "conectado") return;
      this.segundos.set(0);
      let decorridos = 0;
      onCleanup(
        iniciarRelogio(() => {
          decorridos += 1;
          if (decorridos >= DURACAO_DA_SESSAO)
            this.situacao.set("desconectado");
          else this.segundos.set(decorridos);
        }),
      );
    });

    // Sem isto, a tentativa continua fora da página.
    inject(DestroyRef).onDestroy(() => this.controlador?.abort());
  }

  protected tentar() {
    this.controlador?.abort();
    const atual = new AbortController();
    this.controlador = atual;
    this.situacao.set("conectando");
    autenticar(this.nome(), this.senha(), atual.signal).then(
      (valida) => this.situacao.set(valida ? "conectado" : "falha"),
      ignorarCancelamento,
    );
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
@Component({
  selector: "app-login-com-quarentena",
  imports: [PainelDeLogin],
  template: `
    <main class="login">
      <button type="button" class="alternar" (click)="visivel.set(!visivel())">
        {{ visivel() ? "Esconder login" : "Mostrar login" }}
      </button>
      @if (visivel()) {
        <app-painel-de-login />
      }
    </main>
  `,
})
export class LoginComQuarentena {
  protected readonly visivel = signal(true);
}
