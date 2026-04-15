# Storage And Data Contracts

## Objetivo

Definir armazenamento pensando em evolução, não em gambiarra local.

## Camadas de persistência

### 1. Session transcript

Sugestão:

- JSONL por sessão

Conteúdo:

- user messages
- assistant messages
- tool invocations
- tool results
- system checkpoints

### 2. Memory store

Sugestão inicial:

- SQLite

Tabelas lógicas:

- `memory_items`
- `memory_evidence`
- `active_policies`
- `policy_signal_events`
- `policy_review_queue`
- `entities`
- `session_summaries`
- `skill_runs`

### 3. Domain state

Para o domínio de recomendação:

- `seen_titles`
- `rejected_titles`
- `saved_titles`
- `recommendation_feedback`

Esses podem ser projeções derivadas da memória principal, não fontes separadas no longo prazo.

## Contratos principais

### memory_items

- `id`
- `memory_type`
- `scope`
- `subject`
- `value_json`
- `confidence`
- `temporal_weight`
- `status`
- `created_at`
- `updated_at`
- `expires_at`

### memory_evidence

- `id`
- `memory_item_id`
- `session_id`
- `turn_id`
- `snippet`
- `source_kind`
- `created_at`

### session_summaries

- `id`
- `session_id`
- `summary_kind`
- `summary_text`
- `created_at`

### active_policies

- `id`
- `policy_type`
- `policy_slot`
- `instruction`
- `applies_to_json`
- `priority`
- `active`
- `revision_count`
- `explicit_set_count`
- `explicit_reinforce_count`
- `explicit_correction_count`
- `successful_apply_count`
- `violation_count`
- `stale_decay_count`
- `last_signal_type`
- `created_at`
- `updated_at`

### policy_signal_events

- `id`
- `policy_slot`
- `signal_type`
- `delta`
- `evidence_json`
- `created_at`

### policy_review_queue

- `id`
- `policy_slot`
- `reason`
- `status`
- `suggested_prompt`
- `created_at`
- `updated_at`

### skill_runs

- `id`
- `session_id`
- `skill_id`
- `input_json`
- `output_json`
- `status`
- `started_at`
- `finished_at`

## Índices importantes

- por `subject`
- por `memory_type`
- por `updated_at`
- por `expires_at`
- por `session_id`

## Estratégia de evolução

Fase inicial:

- transcript em JSONL
- memória em SQLite

Fase posterior:

- embeddings para recall semântico
- índices híbridos
- cache de resumo por sessão
