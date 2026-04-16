---
name: playwright-browser
description: Usa o browser e o motor de busca configurado para consultar a web, abrir páginas e montar artefatos de links e conteúdo. Depois de search ou navigate, o fluxo normal deve continuar com operações sobre o artefato atual, como filter_links, search_artifact, get_chunks ou list_hosts, em vez de repetir navigate sem ganho novo.
---

# Playwright Browser

Skill de browser para busca, navegação e extração de links e conteúdo.

Regras de uso:

- `search` serve para descoberta geral e cria um artefato de links e conteúdo.
- `navigate` serve para abrir uma URL específica e criar um artefato de links e conteúdo da página.
- Depois que já existir artefato neste turno, o normal é continuar com operações sobre esse artefato:
  - `filter_links`
  - `search_artifact`
  - `get_chunks`
  - `list_hosts`
- Não repita `navigate` sem ganho novo claro.
- Se a página certa já foi aberta, prefira consultar o artefato atual em vez de abrir a mesma página de novo.
