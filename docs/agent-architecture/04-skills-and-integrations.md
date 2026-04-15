# Skills And Integrations

## Objetivo

O agente deve ser expansível. A base não pode depender de ferramentas embutidas diretamente no prompt principal.

## Conceito de skill

Uma skill é uma capacidade isolada com:

- nome
- descrição
- política de uso
- contrato de entrada
- contrato de saída
- permissões
- estratégias de fallback

## Categorias de skill

### 1. Domain skills

Ligadas ao domínio atual.

Exemplos:

- `kdrama_catalog_search`
- `kdrama_review_lookup`
- `kdrama_seen_tracker`

### 2. Web research skills

Pesquisa externa.

Exemplos:

- `web_search_general`
- `reddit_discussion_search`
- `review_source_aggregator`

### 3. Private integration skills

Serviços seus, internos ou self-hosted.

Exemplos:

- `private_media_ingest`
- `homelab_video_register`
- `private_index_lookup`

### 4. Meta skills

Capacidades auxiliares do próprio agente.

Exemplos:

- `memory_extract`
- `memory_recall`
- `conversation_summarize`

## Contrato mínimo

Cada skill deve declarar:

- `id`
- `version`
- `purpose`
- `when_to_use`
- `when_not_to_use`
- `inputs_schema`
- `outputs_schema`
- `permission_level`
- `side_effects`

## Política de seleção

O agente principal não escolhe skill só por keyword. A escolha considera:

- intenção do usuário
- contexto da sessão
- custo/latência
- permissão
- confiabilidade da fonte

## Capacidades que entram na base

### Devem entrar

- busca local
- leitura de memória
- busca web pública
- busca em fontes específicas como Reddit quando o usuário pedir
- integração com serviços privados autorizados

### Não devem entrar

- skill focada em pirataria
- coleta de links ilegais
- evasão de paywall
- distribuição não autorizada de mídia

Isso não impede um sistema robusto de pesquisa. Só define que a skill layer precisa ser compatível com uso legítimo e com integrações privadas autorizadas.

## Estratégia de expansão

Fase 1:

- skills implementadas no código do projeto

Fase 2:

- registry local de skills
- manifesto por skill

Fase 3:

- carregamento dinâmico
- permissões por skill
- health checks por integração

