import { useEffect, useEffectEvent, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  DIAMETRO_INICIAL,
  DIAMETRO_MAXIMO,
  DIAMETRO_MINIMO,
  MENSAGENS,
  circuloSob,
  desenharCirculos,
  mensagemDeAjustado,
  mensagemDeCriado,
  ouvirAtalhos,
  pontoNoCanvas,
  tituloDoAjuste,
  type Circulo,
  type Ponto,
} from "../../dominio";
import "../../estilo.css";

function AreaDeDesenho() {
  // O estado: a lista de círculos, trocada por uma cópia a cada alteração,
  // porque o setState ignora a mesma referência, e o histórico, uma
  // fotografia da lista a cada passo, com o cursor na de agora (ADR 0040).
  // O ajuste troca a lista sem passo, até o diálogo fechar.
  const [circulos, setCirculos] = useState<readonly Circulo[]>([]);
  const [historico, setHistorico] = useState<(readonly Circulo[])[]>([[]]);
  const [cursor, setCursor] = useState(0);
  const [situacao, setSituacao] = useState("");
  // O controle de diálogo: o índice do círculo escolhido pelo botão
  // direito, que vale da abertura do menu ao fim do ajuste, porque o
  // ponteiro sai do canvas a caminho do item; e o diâmetro com que o
  // diálogo abriu, que a tela não mostra.
  const [ponteiro, setPonteiro] = useState<Ponto>();
  const [escolhido, setEscolhido] = useState<number>();
  const diametroDaAbertura = useRef(0);
  const [posicaoDoMenu, setPosicaoDoMenu] = useState<Ponto>({ x: 0, y: 0 });
  const canvas = useRef<HTMLCanvasElement>(null);
  const menu = useRef<HTMLDivElement>(null);
  const dialogo = useRef<HTMLDialogElement>(null);

  // O selecionado: o escolhido, com o menu ou o diálogo aberto, ou, sem
  // eles, o sob o ponteiro.
  const circuloEscolhido =
    escolhido !== undefined ? circulos[escolhido] : undefined;
  const selecionadoEm = (ponto: Ponto | undefined) =>
    circuloEscolhido ?? circuloSob(circulos, ponto);
  const selecionado = selecionadoEm(ponteiro);

  // O desenho dentro do canvas não se monta em JSX: o efeito o refaz depois
  // de cada renderização em que os círculos ou o selecionado mudaram.
  useEffect(() => {
    desenharCirculos(canvas.current!, circulos, selecionado);
  }, [circulos, selecionado]);

  // Um passo novo descarta os desfeitos.
  function registrarPasso(novos: readonly Circulo[]) {
    setHistorico([...historico.slice(0, cursor + 1), novos]);
    setCursor(cursor + 1);
  }

  function criar(ponto: Ponto) {
    setPonteiro(ponto);
    if (selecionadoEm(ponto) !== undefined) return;
    const novos = [...circulos, { ...ponto, diametro: DIAMETRO_INICIAL }];
    setCirculos(novos);
    registrarPasso(novos);
    setSituacao(mensagemDeCriado(ponto));
  }

  // Com o menu aberto, o botão direito só o fecha, como qualquer clique
  // fora dele.
  function abrirMenu(evento: React.MouseEvent) {
    evento.preventDefault();
    if (escolhido !== undefined) return;
    const ponto = pontoNoCanvas(evento.nativeEvent);
    setPonteiro(ponto);
    const circulo = selecionadoEm(ponto);
    if (circulo === undefined) return;
    setEscolhido(circulos.indexOf(circulo));
    setPosicaoDoMenu({ x: evento.pageX, y: evento.pageY });
    menu.current!.showPopover();
  }

  function abrirAjuste() {
    diametroDaAbertura.current = circuloEscolhido!.diametro;
    dialogo.current!.showModal();
    menu.current!.hidePopover();
  }

  // Sem mutação: o círculo ajustado volta à lista como cópia, no índice
  // guardado (Kiss 2014, p. 46).
  function ajustar(diametro: number) {
    setCirculos(
      circulos.map((circulo, i) =>
        i === escolhido ? { ...circulo, diametro } : circulo,
      ),
    );
  }

  function fecharAjuste() {
    const { diametro } = circuloEscolhido!;
    if (diametro !== diametroDaAbertura.current) {
      registrarPasso(circulos);
      setSituacao(mensagemDeAjustado(diametro));
    }
    setEscolhido(undefined);
  }

  // O passo pode tirar da lista o círculo do menu: desfazer e refazer o
  // fecham antes de agir.
  function fecharMenu() {
    setEscolhido(undefined);
    menu.current!.hidePopover();
  }

  function voltar() {
    if (cursor === 0) return;
    fecharMenu();
    const anterior = cursor - 1;
    setCursor(anterior);
    setCirculos(historico[anterior]);
    setSituacao(MENSAGENS.desfeito);
  }

  function avancar() {
    if (cursor === historico.length - 1) return;
    fecharMenu();
    const seguinte = cursor + 1;
    setCursor(seguinte);
    setCirculos(historico[seguinte]);
    setSituacao(MENSAGENS.refeito);
  }

  // O ouvinte abre uma vez e chama sempre o tratador da última
  // renderização; com o diálogo aberto, o atalho não age: o modal já deixa
  // os botões inertes, mas não o document.
  const aoDesfazer = useEffectEvent(() => {
    if (!dialogo.current!.open) voltar();
  });
  const aoRefazer = useEffectEvent(() => {
    if (!dialogo.current!.open) avancar();
  });
  useEffect(
    () =>
      ouvirAtalhos({
        desfazer: () => aoDesfazer(),
        refazer: () => aoRefazer(),
      }),
    [],
  );

  return (
    <section className="desenho">
      <div className="acoes">
        <button
          type="button"
          className="desfazer"
          disabled={cursor === 0}
          onClick={voltar}
        >
          Desfazer
        </button>
        <button
          type="button"
          className="refazer"
          disabled={cursor === historico.length - 1}
          onClick={avancar}
        >
          Refazer
        </button>
      </div>
      <canvas
        ref={canvas}
        role="img"
        aria-label="Desenho"
        onPointerMove={(e) => setPonteiro(pontoNoCanvas(e.nativeEvent))}
        onPointerLeave={() => setPonteiro(undefined)}
        onClick={(e) => criar(pontoNoCanvas(e.nativeEvent))}
        onContextMenu={abrirMenu}
      />
      <p className="situacao" role="status">
        {situacao}
      </p>
      <div
        ref={menu}
        className="menu"
        popover=""
        style={{ left: posicaoDoMenu.x, top: posicaoDoMenu.y }}
        // O menu fecha também no clique fora e no Esc; sem o ajuste, o
        // círculo escolhido volta a ser o sob o ponteiro.
        onToggle={(e) => {
          if (e.newState === "closed" && !dialogo.current!.open) {
            setEscolhido(undefined);
          }
        }}
      >
        <button type="button" onClick={abrirAjuste}>
          Ajustar o diâmetro…
        </button>
      </div>
      {/* O close vem também do Esc. */}
      <dialog ref={dialogo} className="ajuste" onClose={fecharAjuste}>
        <h2>{circuloEscolhido && tituloDoAjuste(circuloEscolhido)}</h2>
        {/* Com o diálogo fechado, o slider não aparece, e o valor não importa. */}
        <label>
          Diâmetro{" "}
          <input
            type="range"
            min={DIAMETRO_MINIMO}
            max={DIAMETRO_MAXIMO}
            value={circuloEscolhido?.diametro ?? DIAMETRO_INICIAL}
            onChange={(e) => ajustar(Number(e.target.value))}
          />
        </label>
        <button
          type="button"
          className="fechar"
          onClick={() => dialogo.current!.close()}
        >
          Fechar
        </button>
      </dialog>
    </section>
  );
}

// A página: o botão que tira o desenho da página e o põe de volta.
function Pagina() {
  const [visivel, setVisivel] = useState(true);
  return (
    <main className="pagina">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder desenho" : "Mostrar desenho"}
      </button>
      {visivel && <AreaDeDesenho />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<Pagina />);
