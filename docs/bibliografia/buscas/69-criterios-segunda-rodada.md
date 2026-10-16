# Critérios da triagem (segunda rodada, tcc-n73z, 2026-10-02)

Contexto: TCC que compara três notações de coordenação para programar interfaces
gráficas (imperativa com callbacks, declarativa por re-renderização como React,
reativa fina com signals como Solid/Angular signals) implementando os mesmos
cinco casos (contador, formulário com validação, busca com sugestões, lista
filtrável, carrinho) em várias tecnologias web (Web Component, jQuery, React,
Solid, Angular) e no Android (Views, Compose), e as avalia pelas Dimensões
Cognitivas de Notações (DCs, Green & Petre 1996).

Perguntas da revisão: (P1) abordagens de PR/PFR para GUIs desde 2016;
(P2) evidência empírica sobre compreensão/usabilidade de PR/PF/declarativo
versus callbacks/Observer/imperativo; (P3) DCs aplicadas a APIs, linguagens,
bibliotecas, notações.

INCLUIR (revisado por pares, inglês ou português, título e resumo tratam de):
 I1. PR, PFR, signals, dataflow ou UI declarativa para GUIs, web front-end ou
     apps móveis (React, Elm, Solid, Svelte, Vue, Angular, Compose, SwiftUI,
     Flutter, RxJS, MobX...).
 I2. Estudo empírico (experimento, estudo com usuários, análise de código) de
     compreensão, usabilidade, manutenção ou defeitos de PR/PF/declarativo vs
     callbacks/Observer/imperativo, ou de frameworks de UI.
 I3. Avaliação pelas DCs (ou DCs + outro método) de linguagem, API, biblioteca
     ou notação textual de programação, especialmente se compara notações nos
     mesmos problemas.
 I4. Survey, revisão sistemática ou mapeamento de PR, PFR ou de frameworks de UI.
 I5. Comparação de várias tecnologias de UI implementando as mesmas tarefas.
EXCLUIR: "reactive" de outras áreas sem GUI (redes, robótica, IoT, sistemas
 distribuídos, bancos de dados, hardware, sistemas embarcados de controle),
 a menos que seja I4; DCs aplicadas só a ferramentas visuais de usuário final,
 visualização, música, educação infantil, modelagem UML etc. sem relação com
 notações de programação textual (marcar E-DC-outra); semântica/teoria de PFR
 sem GUI (E-teoria); preprint com versão revisada; tese/livro sem relação.

NICHO (marque com NICHO e explique em uma frase, mesmo se o resto for excluído):
 N1. Análise pelas DCs de React, hooks, Elm, signals (Solid, Angular, Preact,
     Vue, Svelte), Compose/SwiftUI/Flutter ou de qualquer biblioteca de PR/PFR.
 N2. Comparação, nos mesmos casos/tarefas, de duas ou mais das três notações
     (imperativa com callbacks; declarativa por re-renderização; reativa fina
     com signals), por qualquer método.
 N3. Survey/revisão de PR revisada por pares publicada depois de 2013.
