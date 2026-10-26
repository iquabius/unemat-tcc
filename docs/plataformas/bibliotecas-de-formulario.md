# Bibliotecas de formulário da terceira rodada

Referência. A biblioteca de formulário de cada tecnologia da análise na
Reserva de passagem, na terceira rodada, com a medida pública do
registro, a janela e a fonte, pela regra do ADR 0031. Cada afirmação
sobre ferramenta ou versão leva a data em que foi observada; medidas de
2026-10-12, que refazem as de 2026-10-11 com a janela registrada. As das
tecnologias que saíram da análise estão na seção "Tecnologias fora da
análise (medida de 2026-10-12)".

**Conclusão.** Duas das quatro tecnologias da análise (ADR 0013) ganham
biblioteca de formulário na terceira rodada: o React, o react-hook-form
7.90.0 (84,6% das candidatas), e o Solid, o TanStack Solid Form 1.33.5,
por uma maioria estreita (52,9%). O Web Component fica com a API de
validação de restrições da plataforma, porque nenhuma candidata sem
*framework* soma a maioria, e o Web Component com *signals* o segue por
decisão do autor, e não pela medida, para o passo entre os dois, que já
muda a ligação do estado com a tela e a orquestração (ADR 0013), não
mudar também a biblioteca (ADR 0031, decisão de 2026-10-19, mantida em
2026-10-23). A medida refeita em 2026-10-25, com eixos a mais e três
janelas, está na seção "Medida de 2026-10-25: eixos a mais e janelas":
confirma o React e muda o Solid e o Web Component conforme a janela, a
métrica e o filtro de manutenção.

## A regra

Pelo ADR 0031, conta como candidata a biblioteca que guarda o estado do
formulário ou mostra o erro no campo, compatível com a plataforma da
tecnologia; o validador de objetos (zod, yup) fica fora. Domina a
candidata com mais da metade dos downloads somados das candidatas da
tecnologia na janela. Sem maioria, vale a API da plataforma. O Web
Component com *signals* não se mede: segue o Web Component.

Janela: no npm, de 2026-09-12 a 2026-10-11, 30 dias, pela API pública
`https://api.npmjs.org/downloads/point/2026-09-12:2026-10-11/<pacote>`;
versão e data pelo `https://registry.npmjs.org/<pacote>`.

## Tecnologia → biblioteca e versão

| Tecnologia | Biblioteca e versão (publicação) | Medida | Janela | Fonte |
|---|---|---|---|---|
| Web Component | API de validação de restrições da plataforma (`setCustomValidity`, `checkValidity`) | sem maioria: a maior candidata sem *framework*, o `final-form`, tem no máximo 49,2% | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org; MDN, *Constraint validation* (2026-10-12) |
| Web Component com *signals* | API de validação de restrições da plataforma, como no Web Component | por decisão (ADR 0031) | — | ADR 0031 |
| React | `react-hook-form` 7.90.0 (2026-10-11) | 255.298.395 downloads, 84,6% das candidatas, 12,6 vezes o `formik` | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |
| Solid | `@tanstack/solid-form` 1.33.5 (2026-08-11) | 213.307 downloads, 52,9% das candidatas, 1,74 vez o `@modular-forms/solid` | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |

As versões entram no `package.json` de cada implementação quando a
terceira rodada começar (tcc-0yjr). No Web Component e no Web Component
com *signals*, a API é a do navegador.

## Candidatas medidas

Janela de 2026-09-12 a 2026-10-11, no npm.

Downloads na janela; versão `latest` e data dela no registro em
2026-10-12. A fração é sobre a soma das candidatas da tecnologia.

| Tecnologia | Pacote | Versão (data) | Downloads | Fração |
|---|---|---|---|---|
| React | `react-hook-form` | 7.90.0 (2026-10-11) | 255.298.395 | 84,6% |
| React | `formik` | 2.4.9 (2025-11-10) | 20.301.562 | 6,7% |
| React | `@tanstack/react-form` | 1.33.5 (2026-08-11) | 14.950.345 | 5,0% |
| React | `@rc-component/form` (o do Ant Design) | 1.8.6 (2026-07-27) | 5.496.573 | 1,8% |
| React | `react-final-form` | 7.0.1 (2026-05-05) | 2.446.029 | 0,8% |
| React | `redux-form` | 8.3.10 (2023-03-28) | 2.251.900 | 0,7% |
| React | `@conform-to/react` | 1.21.2 (2026-10-11) | 1.198.726 | 0,4% |
| Solid | `@tanstack/solid-form` | 1.33.5 (2026-08-11) | 213.307 | 52,9% |
| Solid | `@modular-forms/solid` (em manutenção; o README indica o Formisch) | 0.25.1 (2025-03-01) | 122.737 | 30,5% |
| Solid | `@formisch/solid` | 1.1.0 (2026-09-08) | 28.310 | 7,0% |
| Solid | `@solid-primitives/form` | 1.0.0-next.3 (2026-08-30) | 26.621 | 6,6% |
| Solid | `@felte/solid` | 1.2.14 (2024-10-29) | 11.998 | 3,0% |

