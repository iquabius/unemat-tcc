// A página que hospeda a interface, comum às quatro tecnologias, como o
// dominio.ts de cada interface (ADRs 0010 e 0043): um roteador de hash
// com duas rotas. Em "#/" a página está sem a interface; em qualquer
// outra, inclusive sem hash, a interface está montada em #raiz. O teste
// de conformidade sai da tela e volta trocando location.hash, e confere
// que o que a interface abriu (requisição, relógio, inscrição, ouvinte)
// fechou com ela.
//
// A implementação traz só o par montar e desmontar, no idioma da
// tecnologia: montar recebe o contêiner e devolve o desmontar.

export type Montar = (conteiner: HTMLElement) => () => void;

export function hospedar(montar: Montar) {
  const conteiner = document.getElementById("raiz")!;
  let desmontar: (() => void) | undefined;
  const rotear = () => {
    const fora = location.hash === "#/";
    if (fora && desmontar) {
      desmontar();
      desmontar = undefined;
    } else if (!fora && !desmontar) {
      desmontar = montar(conteiner);
    }
  };
  addEventListener("hashchange", rotear);
  rotear();
}
