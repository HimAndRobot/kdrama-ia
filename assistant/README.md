# Assistant

Primeiro corte implementável do agente terminal-first.

## Objetivo

Validar a base arquitetural:

- terminal como primeira superfície
- sessão persistente
- transcript separado da memória
- recall antes da resposta
- skills mínimas
- jobs em background para extração

## Estrutura

```text
assistant/
  README.md
  pyproject.toml
  src/assistant_app/
    __init__.py
    __main__.py
    cli.py
    config.py
    contracts.py
    runtime/
    sessions/
    memory/
    skills/
    jobs/
    storage/
    llm/
```

## Como rodar

```bash
cd assistant
PYTHONPATH=src python3 -m assistant_app
```

## Comandos no terminal

- `/help`
- `/reset`
- `/session`
- `/memory`
- `/policies`
- `/quit`

## Observações

- este primeiro corte funciona sem dependências externas
- o caminho principal é `CodexProvider`, reaproveitando `~/.codex/auth.json` como o OpenClaw faz
- não precisa de `OPENAI_API_KEY` para o fluxo principal
- se não houver auth local do Codex, ele tenta `OPENAI_API_KEY`
- sem auth nenhum, cai para um responder local simples para validar a arquitetura
- se existir auth do Codex e ela estiver quebrada, o terminal falha de forma explícita em vez de esconder o problema com fallback silencioso
- logs locais de debug ficam em `.assistant-data/debug/`
