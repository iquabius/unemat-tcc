import { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  DURACAO_DA_SESSAO,
  MENSAGENS,
  autenticar,
  ignorarCancelamento,
  iniciarRelogio,
  podeEntrar,
  tempoDeSessao,
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

type Situacao = keyof typeof MENSAGENS;

function PainelDeLogin() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [situacao, setSituacao] = useState<Situacao>("desconectado");
  const [segundos, setSegundos] = useState(0);
  const controlador = useRef<AbortController | null>(null);

  // O relógio vive enquanto a situação for "conectado": qualquer outra
  // situação, inclusive uma tentativa nova, e a saída da página o param
  // pela limpeza.
  useEffect(() => {
    if (situacao !== "conectado") return;
    let decorridos = 0;
    return iniciarRelogio(() => {
      decorridos += 1;
      if (decorridos >= DURACAO_DA_SESSAO) setSituacao("desconectado");
      else setSegundos(decorridos);
    });
  }, [situacao]);

  // Sem isto, a tentativa continua fora da página.
  useEffect(() => () => controlador.current?.abort(), []);

  function tentar() {
    controlador.current?.abort();
    const atual = new AbortController();
    controlador.current = atual;
    // Zera aqui, e não no efeito, que roda depois da pintura: a sessão nova
    // mostraria por um quadro o tempo da anterior.
    setSegundos(0);
    setSituacao("conectando");
    autenticar(nome, senha, atual.signal).then(
      (valida) => setSituacao(valida ? "conectado" : "falha"),
      ignorarCancelamento,
    );
  }

  return (
    <section className="painel">
      <label>
        Nome{" "}
        <input
          name="nome"
          autoComplete="username"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
      </label>
      <label>
        Senha{" "}
        <input
          name="senha"
          type="password"
          autoComplete="current-password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
      </label>
      <button
        type="button"
        className="entrar"
        disabled={!podeEntrar(nome, senha)}
        onClick={tentar}
      >
        Entrar
      </button>
      <p className="situacao" role="status">
        {MENSAGENS[situacao]}
      </p>
      {situacao === "conectado" && (
        <>
          <p className="relogio">{tempoDeSessao(segundos)}</p>
          <button
            type="button"
            className="sair"
            onClick={() => setSituacao("desconectado")}
          >
            Sair
          </button>
        </>
      )}
    </section>
  );
}

hospedar((conteiner) => {
  const raiz = createRoot(conteiner);
  raiz.render(<PainelDeLogin />);
  return () => raiz.unmount();
});
