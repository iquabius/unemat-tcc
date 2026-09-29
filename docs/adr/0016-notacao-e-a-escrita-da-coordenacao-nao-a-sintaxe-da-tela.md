# 0016. A notação é a escrita da coordenação, não a sintaxe da tela, e re-renderização e *signals* são duas notações

2026-09-28. Nas Dimensões Cognitivas, a notação é o conjunto de sinais
que o usuário vê e edita, e duas notações com a mesma estrutura que
diferem na execução diferem só no ambiente (Green 1989); por essa letra,
React e Solid, que escrevem a tela no mesmo JSX, seriam uma notação só,
e Solid e Angular com *signals*, que escrevem a tela de formas
diferentes, seriam duas. O trabalho chama de notação a parte do código
que escreve a coordenação entre evento, estado e tela: onde vive o
estado, como se declara um valor derivado, quem atualiza a tela. Por
esse critério ficam as três notações dos ADRs 0011 e 0014, a imperativa
com *callbacks* e duas declarativas, porque o modelo de reatividade
aparece nos sinais: no React o componente inteiro reexecuta a cada
mudança de estado e um valor derivado é uma expressão comum; no Solid o
componente executa uma vez, e o derivado é uma função que lê o *signal*.
Solid e Angular com *signals* escrevem a coordenação com os mesmos
sinais (`signal`, `computed`, leitura por chamada) e diferem só na tela,
a comparação controlada do ADR 0013. A análise só atribui a uma DC uma
diferença entre React e Solid quando aponta o sinal escrito, e não só o
mecanismo, como Green e Petre (1996, p. 22 da pré-publicação) exigem
para as operações mentais difíceis.

Exemplos mínimos, um contador com um valor derivado nas três notações:

```js
// Imperativa com callbacks (jQuery)
let n = 0;
$("#mais").on("click", () => {
  n = n + 1;
  $("#valor").text(n);       // o callback atualiza cada trecho da tela
  $("#dobro").text(n * 2);   // que depende de n; esquecer um é erro
});
```

```tsx
// Declarativa por re-renderização (React)
function Contador() {
  const [n, setN] = useState(0);
  const dobro = n * 2;          // expressão comum
  console.log("executou");      // roda a cada clique: o componente inteiro reexecuta
  return <button onClick={() => setN(n + 1)}>{n} × 2 = {dobro}</button>;
}
```

```tsx
// Reativa fina com signals (Solid)
function Contador() {
  const [n, setN] = createSignal(0);
  const dobro = () => n() * 2;  // o derivado é uma função que lê o signal
  console.log("executou");      // roda uma vez só
  return <button onClick={() => setN(n() + 1)}>{n()} × 2 = {dobro()}</button>;
}
// "const dobro = n() * 2" seria lido uma vez e nunca atualizaria: a forma
// que está certa no React está errada no Solid.
```

Em vez de: uma notação declarativa com dois mecanismos, re-renderização e
reatividade fina; segue a letra das DCs ("the perceived marks or
symbols", Green e Blackwell 1998, p. 8) e desarma a objeção de que JSX é
JSX, mas trataria como ambiente as diferenças escritas que a análise mede
(valores derivados, efeitos, o corpo do componente) e mudaria a pergunta
dos ADRs 0011 e 0014.
Em vez de: notação como sintaxe, uma por forma de escrever a tela; fiel à
letra, mas juntaria React e Solid e separaria Solid e Angular, o
contrário do desenho do ADR 0013.
Custo: o texto precisa dizer o sentido de "notação" antes da análise,
porque ele se afasta da definição das DCs; cada diferença entre React e
Solid precisa de um trecho de código que a mostre; e os nomes "por
re-renderização" e "reativa fina" nomeiam mecanismos, o que o texto
precisa explicar.

Fontes: Green (1989, p. 3 da cópia, a conferir nas p. 443-460 dos anais:
as calculadoras que "differ only in the environment of use"); Green e
Blackwell, tutorial de 1998 (p. 8); Blackwell e Green (2003, p. 7 da
cópia: "what the user sees and edits"); Green e Petre (1996, p. 22 da
pré-publicação); Kiss (2014, p. 12, nota 2), que avalia "the
amalgamation of paradigm, language, toolkit and IDE"; react.dev, *Render
and Commit* e *State as a Snapshot*, e docs.solidjs.com, *Intro to
reactivity* ("Components […] will only run once"), em
`docs/literatura.md`, seção 8.1 (2026-09-26); react.dev, *Reacting to
Input with State* (2026-09-28): "you declare what you want to show";
ADRs 0011, 0013 e 0014.
