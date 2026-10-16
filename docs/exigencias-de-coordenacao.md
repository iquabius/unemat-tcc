# Exigências de coordenação: o que cada interface pede, e o que cada par cobre

Referência. Lista, interface por interface, as exigências de coordenação
que as especificações definem nos dois eixos (`CONTEXT.md`), agrupadas em
tipos, e diz quais tipos cada par de tecnologias cobre na primeira e na
segunda rodada. Serve de base para comparar outros pares como se comparou
Views × Compose em `docs/plataformas/android.md`, seção "Hipótese sobre
o ambiente de execução do Compose", e para pesar o equilíbrio dos pares.
Lido em 2026-10-15 nos `spec.md` de `implementacoes/openspec/specs/`,
nos ADRs 0002, 0005 e 0029 e nas descrições das tarefas da segunda
rodada (tcc-32dr, tcc-k9i2, tcc-r29v, tcc-buku, tcc-dnk5). Os nomes dos
tipos são proposta do agente, revista pelo autor em 2026-10-16; nenhum
entrou no `CONTEXT.md`.

**Conclusão.** A orquestração de eventos tem sete tipos nas cinco
interfaces, e o gerenciamento de estado, nove. Nenhum par cobre todos. O
Windows Forms × WPF é o mais equilibrado: o Formulário e o Quadro no
estado, o Login na orquestração, com as três políticas de concorrência e
os relógios. O Web Component × Lit pende para a orquestração, sem estado
compartilhado; o Solid × Angular com *signals*, para o estado, sem relógio
nem ciclo de vida preso a um estado; o Views × Compose é o mais forte no
gerenciamento de estado e não tem a política em que a requisição nova
cancela a anterior. A ordem de corte do ADR 0029 começa pelo Quadro do
Angular, que leva consigo o estado compartilhado e a fila do par Solid ×
Angular.

## Tipos de orquestração de eventos

| Tipo | O que exige | Onde (rodada) |
|---|---|---|
| O1. Pedido novo com outro em andamento | a política quando o usuário faz um pedido novo com outro em andamento: **substituição**, o novo cancela o anterior, e a resposta cancelada nunca aparece (*switch*); **descarte**, o pedido novo é ignorado até a resposta (*exhaust*); **fila**, os pedidos se aplicam na ordem dos cliques (*concat*) | substituição: Busca, termo novo (1ª); Login, tentativa nova (1ª). Descarte: envio do Formulário (1ª, tcc-32dr). Fila: atualização otimista do Quadro (2ª). Sem política definida: validação do e-mail (2ª) |
| O2. Tempo | **espera** depois da última tecla (*debounce*); **relógio** que a interface mostra; **prazo** que muda o estado sozinho; **frequência** de atualização escolhida pelo usuário | espera: Busca (2ª). Relógio: tempo de sessão do Login (1ª); contagem regressiva da quarentena (2ª). Prazo: expiração aos 10 s do Login (1ª); fim da quarentena (2ª); nova inscrição em 2 s nos Dados ao vivo (2ª). Frequência: Dados ao vivo (2ª) |
| O3. Ciclo de vida | o que a interface abre (requisição, relógio, inscrição, ouvinte) fecha **com a tela** (limpeza ao sair da tela, ADR 0029) ou **com um estado** (o relógio vive enquanto a sessão vive; a pausa fecha a inscrição), e fica **uma só** depois de esconder e mostrar a tela | com a tela: Login, Quadro e Dados ao vivo (1ª); Busca e Formulário à espera da tcc-v4m7. Com um estado: sessão do Login; pausa dos Dados ao vivo (1ª); reconexão cancelada por pausar ou esconder (2ª). Uma só: Dados ao vivo, cenário 11 (1ª) |
| O4. Fonte de fora da interface | eventos que ninguém na tela pediu, combinados com os do usuário | a fonte que manda um lote por segundo: Dados ao vivo (1ª). A outra aba que grava o quadro: Quadro (1ª) |
| O5. Separação dos eventos | saber de onde veio cada evento e o que ele pode mudar: a alteração que o programa faz conta ou não como a do usuário, e duas fontes não interferem uma na outra | a escolha de uma sugestão muda o campo sem disparar busca: Busca (1ª). Editar não cancela a tentativa nem encerra a sessão: Login (1ª). Editar não cancela o envio: Formulário (1ª). O nome lembrado volta preenchido e já habilita o Entrar, sem o usuário digitar: Login (2ª). No Views, o *listener* dispara de novo quando o código altera o campo (ADR 0005) |
| O6. Falha e recuperação | o que a falha deixa na tela e como a interface volta a funcionar: a busca seguinte mostra as sugestões, o cartão volta à coluna de onde saiu, o painel se inscreve de novo na fonte | a busca seguinte funciona: Busca (1ª). A falha mantém os dados no formulário: envio do Formulário (1ª). A quarentena depois de três falhas seguidas: Login (2ª). O cartão volta se o servidor falhar: Quadro (2ª). A reconexão depois de queda: Dados ao vivo (2ª) |
| O7. Ação que espera a tela atualizar | uma ação que só funciona depois que a tela mudou, como mover o foco para um campo que acabou de aparecer | o foco no título do passo novo e no primeiro campo inválido: Formulário (2ª). Leitura nossa: os atalhos Ctrl+Z e Ctrl+Y do Quadro (2ª) pedem um ouvinte fora do componente, que também cai em O3 |

