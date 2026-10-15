# Bibliotecas de formulário da terceira rodada

Referência. A biblioteca de formulário de cada tecnologia na terceira
rodada, com a medida pública do registro, a janela e a fonte, pela regra
do ADR 0031. Cada afirmação sobre ferramenta ou versão leva a data em que
foi observada; medidas de 2026-10-12, que refazem as de 2026-10-11 com a
janela registrada.

**Conclusão.** Quatro das nove tecnologias da terceira rodada ganham
biblioteca: o React, o react-hook-form; o Solid, o TanStack Solid Form; o
Angular com *signals*, os *Signal Forms* do `@angular/forms`; o WPF, o
CommunityToolkit.Mvvm. As outras cinco ficam com a API da plataforma: no
Web Component e no Lit, nenhuma candidata soma a maioria; no Views e no
Compose, o Maven não publica contagem; no Windows Forms, a maioria das
candidatas compatíveis são 177 downloads em seis semanas. A única maioria
estreita é a do Solid (52,9%).

## 1. A regra

Pelo ADR 0031, conta como candidata a biblioteca que guarda o estado do
formulário ou mostra o erro no campo, compatível com a plataforma da
tecnologia; o validador de objetos (FluentValidation, Konform, zod, yup)
fica fora. Domina a candidata com mais da metade dos downloads somados
das candidatas da tecnologia na janela. Sem contagem pública ou sem
maioria, vale a API da plataforma.

Janelas:

- **npm**: 2026-09-12 a 2026-10-11, 30 dias, pela API pública
  `https://api.npmjs.org/downloads/point/2026-09-12:2026-10-11/<pacote>`;
  versão e data pelo `https://registry.npmjs.org/<pacote>`.
- **NuGet**: as seis semanas que o nuget.org publica por pacote
  (`https://www.nuget.org/stats/reports/packages/<id>?groupby=Version`),
  relatórios atualizados em 2026-10-12 por volta das 20h UTC; o nuget.org
  não diz as datas exatas da janela. O total desde a publicação, da busca
  (`azuresearch-usnc.nuget.org/query`), vai como contexto.
- **Maven**: sem contagem pública de downloads (o Maven Central só mostra
  as estatísticas ao publicador); como contexto, os dependentes publicados
  no deps.dev e as estrelas no GitHub.

## 2. Tecnologia → biblioteca e versão

| Tecnologia | Biblioteca e versão (publicação) | Medida | Janela | Fonte |
|---|---|---|---|---|
| Web Component | API de validação de restrições da plataforma (`setCustomValidity`, `checkValidity`) | sem maioria: a maior candidata sem *framework*, o `final-form`, tem no máximo 49,2% | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org; MDN, *Constraint validation* (2026-10-12) |
| React | `react-hook-form` 7.90.0 (2026-10-11) | 255.298.395 downloads, 84,6% das candidatas, 12,6 vezes o `formik` | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |
| Solid | `@tanstack/solid-form` 1.33.5 (2026-08-11) | 213.307 downloads, 52,9% das candidatas, 1,74 vez o `@modular-forms/solid` | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |
| Lit | API de validação de restrições da plataforma, como no Web Component; Lit 3.3.3 (2026-05-14) | sem maioria: a líder, `@vaadin/hilla-lit-form`, tem 28,5% | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org |
| Angular com *signals* | `@angular/forms` 22.2.0 (2026-09-23), a mesma do `@angular/core` em `implementacoes/`, com os *Signal Forms* (`form()` de `@angular/forms/signals`) | 23.793.794 downloads, 95,9% das candidatas; a API escolhida pelo ADR 0031, porque a medida não separa as APIs do pacote | npm, 2026-09-12 a 2026-10-11 | api.npmjs.org; `types/_structure-chunk.d.ts` do pacote, `@publicApi 22.0` |
| Views | API da plataforma: o erro no campo do Material Components (`TextInputLayout.setError`), já em `libs.versions.toml` (`material` 1.14.0) | sem contagem pública | — | developer.android.com, `TextInputLayout` (2026-10-12) |
| Compose | API da plataforma: `isError` e `supportingText` do `TextField` do Material 3, do BOM 2026.09.00 de `libs.versions.toml` | sem contagem pública | — | `androidx/androidx`, `material3/.../TextField.kt` (ramo `androidx-main`, 2026-10-12) |
| Windows Forms | API da plataforma: `ErrorProvider` e o evento `Validating` | a maioria das candidatas compatíveis são 177 downloads, sem ecossistema (seção 3.2) | NuGet, seis semanas até 2026-10-12 | learn.microsoft.com, `ErrorProvider` (2026-10-12); `dotnet/winforms`, `ErrorProvider.cs` |
| WPF | `CommunityToolkit.Mvvm` 8.4.2 (2026-03-25), com o `ObservableValidator` (`INotifyDataErrorInfo`) | 3.329.052 downloads, 98,6% das candidatas | NuGet, seis semanas até 2026-10-12 | nuget.org/stats; learn.microsoft.com, *ObservableValidator* (2026-10-12) |

As versões entram nos arquivos de dependência
(`implementacoes/*/package.json`, os `.csproj` do desktop) quando a
terceira rodada começar (tcc-0yjr). A plataforma não ganha dependência
nova no Android, e no Web Component e no Lit a API é a do navegador.

## 3. Candidatas medidas

### 3.1 npm, 2026-09-12 a 2026-10-11

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
815.576.763 (19.3.0); `@angular/core` 27.227.175 (22.2.2); `solid-js`
26.673.877 (1.9.17, 2026-10-07); `lit` 31.952.129 (3.3.3).

### 3.2 NuGet, seis semanas até 2026-10-12

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

### 3.3 Maven, Android

Sem contagem pública. Dependentes publicados no deps.dev (só pacotes do
Maven Central, não aplicativos) e repositório no GitHub, em 2026-10-12:

| Pacote | Tipo | Última versão | Dependentes (deps.dev) | GitHub |
|---|---|---|---|---|
| `io.konform:konform-jvm` | valida objetos | 0.11.1 (2025-03-31) | 110 (14 diretos) | `konform-kt/konform`, 822 estrelas, *push* em 2026-10-08 |
| `com.mobsandgeeks:android-saripaar` | anotações nos campos das Views | 2.0.3 (2015-09-18) | 0 | `ragunathjawahar/android-saripaar`, 3.186 estrelas, *push* em 2020-12-03 |
| `org.valiktor:valiktor-core` | valida objetos | 0.12.0 | 18 (12 diretos) | `valiktor/valiktor`, 446 estrelas, *push* em 2021-12-16 |

## 4. Ressalvas

- **Download não é uso.** O registro conta integração contínua, espelhos e
  dependências transitivas; a medida compara pacotes entre si, não conta
  projetos.
- **Pacote não é API.** O `@angular/forms` reúne os Reactive Forms, os
  *template-driven* e os *Signal Forms*; o CommunityToolkit.Mvvm conta
  também quem o usa sem validação.
- **Maioria estreita no Solid.** Os 52,9% do TanStack Solid Form mudam com
  a lista de candidatas; a linhagem Modular Forms e Formisch, somada, tem
  37,5%.
- **Janela do NuGet.** São as seis semanas que o nuget.org publica, sem
  datas exatas; a do npm é fixa e se refaz pela mesma URL.

## 5. Fontes

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
`implementacoes/node_modules`.
