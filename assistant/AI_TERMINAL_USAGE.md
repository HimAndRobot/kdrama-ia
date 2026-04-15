# Uso do Assistente via Terminal por outra IA

Este documento ensina uma IA externa a usar o assistente pelo terminal como usuário final.

A IA externa deve apenas conversar com o assistente e relatar o comportamento observado. Ela nao deve analisar código, banco, logs, debug ou arquivos internos.

## Iniciar

Execute:

```bash
cd /Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/assistant
PYTHONPATH=src python3 -m assistant_app
```

Quando o assistente abrir, digite mensagens normalmente no prompt:

```text
>
```

## Encerrar

Para sair, use:

```text
/quit
```

Prefira `/quit` em vez de `Ctrl+C`, porque ele permite finalizar tarefas internas antes de encerrar.

## Comandos disponíveis

```text
/help
/session
/quit
```

Use apenas esses comandos operacionais. Nao use comandos internos de memória, política, debug ou inspeção técnica.

## Como relatar

Depois de usar o assistente, relate apenas:

- o que foi dito ao assistente;
- o que o assistente respondeu;
- qual comportamento pareceu correto ou incorreto;
- se o comportamento mudou depois de fechar e abrir o terminal.

Nao explique causas técnicas. A análise técnica será feita pelos mantenedores do projeto.
