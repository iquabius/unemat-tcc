# Implementações de referência no CodeSandbox

Referência. São as implementações que o autor escreveu à mão no
CodeSandbox, antes das implementações atuais de `casos/`. As atuais foram
geradas com agentes de IA a partir de algumas destas, e ficaram mais
padronizadas entre as tecnologias. Lista do autor de 2026-10-07; os links
não foram abertos nesta data.

## O que ainda não se sabe

Não está registrado quais destas implementações, nem em que versão,
serviram de base quando o autor pediu aos agentes as implementações
atuais (informação do autor em 2026-10-07). Isso pesa na decisão sobre
declarar os agentes na metodologia (pauta da orientação de 2026-10-09,
ponto A4, tcc-y4q). Para mapear, o código de cada uma pode ser baixado
do CodeSandbox e comparado com `casos/`.

Nenhuma delas está no projeto de TCC entregue em 2017
(`../unemat-projeto-tcc`), que não nomeia programas. A menção mais antiga
no repositório é o link do Contador com POO em `texto/cases.org`, de
2020-03-04 (commit `09d0a2b`).

## Lista

| Interface | Implementação no CodeSandbox | Tarefa atual |
|---|---|---|
| Contador | [contador-com-callback](https://codesandbox.io/p/sandbox/contador-com-callback-m66fh?file=%2Fsrc%2Findex.js) | Contador |
| Contador | [contador-com-oop-callbacks](https://codesandbox.io/p/sandbox/contador-com-oop-callbacks-nst9y), citada num comentário de `texto/cases.org` | Contador |
| Contador | [contador-com-oop-funcao-de-seta](https://codesandbox.io/p/sandbox/contador-com-oop-funcao-de-seta-jv2ei) | Contador |
| Contador | [contador-com-rxjs](https://codesandbox.io/p/sandbox/contador-com-rxjs-odfoq?file=%2Fsrc%2Findex.js) | Contador |
| Contador | [contador-com-rxjs-2](https://codesandbox.io/p/sandbox/contador-com-rxjs-2-t00ud?file=%2Fsrc%2Findex.js) | Contador |
| Conversor de temperatura | [conversor-de-temperatura-com-poo](https://codesandbox.io/p/sandbox/conversor-de-temperatura-com-poo-0tcxt) | nenhuma |
| Conversor de temperatura | [conversor-de-temperatura-com-rxjs-5](https://codesandbox.io/p/sandbox/conversor-de-temperatura-com-rxjs-5-ez3is) | nenhuma |
| Reserva de voo | [reserva-de-voo-com-poo](https://codesandbox.io/p/sandbox/reserva-de-voo-com-poo-w9jei) | Formulário com validação |
| Reserva de voo | [reserva-de-voo-com-rxjs-5](https://codesandbox.io/p/sandbox/reserva-de-voo-com-rxjs-5-f9svq) | Formulário com validação |
| Reserva de voo | [reserva-de-voo-com-xstream](https://codesandbox.io/p/sandbox/reserva-de-voo-com-xstream-6vucn) | Formulário com validação |
| Cronômetro | [cronometro-com-rxjs-5](https://codesandbox.io/p/sandbox/cronometro-com-rxjs-5-zg544) | nenhuma; há uma cópia em `casos/cronometro-com-rxjs-5` (commit `6eb671c`, 2020-03-27), fora da análise (ADR 0012) e não comparada com o CodeSandbox |

O Contador, o Conversor de temperatura e a Reserva de voo têm os nomes de
três tarefas do 7GUIs (*Counter*, *Temperature Converter* e *Flight
Booker*; Kiss 2014). A introdução diz que o Contador e o Formulário com
validação adaptam o *Counter* e o *Flight Booker*. A Busca com sugestões,
a Lista filtrável e o Carrinho não têm implementação de referência na
lista.
