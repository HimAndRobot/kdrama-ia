# Policy Signal System

## Objetivo

As políticas ativas não devem nascer com peso alto por chute do modelo.

O peso deve ser derivado de sinais acumulados da conversa e da execução.

## Regra principal

Toda política nasce com:

- `weight = 0.0`

O valor cresce ou cai aos poucos conforme sinais locais, sem depender de prompt extra.

## Sinais

### Explicit set

O usuário criou a regra.

Efeito inicial:

- cria a política
- `delta = 0.0`

### Explicit reinforce

O usuário repetiu ou reforçou a mesma regra.

Exemplo:

- "usa o MDL"
- "lembra de usar o MDL"

Delta sugerido:

- `+0.15`

### Explicit correction

O agente falhou e o usuário corrigiu a regra.

Exemplo:

- "só na primeira mensagem"
- "não é para repetir isso"

Delta sugerido:

- `+0.20`

### Successful apply

A política foi aplicada e não houve reclamação imediata.

Delta sugerido:

- `+0.03`

### Violation

A política existia e o agente a descumpriu de forma explícita.

Delta sugerido:

- `+0.20`

Observação:

Esse sinal não aumenta por "mérito", aumenta por urgência operacional.

### Stale decay

A política ficou muito tempo sem uso ou sem reforço.

Delta sugerido:

- `-0.02`

### Downgrade

O usuário afrouxou uma regra.

Exemplo:

- "não precisa repetir sempre"
- "não precisa ser toda hora"

Delta sugerido:

- `-0.08`

## Clamp

O peso sempre fica em:

- `0.0 <= weight <= 1.0`

Isso evita crescimento infinito e deixa o sistema convergir.

## Slots

Políticas não devem ser acumuladas sem controle.

Cada política precisa ter:

- `policy_slot`

Exemplos:

- `response_opening_style`
- `drama_research_source_priority`
- `review_source_bias`

O slot permite:

- substituir
- revisar
- desativar
- reforçar

sem criar outra política redundante.

## Eventos persistidos

Além da política atual, o sistema deve persistir:

- `policy_signal_events`

Com isso, o peso final deixa de ser uma caixa-preta.

## Review queue

Quando uma política:

- chega em `0.0`
- fica muito tempo sem uso
- entra em conflito
- ou fica ambígua

ela pode entrar em:

- `policy_review_queue`

Essa fila não entra no loop principal.

Ela serve para o runtime perguntar ao usuário em momento oportuno:

- se a regra ainda vale
- se deve ser removida
- se deve ser atualizada

## Relação com sugestões futuras

O mesmo mecanismo de fila serve depois para:

- sugestão de assunto
- sugestão de notícia acompanhada
- sugestão de follow-up
- sugestão de revisão de regra

Ou seja:

o sistema de peso foi desenhado para virar infraestrutura de sugestões no futuro, sem quebrar a base atual.