Web Component, sem *framework*, na mesma janela:

| Pacote | Versão (data) | Downloads | Uso direto |
|---|---|---|---|
| `@tanstack/form-core` | 1.33.5 (2026-08-11) | 16.396.448 | nenhum medível: os adaptadores (`react-form` 14.950.345, `vue-form` 270.453, `solid-form` 213.307, `svelte-form` 138.008, `angular-form` 13.409, `lit-form` 9.823) e o `@tanstack/form-devtools` (1.102.954), que dependem dele, somam mais |
| `final-form` | 5.0.1 (2026-05-05) | 2.979.315 | no máximo 533.286, descontado o `react-final-form` |
| `vest` | 6.3.4 (2026-10-03) | 236.222 | — |
| `hyperform` | 0.12.1 (2022-07-26) | 172.977 | — |
| `@conform-to/dom` | 1.21.2 (2026-10-11) | 1.255.082 | no máximo 56.356, descontado o `@conform-to/react` |
| `just-validate` | 4.3.0 (2023-11-13) | 51.706 | — |
| `pristinejs` | 1.1.0 (2023-04-01) | 17.797 | — |
| `form-associated-helpers` | 0.0.11 (2024-07-13) | 16.209 | — |
| `@felte/element` | 0.5.14 (2024-10-29) | 347 | — |

O `jquery-validation` (1.22.1, 996.493) depende do jQuery e não entra.
Tomando os resíduos como uso direto, as candidatas somam cerca de 1,09
mi, e o `final-form` fica com no máximo 49,2%.

Downloads das tecnologias na mesma janela, para a escala: `react`
815.576.763 (19.3.0); `solid-js` 26.673.877 (1.9.17, 2026-10-07).

## Ressalvas

- **Download não é uso.** O registro conta integração contínua, espelhos e
  dependências transitivas; a medida compara pacotes entre si, não conta
  projetos.
- **Maioria estreita no Solid.** Os 52,9% do TanStack Solid Form mudam com
  a lista de candidatas; a linhagem Modular Forms e Formisch, somada, tem
  37,5%.

## Medida de 2026-10-25: eixos a mais e janelas

Medida de 2026-10-25, sobre as mesmas candidatas da seção "Candidatas
medidas", pelo método de `medida-das-bibliotecas.md` (os eixos, as
janelas, o filtro e as variantes de regra estão lá; os dados brutos, em
`tmp/pesquisas/2026-10-25-medida-das-bibliotecas/`). Três janelas de
downloads: a nova, 2026-09-25 a 2026-10-24, que a API do npm zera em 9
dos 30 dias; a do ADR, 2026-09-12 a 2026-10-11 (2 dias zerados); e a
limpa, 2026-07-27 a 2026-08-25 (1 dia zerado). A mediana é das quatro
semanas inteiras da janela nova. Dependentes publicados e repositórios
dependentes pelo ecosyste.ms, *hits* do mês no jsDelivr, versão e data
pelo registro, tudo no retrato de 2026-10-25. O filtro marca `24m` a
candidata sem versão há mais de 24 meses; nenhuma está depreciada ou
arquivada.

