# Tasks

## 1. Teste de conformidade e especificação viva

- [ ] 1.1 Conferir na verificação "1 abre com o quadro inicial" o quadro
  inicial gravado no `localStorage`, e trocar o `localStorage.clear()` da
  limpeza em outra aba por `localStorage.removeItem("quadro")`; verificar
  rodando o teste nas quatro implementações.
- [ ] 1.2 Arquivar a mudança no mesmo commit do teste
  (`npm run openspec -- archive conferir-gravacao-ao-abrir-do-quadro
  --yes`); verificar com `npm run conferir-especificacao`, que tem de
  passar com 25 cenários no Quadro.

## Workflow follow-up

- Nenhuma implementação muda: as quatro já gravam ao abrir e passam no
  teste de conformidade.