O1 e O6 se sobrepõem no cancelamento, que o ADR 0002 já registra no custo:
cada interface o faz com uma política diferente. O5 tem os dois sentidos:
na Busca, a alteração feita pelo programa não pode contar como a do
usuário; no nome lembrado do Login, tem de contar.

## Tipos de gerenciamento de estado

| Tipo | O que exige | Onde (rodada) |
|---|---|---|
| E1. Derivado de um valor | um valor calculado de outro, que o acompanha a cada alteração | o erro de cada campo do Formulário; o Entrar habilitado do Login; o destaque do palpite e a situação dos Dados ao vivo; a contagem de cada coluna do Quadro (1ª) |
| E2. Derivado de várias partes | um valor que lê várias partes da tela, ou uma restrição que vale para todas | o Reservar, que considera todos os erros; a volta não antes da ida, mostrada quando qualquer data foi tocada (Formulário, 1ª); o "Definir Status" das tarefas, desabilitado quando a coluna "Fazendo" enche (com a especificação da tcc-4v3f; hoje, os botões das outras colunas que levam a "Fazendo"); o resumo do cabeçalho (Quadro, 1ª); os pontos e o total do bolão, do palpite digitado e do placar que a fonte manda (Dados ao vivo, 2ª) |
| E3. Partes condicionais | uma parte aparece, fica habilitada ou conta conforme outro valor | a volta habilitada só em "Ida e volta" e o campo desabilitado que não conta para o Reservar (Formulário, 1ª); o passo do assistente (2ª) |
| E4. Estado de interação | o que o usuário já fez na tela, à parte dos dados | o "tocado" (Formulário, 1ª); o item ativo do *combobox* (Busca, 2ª); a última ação na situação do Quadro (1ª) |
| E5. Situação de uma operação | os estados pelos quais uma operação passa, cada um com a sua tela | Busca: vazia, "Buscando…", sugestões, nenhuma cidade, falha (1ª). Login: desconectado, conectando, conectado, falha (1ª); quarentena (2ª). Dados ao vivo: aguardando, com lotes, pausado (1ª); reconectando (2ª). Envio do Formulário: enviando, falha, confirmação (1ª); e-mail em validação (2ª) |
| E6. Estado compartilhado | partes da tela que leem e alteram o mesmo estado | o cabeçalho e as três colunas do Quadro (1ª) |
| E7. Lista e identidade dos itens | a lista na tela acompanha a lista no estado, item por item | as sugestões da Busca; as colunas, com a tarefa que muda de lista, no Quadro; as linhas dos jogos nos Dados ao vivo (1ª); a linha com palpite editável (2ª) |
| E8. Histórico | um valor que registra o que já aconteceu | o último termo e o destino que fica (Busca, 1ª); a confirmação até a próxima reserva (Formulário, 1ª); os gols novos desde o último lote mostrado, contados também durante a pausa (Dados ao vivo, 1ª); desfazer e refazer (Quadro, 2ª); as falhas seguidas (Login, 2ª) |
| E9. Estado salvo fora da interface | salvar, ler e validar o que fica fora da interface | o `localStorage`, com a validação ao abrir e o que outra aba grava (Quadro, 1ª); o nome lembrado (Login, 2ª); o servidor que confirma ou desfaz a mudança otimista (Quadro, 2ª) |

O reinício com a tela (mostrar começa do zero no Login e nos Dados ao
vivo, e abre o quadro salvo no Quadro) aparece nos dois eixos: o que se
fecha é O3, e o que volta ao valor inicial é estado. A tabela não o conta
à parte.

## Mapa por interface

| Interface | Orquestração (1ª) | Orquestração (2ª) | Estado (1ª) | Estado (2ª) |
|---|---|---|---|---|
| Formulário | O1 descarte, O5, O6 (envio, tcc-32dr, ainda fora do `spec.md`) | O1 sem política (e-mail), O7 (foco) | E1, E2, E3, E4, E8; E5 com o envio | E3 e E4 (passo), E5 (e-mail) |
| Busca | O1 substituição, O5, O6; O3 com a tela à espera da tcc-v4m7 | O2 espera | E5, E7, E8 | E4 (item ativo) |
| Login | O1 substituição, O2 relógio e prazo, O3 com a tela e com um estado, O5 | O2 relógio e prazo, O5, O6 (quarentena) | E1, E5 | E5, E8, E9 |
| Quadro | O3 com a tela, O4 (outra aba) | O1 fila, O6, O7 (atalhos, leitura nossa) | E1, E2, E4, E6, E7, E9 | E8, E9 |
| Dados ao vivo | O3 com a tela, com um estado e uma só, O4 (lotes) | O2 prazo e frequência, O3 com um estado, O6 | E1, E7, E8 | E2 (bolão), E7 |

