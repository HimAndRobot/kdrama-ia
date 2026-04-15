# Roadmap

## Fase 0: Arquitetura

Entregas:

- documentação da base
- definição de pipeline
- definição de storage
- definição de skill contract

## Fase 1: Session Foundation

Objetivo:

- sessão persistente única
- transcript confiável
- histórico recuperável

Entregas:

- session manager
- transcript writer/reader
- tail loader para contexto recente

## Fase 2: Memory Foundation

Objetivo:

- memória separada do transcript

Entregas:

- schema de memória
- extractor leve pós-turno
- recall básico antes da resposta

## Fase 3: Domain Intelligence

Objetivo:

- agente recomendador realmente útil

Entregas:

- rastreamento de títulos vistos
- restrições de recomendação
- perfis temporários vs estáveis
- perguntas de desambiguação

## Fase 4: Skills Layer

Objetivo:

- tornar o agente expansível

Entregas:

- registry de skills
- skills locais de catálogo
- skill de web research
- skill de fontes específicas como Reddit
- skill contract + permission model

## Fase 5: Background Intelligence

Objetivo:

- consolidar memória sem bloquear conversa

Entregas:

- queue de jobs
- extractor assíncrono
- consolidator
- reflection worker

## Fase 6: Private Integrations

Objetivo:

- plugar serviços do homelab

Entregas:

- adapter framework para serviços privados
- secrets/config separados
- skill privada de ingestão/registro

## Fase 7: Advanced Recall

Objetivo:

- melhorar qualidade de memória

Entregas:

- embeddings
- busca híbrida
- re-ranking
- summaries por tema

## Critérios de sucesso da base

1. O agente sabe que um título já foi visto.
2. O agente distingue preferência temporária de estável.
3. O agente usa memória antes de responder.
4. O agente suporta adicionar skill nova sem refatorar tudo.
5. O agente consegue evoluir para integrações privadas.

