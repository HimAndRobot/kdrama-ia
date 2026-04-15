# Terminal-First Deliverable

## Objetivo deste entregável

Definir o primeiro corte implementável do sistema para validar a base antes de
qualquer expansão para Telegram, web ou áudio.

## O que este primeiro corte precisa provar

1. o agente funciona no terminal
2. a sessão persiste entre execuções
3. a memória já existe como sistema separado
4. a interface é só uma superfície, não o núcleo
5. o projeto está pronto para ganhar skills e background jobs

## Escopo do primeiro corte

### Entra

- terminal chat interativo
- runtime único
- session manager
- transcript persistente
- memory store inicial
- recall simples antes da resposta
- skill registry mínimo
- queue de jobs para pós-turno

### Não entra

- Telegram ainda
- áudio ainda
- UI web ainda
- embeddings ainda
- reflection profunda ainda

## UX mínima do terminal

Inspirada no `codex`, mas menor.

### Layout

- cabeçalho curto com nome da sessão
- área de output incremental
- área de input
- status line simples

### Precisa ter

- envio de mensagem
- streaming de resposta
- exibição de tool calls
- indicação de atividade do runtime
- comando para resetar sessão
- comando para inspecionar memória/sessão

### Não precisa ter no primeiro corte

- alternate screen sofisticada
- popups
- file picker
- image paste
- editor externo

## Contrato entre terminal e runtime

### Input para o runtime

```json
{
  "session_key": "main",
  "surface": "terminal",
  "text": "quero um thriller escolar",
  "attachments": [],
  "metadata": {}
}
```

### Eventos do runtime para o terminal

- `run_started`
- `memory_recall_started`
- `memory_recall_finished`
- `assistant_delta`
- `tool_call_started`
- `tool_call_finished`
- `run_finished`
- `run_failed`

## Estrutura de diretórios proposta para iniciar

```text
src/
  runtime/
  sessions/
  memory/
  skills/
  jobs/
  storage/
  surfaces/
    terminal/
```

## Critério de aceite

O primeiro corte está aceito quando:

1. eu consigo abrir o terminal do agente
2. mandar uma mensagem
3. fechar o processo
4. abrir de novo
5. continuar a mesma sessão
6. ver que um fato simples já foi lembrado

## Decisão de implementação

Se este entregável for aprovado, a ordem de execução recomendada é:

1. `storage`
2. `sessions`
3. `memory`
4. `runtime`
5. `surfaces/terminal`
6. `skills`
7. `jobs`

