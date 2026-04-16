---
name: conversation-history
title: Conversation History
description: Consulta conversas anteriores por ordem, dia ou proximidade textual, e pode abrir ou resumir uma conversa passada com foco em um tema/frase.
---

# Conversation History

Use esta skill quando o usuário pedir para lembrar, localizar, abrir ou resumir uma conversa anterior.

Capacidades principais:

- `list_conversations`
  - lista conversas anteriores por ordem (`recent` ou `oldest`)
  - aceita filtro opcional por `day`

- `search_conversations`
  - busca conversas por frase, termos soltos ou tags livres
  - usa proximidade textual no corpus de transcript
  - aceita filtro opcional por `day`

- `read_conversation`
  - abre uma conversa específica
  - aceita `session_id`, `session_key` ou `ordinal`
  - retorna um recorte de mensagens

- `summarize_conversation`
  - faz um resumo focado numa frase/tema
  - pode mirar uma conversa específica
  - ou escolher a melhor conversa encontrada pela `query`

Boas práticas:

- Use `list_conversations` quando o usuário souber “foi a conversa anterior / a de ontem / a terceira mais recente”.
- Use `search_conversations` quando o usuário lembrar do assunto, site, drama, nome ou tags.
- Use `read_conversation` quando você já souber qual conversa abrir.
- Use `summarize_conversation` quando o usuário quiser “me lembra o que falamos sobre X”.
