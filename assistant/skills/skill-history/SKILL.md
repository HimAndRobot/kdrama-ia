---
name: skill-history
title: Skill History
description: Consulta as últimas skills executadas na sessão atual para recuperar chamadas, parâmetros e um resumo curto do que aconteceu.
---

# Skill History

Use esta skill quando for necessário revisar rapidamente quais skills já foram chamadas, com quais parâmetros e qual foi o resumo curto do resultado.

Operações principais:

- `last_skill_calls`
  - retorna as últimas skill calls da sessão atual
  - útil para evitar repetir a mesma chamada sem necessidade
  - útil para recuperar o contexto operacional de turns anteriores