**O que muda.** No React, nada: o `react-hook-form` tem a maioria dos
downloads nas três janelas (83,9%, 84,6% e 85,8%) e dos *hits* do
jsDelivr (79,4%); só não a tem pelos dependentes publicados (42,9%) nem
pelos repositórios dependentes, em que o `formik` lidera por 106.319 a
105.160 (42,8%). No Solid, a maioria do TanStack Solid Form depende da
janela: 52,9% na do ADR, 52,0% na limpa e 47,0% na nova, em que o
`@solid-primitives/form` subiu de 26.621 para 39.298 downloads; pelos
repositórios dependentes a maioria é do `@modular-forms/solid` (60,1%),
e pelos dependentes publicados, do `@felte/solid` (70,0%, 7 pacotes). No
Web Component, o resíduo refeito na janela nova dá ao `final-form` 49,3%
(49,2% em 2026-10-12, e 49,2% com os downloads da janela do ADR baixados
de novo em 2026-10-25), e a API da plataforma fica nessas duas janelas;
mas na janela limpa o resíduo do `final-form` é 51,2% (485.872 de
949.350), e, tirando as quatro candidatas sem versão há mais de 24 meses
(`hyperform`, `just-validate`, `pristinejs` e `form-associated-helpers`),
62,7% na janela nova (382.894 de 610.581), 64,5% na do ADR e 61,0% na
limpa: a API da plataforma no Web Component depende da janela e do
filtro tanto quanto o TanStack Solid Form no Solid. Os adaptadores e o
devtools do TanStack (13.890.580) somam mais que o `@tanstack/form-core`
(13.704.508), de modo que o resíduo dele é zero nas três janelas. O eixo que mais diverge
é o jsDelivr: o `pristinejs` e o `just-validate`, sem versão desde 2023,
têm 3.191.371 e 2.965.017 *hits* por mês com 14.660 e 41.349 downloads,
que é o uso em páginas sem *bundler* que o npm não vê.

### React

| Pacote | Downloads nova (fração) | ADR | Limpa | Mediana semanal | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `react-hook-form` | 191.279.933 (83,9%) | 255.298.395 | 246.756.060 | 43.588.303 | 3.937 | 105.160 | 650.081 | 7.91.0 (2026-10-23) | 38/73 | 44.861 | |
| `formik` | 15.397.147 (6,8%) | 20.301.562 | 19.047.458 | 3.612.703 | 3.368 | 106.319 | 14.189 | 2.4.9 (2025-11-10) | 2/2 | 34.307 | |
| `@tanstack/react-form` | 12.513.770 (5,5%) | 14.950.345 | 11.174.178 | 3.041.962 | 0 | 1.835 | 19.979 | 1.33.5 (2026-08-11) | 36/148 | 6.734 | |
| `@rc-component/form` | 4.305.655 (1,9%) | 5.496.573 | 4.686.464 | 1.028.552 | 0 | 0 | 123.383 | 1.8.6 (2026-07-27) | 15/21 | 1.028 | |
| `react-final-form` | 1.791.750 (0,8%) | 2.446.029 | 2.609.242 | 421.976 | 698 | 10.605 | 2.364 | 7.0.1 (2026-05-05) | 1/3 | 7.435 | |
| `redux-form` | 1.706.469 (0,7%) | 2.251.900 | 2.155.269 | 388.556 | 1.158 | 23.023 | 7.740 | 8.3.10 (2023-03-28) | 0/0 | 12.473 | 24m |
| `@conform-to/react` | 952.798 (0,4%) | 1.198.726 | 1.026.328 | 237.688 | 6 | 1.471 | 1.294 | 1.21.2 (2026-10-11) | 21/42 | 2.583 | |

