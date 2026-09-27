---
title: Escrever o script que conta as linhas de cada implementação
status: todo
type: task
priority: normal
created_at: 2026-09-27T02:17:00Z
updated_at: 2026-09-27T02:17:00Z
---

ADR 0012: apoio à concisão. Conta as linhas não vazias e sem comentários de cada implementação (`casos/<caso>/<tecnologia>/`), fora o domínio compartilhado (`dominio.ts`, `dominio-kotlin/`), o estilo (`estilo.css` e os arquivos de estilo do Android), a configuração do projeto e os testes; no Angular, o *template* soma com a classe. Versionado no repositório, com o critério no cabeçalho, como `docs/jetbrains-deveco-2025-android.py`.

Pronto quando: o script imprime uma tabela caso × tecnologia para as 30 implementações web e as 6 do Android, e o texto pode citar o comando que a gera.

Origem: ADR 0012.