## Cobertura por par

Interfaces de cada par pelo ADR 0029: Web Component, React e Solid têm as
cinco; o Lit, Formulário, Busca e Dados ao vivo; o Angular com *signals*,
Formulário, Busca e Quadro; Views × Compose, Formulário, Quadro e Dados ao
vivo; Windows Forms × WPF, Formulário, Quadro e Login. Cada célula diz a
interface que traz o tipo ao par; "—" é o tipo que o par não tem.

| Tipo | Web Component × Lit | Solid × Angular | Views × Compose | Windows Forms × WPF |
|---|---|---|---|---|
| O1 substituição | Busca | Busca | — | Login |
| O1 descarte | Formulário | Formulário | Formulário | Formulário |
| O1 fila | — | Quadro (2ª) | Quadro (2ª) | Quadro (2ª) |
| O2 espera | Busca (2ª) | Busca (2ª) | — | — |
| O2 relógio e prazo | Dados ao vivo (2ª, só prazo) | — | Dados ao vivo (2ª, só prazo) | Login |
| O2 frequência | Dados ao vivo (2ª) | — | Dados ao vivo (2ª) | — |
| O3 com a tela | Busca, Dados ao vivo | Busca, Quadro | Quadro, Dados ao vivo | Quadro, Login |
| O3 com um estado | Dados ao vivo | — | Dados ao vivo | Login |
| O4 fonte de fora | Dados ao vivo | Quadro | Quadro, Dados ao vivo | Quadro |
| O5 separação | Busca, Formulário | Busca, Formulário | Formulário | Login, Formulário |
| O6 falha | Busca, Formulário, Dados ao vivo (2ª) | Busca, Formulário, Quadro (2ª) | Formulário, Quadro (2ª), Dados ao vivo (2ª) | Formulário, Login (2ª), Quadro (2ª) |
| O7 ação que espera a tela | Formulário (2ª) | Formulário (2ª), Quadro (2ª) | Formulário (2ª), Quadro (2ª) | Formulário (2ª), Quadro (2ª) |
| E1 a E4 | Formulário | Formulário, Quadro | Formulário, Quadro, Dados ao vivo | Formulário, Quadro, Login |
| E5 situação | Busca, Dados ao vivo, Formulário | Busca, Formulário | Dados ao vivo, Formulário | Login, Formulário |
| E6 compartilhado | — | Quadro | Quadro | Quadro |
| E7 lista | Busca, Dados ao vivo | Busca, Quadro | Quadro, Dados ao vivo | Quadro |
| E8 histórico | Busca, Dados ao vivo, Formulário | Busca, Formulário, Quadro (2ª) | Dados ao vivo, Formulário, Quadro (2ª) | Formulário, Login (2ª), Quadro (2ª) |
| E9 salvo fora | — | Quadro | Quadro | Quadro, Login (2ª) |
| Tipos que faltam | O1 fila, O2 relógio, E6, E9 | O2 relógio, prazo e frequência, O3 com um estado | O1 substituição, O2 espera e relógio | O2 espera e frequência |

Leitura nossa, a conferir quando o autor fixar os tipos:

- ao Windows Forms × WPF falta só o tempo da Busca e dos Dados ao vivo, e
  o Login lhe dá a substituição, o relógio, o prazo e o ciclo de vida preso a um
  estado;
- o Web Component × Lit tem toda a orquestração que a web tem, menos a
  fila, e no estado só o Formulário pesa; o par isola a ligação do estado
  com a tela (`docs/delineamento.md`, seção "O que um par isola"), e o
  estado compartilhado fica sem esse contraste;
- o Solid × Angular tem o estado do Formulário e do Quadro e a substituição da
  Busca, mas nenhum relógio nem ciclo de vida preso a um estado; com a
  ordem de corte do ADR 0029, perde primeiro a fila e depois E6 e E9;
- o Views × Compose cobre o estado nas três interfaces, e a substituição só
  entra se a validação do e-mail a adotar (tcc-k9i2).

## Lacunas nas especificações

Levantadas em 2026-10-15.

- O envio que ignora o reenvio está decidido para a primeira rodada
  (ADRs 0002 e 0005), mas não está no `spec.md` do Formulário; é a
  tcc-32dr, aberta, que bloqueia a segunda rodada do Formulário
  (tcc-k9i2).
- A Busca e o Formulário não têm o requisito "Limpeza ao sair da tela",
  que o ADR 0029 pede a todas as interfaces; é a tcc-v4m7, aberta.
- A validação do e-mail da segunda rodada não diz o que acontece com a
  resposta de um e-mail que o usuário já mudou, nem se a validação espera
  a última tecla; a política decide se ela traz a substituição ao Formulário.