O `react` teve 642.034.744 downloads na janela nova: o `react-hook-form` é
29,8% dele. O Snyk Advisor dá 90/100 ao `react-hook-form` ("Key ecosystem
project"; manutenção "Sustainable"; comunidade "Active"). A tag
`react-hook-form` tem 2.560 perguntas no Stack Overflow (1.714 desde
2021-10-25, 11 no último ano) e a `formik`, 2.838 (1.003, 0); o tópico
`react-hook-form` no GitHub tem 6.330 repositórios (5.901 criados desde
2021-10-25) e `formik`, 2.974 (2.075); no dev.to, 50 artigos com a tag
`reacthookform` (39 desde 2021-10-25) e 52 com `formik` (31). O State of React 2024 e 2025 pergunta
pelas bibliotecas de formulário (`react_hook_form`, `formik`,
`react_final_form`, `redux_form`, `react_json_schema_form`, `formily`,
`mantine_forms`; em 2025, também `conform` e `tanstack_form`), e o
`page-data.json` da página *Component Libraries* traz os resultados: o
`react-hook-form` foi usado por 74,3% dos que responderam em 2025 e
70,8% em 2024, o `formik` por 41,4% e 46,3%, o TanStack Form por 21,5%
e 0,7%; entre as escolhas das candidatas, o `react-hook-form` tem 47,8%
em 2025 e 51,6% em 2024 (`medida-das-bibliotecas.md`, seção "Pesquisa
de uso: o State of React"). O Developer Survey do Stack Overflow não
pergunta por nenhuma. No OpenAlex,
"react-hook-form" devolve 53 trabalhos desde 2021 e "formik form
library", 2.

### Solid

| Pacote | Downloads nova (fração) | ADR | Limpa | Mediana semanal | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `@tanstack/solid-form` | 145.546 (47,0%) | 213.307 | 195.218 | 30.056 | 0 | 39 | 482 | 1.33.5 (2026-08-11) | 36/134 | 6.734 | |
| `@modular-forms/solid` | 86.860 (28,1%) | 122.737 | 138.873 | 19.184 | 3 | 137 | 925 | 0.25.1 (2025-03-01) | 0/2 | 1.210 | |
| `@solid-primitives/form` | 39.298 (12,7%) | 26.621 | 1.951 | 9.332 | 0 | 1 | 239 | 1.0.0-next.5 (2026-10-14) | 5/5 | 1.560 | |
| `@formisch/solid` | 28.979 (9,4%) | 28.310 | 11.738 | 7.615 | 0 | 1 | 836 | 1.1.0 (2026-09-08) | 24/31 | 1.205 | |
| `@felte/solid` | 8.694 (2,8%) | 11.998 | 27.448 | 2.138 | 7 | 50 | 58 | 1.2.14 (2024-10-29) | 0/1 | 1.088 | |

O `solid-js` teve 23.765.155 downloads na janela nova: o TanStack Solid
Form é 0,6% dele. O Snyk Advisor não dá nota ao `@tanstack/solid-form`.
Nenhuma candidata tem tag própria no Stack Overflow (consultadas em
2026-10-25 `tanstack-form`, `modular-forms`, `felte`, `formisch` e
`solid-primitives`; só a tag genérica `tanstack` existe, com 184
perguntas); o tópico `tanstack-form` no GitHub tem 153 repositórios (151 criados desde 2021-10-25), sem separar
o adaptador do Solid; no dev.to, 1 artigo com `tanstackform`. No
OpenAlex, "TanStack Form" devolve 0 trabalhos.

### Web Component

| Pacote | Downloads nova (fração bruta) | ADR | Limpa | Resíduo na janela nova | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `@tanstack/form-core` | 13.704.508 (79,6%) | 16.396.448 | 12.477.227 | 0 (os adaptadores e o devtools somam 13.890.580) | 2 | 835 | 15.219 | 1.33.5 (2026-08-11) | 36/132 | 6.734 | |
| `final-form` | 2.174.644 (12,6%) | 2.979.315 | 3.095.114 | 382.894 (descontado o `react-final-form`), 49,3% | 704 | 11.066 | 3.505 | 5.0.1 (2026-05-05) | 1/6 | 3.048 | |
| `@conform-to/dom` | 997.383 (5,8%) | 1.255.082 | 1.082.860 | 44.585 (descontado o `@conform-to/react`) | 3 | 1.098 | 1.171 | 1.21.2 (2026-10-11) | 21/42 | 2.583 | |
| `vest` | 182.863 (1,1%) | 236.222 | 253.597 | 182.863, 23,5% | 18 | 104 | 35.607 | 6.3.4 (2026-10-03) | 289/295 | 2.670 | |
| `hyperform` | 98.347 (0,6%) | 172.977 | 50.443 | 98.347 | 18 | 560 | 661 | 0.12.1 (2022-07-26) | 0/0 | 734 | 24m |
| `just-validate` | 41.349 (0,2%) | 51.706 | 50.706 | 41.349 | 4 | 475 | 2.965.017 | 4.3.0 (2023-11-13) | 0/0 | 591 | 24m |
| `pristinejs` | 14.660 (0,1%) | 17.797 | 15.615 | 14.660 | 6 | 135 | 3.191.371 | 1.1.0 (2023-04-01) | 0/0 | 436 | 24m |
| `form-associated-helpers` | 11.906 (0,1%) | 16.209 | 36.227 | 11.906 | 0 | 1 | 507 | 0.0.11 (2024-07-13) | 0/0 | 11 | 24m |
| `@felte/element` | 239 (0,0%) | 347 | 358 | 239 | 1 | 2 | 36 | 0.5.14 (2024-10-29) | 0/1 | 1.088 | |

O resíduo total é 776.843. Os adaptadores na janela nova:
`@tanstack/react-form` 12.513.770, `@tanstack/vue-form` 209.649,
`@tanstack/solid-form` 145.546, `@tanstack/svelte-form` 93.304,
`@tanstack/angular-form` 10.580, `@tanstack/lit-form` 9.128 e
`@tanstack/form-devtools` 908.603. Pelos dependentes publicados o
`final-form` tem 93,1% das nove candidatas e pelos repositórios
dependentes, 77,5%; pelo jsDelivr, o `pristinejs` tem 51,4% e, tirando os
pacotes sem versão há 24 meses, o `vest`, 64,1%.

### Sensibilidade

O resultado da regra do ADR 0031 e das variantes de
`medida-das-bibliotecas.md`, por tecnologia; "API" é a API da
plataforma.

| Tecnologia | Downloads, nova | Downloads, ADR | Downloads, limpa | Mediana semanal | Dependentes publicados | Repositórios dependentes | jsDelivr | Com filtro (24 m) |
|---|---|---|---|---|---|---|---|---|
| React | `react-hook-form` 83,9% | 84,6% | 85,8% | 83,3% | API (42,9%) | API (`formik` 42,8%) | `react-hook-form` 79,4% | `react-hook-form` 84,5% |
| Solid | API (`@tanstack/solid-form` 47,0%) | `@tanstack/solid-form` 52,9% | `@tanstack/solid-form` 52,0% | API (`@tanstack/solid-form` 44,0%) | `@felte/solid` 70,0% | `@modular-forms/solid` 60,1% | API (`@modular-forms/solid` 36,4%) | API (`@tanstack/solid-form` 47,0%) |
| Web Component (pelo resíduo) | API (`final-form` 49,3%) | API (`final-form` 49,2%) | `final-form` 51,2% | — | `final-form` 93,1% | `final-form` 77,5% | `pristinejs` 51,4% | `final-form` 62,7% |

### Busca de código e Google Trends

Medidos em 2026-10-25 pelo método de `medida-das-bibliotecas.md`
(seção "Busca de código e Google Trends"). Os `package.json` do GitHub
que declaram cada candidata (`gh api search/code`, sem janela) dão a
maioria ao `react-hook-form` no React (993.280 de 1.147.256 arquivos,
86,6%; o `formik`, 124.928, 10,9%), a ninguém no Solid (o
`@modular-forms/solid` tem 219 dos 520, 42,1%, e o TanStack Solid Form,
190, 36,5%) e ao `final-form` no Web Component (3.536 de 4.882, 72,4%;
88,7% sem as candidatas sem versão há 24 meses). No Google Trends, o
`react hook form` tem 51,8% do grupo das cinco do React em cinco anos e
48,0% em doze meses, em que o `tanstack form` sobe a 15,4%; o termo
junta o TanStack Form de todos os *frameworks*, e sem ele o `react hook
form` tem 56,8%. Os termos do Solid ficam no ruído (médias abaixo de 2;
"modular forms" sozinho é assunto de matemática), e os do Web Component
não dão maioria a ninguém, com o `final-form` em 10,2% e 12,2%, atrás de
`hyperform` e `vest validation`, que não se conferiu buscarem os
pacotes.

## Tecnologias fora da análise (medida de 2026-10-12)

O Lit, o Angular com *signals*, as Views, o Compose, o Windows Forms e o
WPF saíram da análise (ADRs 0001 e 0013), e as medidas deles ficam
aqui, sem mudança, para os trabalhos futuros da conclusão (decisão do
autor de 2026-10-19; tcc-dpci). O Lit voltou à análise nas sete
interfaces em 2026-10-25 (tcc-cp6c), e a lista dele, com duas candidatas
fora do critério, se corrige na subseção "Lit: a lista corrigida". Pela
mesma regra, ganhavam biblioteca o
Angular com *signals*, os *Signal Forms* do `@angular/forms`, e o WPF, o
CommunityToolkit.Mvvm. Ficavam com a API da plataforma o Lit, em que
nenhuma candidata somava a maioria; as Views e o Compose, porque o Maven
não publica contagem; e o Windows Forms, em que a maioria das candidatas
compatíveis são 177 downloads em seis semanas. No .NET e no Kotlin, os
validadores de objetos que a regra deixa fora são o FluentValidation e o
Konform; sem contagem pública, vale a API da plataforma.

Janelas, além da do npm:

- **NuGet**: as seis semanas que o nuget.org publica por pacote
  (`https://www.nuget.org/stats/reports/packages/<id>?groupby=Version`),
  relatórios atualizados em 2026-10-12 por volta das 20h UTC; o nuget.org
  não diz as datas exatas da janela. O total desde a publicação, da busca
  (`azuresearch-usnc.nuget.org/query`), vai como contexto.
- **Maven**: sem contagem pública de downloads (o Maven Central só mostra
  as estatísticas ao publicador); como contexto, os dependentes publicados
  no deps.dev e as estrelas no GitHub.

| Tecnologia | Biblioteca e versão (publicação) | Medida | Janela | Fonte |
|---|---|---|---|---|
| Lit | API de validação de restrições da plataforma, como no Web Component; Lit 3.3.3 (2026-05-14) | sem maioria: a líder, `@vaadin/hilla-lit-form`, tem 28,5% | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |
| Angular com *signals* | `@angular/forms` 22.2.0 (2026-09-23), a mesma do `@angular/core` então em `implementacoes/`, com os *Signal Forms* (`form()` de `@angular/forms/signals`) | 23.793.794 downloads, 95,9% das candidatas; a API escolhida pelo ADR 0031, porque a medida não separa as APIs do pacote | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org; `types/_structure-chunk.d.ts` do pacote, `@publicApi 22.0` |
| Views | API da plataforma: o erro no campo do Material Components (`TextInputLayout.setError`), já em `libs.versions.toml` (`material` 1.14.0) | sem contagem pública | — | developer.android.com, `TextInputLayout` (2026-10-12) |
| Compose | API da plataforma: `isError` e `supportingText` do `TextField` do Material 3, do BOM 2026.09.00 de `libs.versions.toml` | sem contagem pública | — | `androidx/androidx`, `material3/.../TextField.kt` (ramo `androidx-main`, 2026-10-12) |
| Windows Forms | API da plataforma: `ErrorProvider` e o evento `Validating` | a maioria das candidatas compatíveis são 177 downloads, sem ecossistema (seção "NuGet") | NuGet, seis semanas até 2026-10-12 | learn.microsoft.com, `ErrorProvider` (2026-10-12); `dotnet/winforms`, `ErrorProvider.cs` |
| WPF | `CommunityToolkit.Mvvm` 8.4.2 (2026-03-25), com o `ObservableValidator` (`INotifyDataErrorInfo`) | 3.329.052 downloads, 98,6% das candidatas | NuGet, seis semanas até 2026-10-12 | nuget.org/stats; learn.microsoft.com, *ObservableValidator* (2026-10-12) |

A versão do WPF entraria no `.csproj` dele. A plataforma não ganharia
dependência nova no Android, e no Lit a API é a do navegador.

### npm: Lit e Angular

Janela de 2026-09-12 a 2026-10-11; versão `latest` e data dela no
registro em 2026-10-12. A fração é sobre a soma das candidatas da
tecnologia.

| Tecnologia | Pacote | Versão (data) | Downloads | Fração |
|---|---|---|---|---|
| Lit | `@vaadin/hilla-lit-form` (presa ao *backend* do Vaadin Hilla) | 25.2.12 (2026-10-12) | 39.293 | 28,5% |
| Lit | `@open-wc/form-control` | 1.0.0 (2023-10-02) | 37.294 | 27,0% |
| Lit | `@lion/ui` (biblioteca de componentes inteira) | 0.22.0 (2026-10-12) | 31.703 | 23,0% |
| Lit | `@lion/form-core` | 0.18.3 (2022-09-08) | 19.954 | 14,5% |
| Lit | `@tanstack/lit-form` | 1.25.5 (2026-08-11) | 9.823 | 7,1% |
| Angular | `@angular/forms` | 22.2.2 (2026-10-08) | 23.793.794 | 95,9% |
| Angular | `@ngx-formly/core` | 9.0.0 (2026-10-07) | 976.284 | 3,9% |
| Angular | `@ngneat/reactive-forms` | 5.0.2 (2022-12-04) | 30.152 | 0,1% |
| Angular | `@tanstack/angular-form` | 1.33.5 (2026-08-11) | 13.409 | 0,1% |
| Angular | `ngx-vest-forms` | 2.7.0 (2026-05-06) | 1.170 | 0,0% |

Downloads das tecnologias na mesma janela, para a escala:
`@angular/core` 27.227.175 (22.2.2); `lit` 31.952.129 (3.3.3).

### Lit: a lista corrigida

Conclusão (2026-10-25): duas das cinco candidatas do Lit medidas em
2026-10-12 estão fora do critério da regra, a biblioteca que guarda o
estado do formulário ou mostra o erro no campo, e saem da lista; com a
regra I, a maioria dos downloads depois do filtro de manutenção, que o
autor decidiu em 2026-10-25 e que conta a depreciação dita na
documentação (`medida-das-bibliotecas.md`, seção "O filtro de
depreciação e manutenção"), sobra só o `@tanstack/lit-form`. Se o Lit
segue essa medida, ou o Web Component, como o Web Component com
*signals*, é decisão do ADR 0031, ainda não tomada.

Saem da lista:

- o `@open-wc/form-control` ("Base class for creating form-participating
  custom elements", no registro): serve para escrever um controle de
  formulário, o elemento personalizado que participa do `<form>` pelo
  `ElementInternals` (o FACE), e não para coordenar o estado e os erros
  de um formulário; pelo mesmo motivo fica fora o `@lit-labs/forms`
  0.1.0 (2025-12-23), dos *mixins* para escrever esse controle no Lit,
  com 25 downloads na janela;
- o `@lion/ui` 0.25.0 (2026-10-19), biblioteca de componentes inteira,
  como as coleções de *hooks* que o ADR 0031 tira do Placar ao vivo: os
  downloads vêm dos outros componentes; o *form-core* do Lion, sem
  versão própria desde 2022-09-08, continua dentro dele, em
  `components/form-core`.

Ficam três, na janela do ADR, de 2026-09-12 a 2026-10-11, com a fração
sobre as que ficam em cada coluna:

| Candidata | Downloads | Sem filtro | Sem a de 24 meses | Regra I |
|---|---|---|---|---|
| `@vaadin/hilla-lit-form` 25.2.13 (2026-10-21) | 39.293 | 56,9% | 80,0% | sai: "Hilla with Lit is deprecated and is removed in Vaadin 26" (vaadin.com/docs, Form Binding Reference, lida em 2026-10-25) |
| `@lion/form-core` 0.18.3 (2022-09-08) | 19.954 | 28,9% | sai (24m) | sai (24m) |
| `@tanstack/lit-form` 1.25.5 (2026-08-11) | 9.823 | 14,2% | 20,0% | 100% (candidata única) |

O Hilla prende o formulário ao *backend*: os modelos que o `Binder`
recebe são gerados de classes Java ("The model classes aren't intended
to be instantiated manually", mesma página). Os dados de 2026-10-25
estão em `tmp/pesquisas/2026-10-25-formulario-no-lit/` (fora do git).

### NuGet

Seis semanas até 2026-10-12.

| Tecnologia | Pacote | Versão | Seis semanas | Total desde a publicação | Fração |
|---|---|---|---|---|---|
| WPF | `CommunityToolkit.Mvvm` | 8.4.2 (2026-03-25) | 3.329.052 | 29.287.276 | 98,6% |
| WPF | `ReactiveUI.Validation` | 8.1.0 | 27.015 | 820.876 | 0,8% |
| WPF | `MvvmValidation` | 3.1.2 | 12.011 | 585.639 | 0,4% |
| WPF | `Validar.Fody` | 1.9.0 | 6.534 | 342.607 | 0,2% |
| Windows Forms | `EnterpriseLibrary.Validation.Integration.WinForms` | 6.0.1304 (2013-04-26), alvo só `.NETFramework4.5` | 3.436 | 115.969 | incompatível |
| Windows Forms | `Kimtoo.ValidationProvider` (vendido no Gumroad) | 1.0.8 (2022-04-14) | 177 | 30.140 | 70,5%, sem ecossistema (ADR 0031) |
| Windows Forms | `Tools.ControlValidation` | 1.0.6 (2015-07-06) | 74 | 12.284 | 29,5% |
| fora (valida objetos) | `FluentValidation` | 12.2.0 | 55.952.979 | 1.072.947.795 | — |

O `ObservableValidator` do CommunityToolkit.Mvvm implementa o
`INotifyDataErrorInfo`, que a ligação do WPF mostra no campo; o
`ErrorProvider` do Windows Forms só lê `IDataErrorInfo` (`dotnet/winforms`,
`ErrorProvider.cs`, ramo `main`, 2026-10-12), e por isso o toolkit não é
candidata ali. Das duas candidatas compatíveis que sobram, o
Kimtoo.ValidationProvider tem a maioria, mas com 177 downloads em seis
semanas, o que não indica ecossistema; o ADR 0031 declara o caso, e o
Windows Forms fica com a API da plataforma.

### Maven, Android

Sem contagem pública. Dependentes publicados no deps.dev (só pacotes do
Maven Central, não aplicativos) e repositório no GitHub, em 2026-10-12:

| Pacote | Tipo | Última versão | Dependentes (deps.dev) | GitHub |
|---|---|---|---|---|
| `io.konform:konform-jvm` | valida objetos | 0.11.1 (2025-03-31) | 110 (14 diretos) | `konform-kt/konform`, 822 estrelas, *push* em 2026-10-08 |
| `com.mobsandgeeks:android-saripaar` | anotações nos campos das Views | 2.0.3 (2015-09-18) | 0 | `ragunathjawahar/android-saripaar`, 3.186 estrelas, *push* em 2020-12-03 |
| `org.valiktor:valiktor-core` | valida objetos | 0.12.0 | 18 (12 diretos) | `valiktor/valiktor`, 446 estrelas, *push* em 2021-12-16 |

### Ressalvas destas tecnologias

- **Pacote não é API.** O `@angular/forms` reúne os Reactive Forms, os
  *template-driven* e os *Signal Forms*; o CommunityToolkit.Mvvm conta
  também quem o usa sem validação.
- **Janela do NuGet.** São as seis semanas que o nuget.org publica, sem
  datas exatas; a do npm é fixa e se refaz pela mesma URL.

## Fontes

API de downloads do npm (`api.npmjs.org/downloads/point`) e registro npm
(`registry.npmjs.org`), consultados em 2026-10-12; busca do npm
(`registry.npmjs.org/-/v1/search`) para levantar as candidatas;
NUGET, relatórios por pacote (`nuget.org/stats/reports/packages`), busca
(`azuresearch-usnc.nuget.org/query`), *nuspec* e registro
(`api.nuget.org/v3`), 2026-10-12; deps.dev (`api.deps.dev/v3` e
`v3alpha`, dependentes) e `api.github.com`, 2026-10-12; README de
`fabian-hiller/modular-forms` (2026-10-12); MDN, *Constraint validation*
(2026-10-12); MICROSOFT, learn.microsoft.com, `ErrorProvider` e
*ObservableValidator* (2026-10-12); `dotnet/winforms`, `ErrorProvider.cs`;
ANDROID, developer.android.com, `TextInputLayout` (2026-10-12);
`androidx/androidx`, `TextField.kt` do Material 3; angular.dev,
*Forms* (2026-10-12); `@angular/forms` 22.2.0 instalado em
`implementacoes/node_modules` (2026-10-12; o Angular saiu do
repositório em 2026-10-25).

## Histórico

- 2026-10-12: criada como `docs/bibliotecas-de-formulario.md` com a
  medida da tcc-di3a, nas nove tecnologias de então, pelo npm, pelo
  NuGet e pelo Maven, com a regra do ADR 0031.
- 2026-10-16: veio para `docs/plataformas/`.
- 2026-10-19: a conclusão, a regra, a janela e a tabela por tecnologia
  passaram às quatro tecnologias da análise (ADR 0013), com a linha do
  Web Component com *signals*, que segue o Web Component por decisão
  (ADR 0031); as medidas do Lit, do Angular, do NuGet e do Maven, com as
  ressalvas que só valem para elas, foram sem mudança para a seção
  "Tecnologias fora da análise (medida de 2026-10-12)".
- 2026-10-23: a conclusão passou a dar como motivo de o Web Component
  com *signals* seguir o Web Component que o passo entre os dois, que
  já muda a ligação do estado com a tela e a orquestração (ADR 0013),
  não mude também a biblioteca; antes, dizia que o par continuaria
  diferindo só na ligação. A decisão ficou (decisão do autor).
- 2026-10-25: ganhou a seção "Medida de 2026-10-25: eixos a mais e
  janelas", com as mesmas candidatas medidas em três janelas e pelos
  eixos de `medida-das-bibliotecas.md`, e a frase da conclusão que
  aponta para ela; a regra, a janela e as tabelas de 2026-10-12 ficaram.
  Depois, no mesmo dia, a subseção "Busca de código e Google Trends" e
  os resultados do State of React na seção do React.
- 2026-10-25, depois: com o Lit de volta à análise, ganhou a subseção
  "Lit: a lista corrigida", que tira da lista de 2026-10-12 o
  `@open-wc/form-control` (controle de formulário) e o `@lion/ui`
  (biblioteca de componentes inteira) e mede as três que ficam pela
  regra I; a tabela de 2026-10-12 ficou como estava.
