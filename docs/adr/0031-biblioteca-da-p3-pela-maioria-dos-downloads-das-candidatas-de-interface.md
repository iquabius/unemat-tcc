# 0031. Na P3, cada tecnologia usa a biblioteca de formulário que tem a maioria dos downloads das candidatas de interface no registro, ou a API da plataforma

2026-10-12. O ADR 0029 manda a P3 reescrever a interface base com a
biblioteca de formulário mais usada no ecossistema de cada tecnologia,
pela medida pública do registro, ou com a API da plataforma quando
nenhuma domina, sem dizer o que é biblioteca de formulário nem quando
ela domina. Conta como candidata a biblioteca que guarda o estado do
formulário ou mostra o erro no campo, compatível com a plataforma da
tecnologia; o validador de objetos, como o FluentValidation e o Konform,
fica fora, como o zod e o yup no npm. Domina a candidata que soma mais da
metade dos downloads das candidatas da tecnologia numa janela registrada
(npm, 2026-09-12 a 2026-10-11; NuGet, as seis semanas até 2026-10-12); sem
contagem pública, como no Maven, vale a API da plataforma. Saem o
react-hook-form 7.90.0 no React (84,6%), o TanStack Solid Form 1.33.5 no
Solid (52,9%), o `@angular/forms` 22.2.0 no Angular com *signals*
(95,9%), com os *Signal Forms*, e o CommunityToolkit.Mvvm 8.4.2 no WPF
(98,6%); Web Component, Lit, Views, Compose e Windows Forms ficam com a
API da plataforma. No Angular, a medida escolhe o pacote, e não a API: os
*Signal Forms* (`form()`, `@publicApi 22.0`) mantêm o `angular-signals`
sem RxJS (ADR 0013). No Windows Forms, o ErrorProvider só lê
`IDataErrorInfo`, e não o `INotifyDataErrorInfo` do CommunityToolkit; a
integração da Enterprise Library (6.0.1304, 2013) só tem alvo no .NET
Framework 4.5; e a maioria das duas candidatas que sobram, a do
Kimtoo.ValidationProvider 1.0.8 (2022-04-14), são 177 downloads em seis
semanas, o que não indica ecossistema: é um caso declarado, sem piso
numérico na regra. A tabela com as medidas está em
`docs/bibliotecas-de-formulario.md`, e as versões se fixam nos arquivos
de dependência quando a P3 começar.

Em vez de: contar o validador de objetos como biblioteca de interface; o
FluentValidation domina o NuGet (55,95 mi de downloads em seis semanas,
17 vezes o CommunityToolkit.Mvvm) e daria a mesma biblioteca ao Windows
Forms e ao WPF, mas a contagem vem sobretudo do servidor, a ligação do
erro à tela ficaria escrita à mão, e pela mesma regra o zod contaria na
web.
Em vez de: exigir que a líder tenha o dobro da segunda; mais robusto
contra a lista de candidatas, mas o Solid (1,74 vez o Modular Forms)
passaria à API da plataforma, e a P3 do Solid não mostraria o ecossistema
que ele tem.
Em vez de: exigir uma fração mínima dos downloads da própria tecnologia,
como 5%; mede a adoção dentro do ecossistema (react-hook-form 31% do
`react`, `@angular/forms` 87% do `@angular/core`), mas o limiar seria
arbitrário, e o Solid (0,8% do `solid-js`) e o Lit cairiam.
Em vez de: os Reactive Forms no Angular; o guia (angular.dev/guide/forms,
2026-10-12) ainda os recomenda "if forms are a key part of your
application", mas levariam *Observables* ao `angular-signals`, misturando
dois modelos de programação, e repetiriam o `angular-rxjs`.
Em vez de: um piso numérico, como uma fração mínima dos downloads da
tecnologia ou um número mínimo na janela; resolveria o Windows Forms pela
regra, mas o piso seria arbitrário e teria de ser conferido em cada
tecnologia.
Em vez de: o Kimtoo.ValidationProvider no Windows Forms, pela regra à
risca; coerente, mas é um pacote comercial sem versão desde 2022-04, e
a P3 mediria uma biblioteca sem ecossistema.
Custo: a maioria do Solid é estreita e muda com a lista de candidatas; os
downloads contam integração contínua e dependências transitivas, e os
pacotes núcleo (`@tanstack/form-core`, `final-form`) só entram pelo
resíduo depois de descontados os adaptadores; o download do
`@angular/forms` não diz qual API se usa, e o do CommunityToolkit.Mvvm
conta o uso de MVVM sem validação; a janela do NuGet é a que o
nuget.org publica, sem datas exatas; o React × Solid da P3 compara duas
bibliotecas diferentes, e a conclusão se lê como do ecossistema (ADR
0029); uma medida refeita em outra data pode mudar a escolha, que fica
fixada pela janela registrada.

Fontes: api.npmjs.org/downloads e registry.npmjs.org (2026-10-12);
nuget.org/stats/reports/packages e a busca do NuGet (2026-10-12);
deps.dev e api.github.com para o Maven (2026-10-12);
`@angular/forms` 22.2.0, `types/signals.d.ts` e
`types/_structure-chunk.d.ts`; `dotnet/winforms`, `ErrorProvider.cs`
(ramo `main`, 2026-10-12); ADRs 0013 e 0029; tcc-di3a.
