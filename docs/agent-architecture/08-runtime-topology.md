# Runtime Topology

## Decisão

A primeira superfície do agente será **terminal**, não web.

Mas o runtime não deve nascer acoplado ao terminal. O terminal será apenas o
primeiro adapter de entrada e saída.

## Referências usadas

- `reference/codex/`
- `reference/openclaw/`

## O que cada referência ensina

### Codex

O `codex` é a referência para:

- experiência interativa de terminal
- sessão retomável
- fluxo de chat no terminal
- composer de entrada
- UI local, rápida, centrada em REPL/TUI

Pontos observados:

- CLI principal em `reference/codex/codex-rs/cli/src/main.rs`
- TUI própria em `reference/codex/codex-rs/tui/`
- documentação de composer em `reference/codex/docs/tui-chat-composer.md`

### OpenClaw

O `openclaw` é a referência para:

- runtime persistente
- sessões
- memória
- background jobs
- adapters de superfície/canais

Pontos observados:

- runtime e bootstrap em `reference/openclaw/docs/concepts/agent.md`
- sessões em `reference/openclaw/docs/concepts/session.md`
- jobs em segundo plano em `reference/openclaw/docs/automation/cron-jobs.md`

## Arquitetura alvo

```text
surface adapter
(terminal agora; telegram/app/voice depois)
-> runtime api
-> session manager
-> memory system
-> skill runner
-> background jobs
-> storage
```

## Regra estrutural

O cérebro do agente não sabe se a mensagem veio do terminal, Telegram ou áudio.

Ele só recebe um envelope normalizado:

- `session_key`
- `message_id`
- `surface`
- `content`
- `attachments`
- `timestamp`
- `metadata`

## Módulos

### `surfaces/terminal`

Responsável por:

- input do usuário
- render incremental
- histórico visual local
- atalhos e comandos do terminal

Não deve:

- implementar memória
- decidir skills
- persistir lógica de sessão por conta própria

### `runtime/`

Responsável por:

- receber a mensagem normalizada
- carregar contexto
- rodar recall
- acionar loop do agente
- publicar eventos de stream
- fechar o turno

### `sessions/`

Responsável por:

- criar/continuar sessão
- transcript
- resumos
- estado operacional da conversa

### `memory/`

Responsável por:

- recall pré-resposta
- extração pós-turno
- consolidação em background

### `skills/`

Responsável por:

- registry
- contrato
- roteamento
- execução

### `jobs/`

Responsável por:

- extração assíncrona
- consolidação/reflection
- cron futuro

### `storage/`

Responsável por:

- transcript
- SQLite
- índices futuros

## Escolha prática agora

Vamos construir:

1. runtime central primeiro
2. adapter de terminal em cima dele
3. Telegram depois
4. áudio/app depois

## O que fica preparado desde já

- envelope de mensagem neutro por superfície
- evento de stream neutro por superfície
- sessão persistente fora da UI
- skills fora da UI
- jobs fora da UI

