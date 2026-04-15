# Background Extraction And Reflection

## Problema

Não dá para depender de "fim da conversa" para extrair memória.

Conversa real:

- para
- volta
- muda de assunto
- reabre contexto antigo

Então a extração precisa existir como processo assíncrono.

## Objetivo

Rodar em segundo plano sem travar a resposta principal e sem exigir um marcador artificial de término.

## Componentes

### 1. Turn extractor

Roda após cada turno concluído.

Extrai candidatos como:

- fatos explícitos
- títulos vistos
- títulos rejeitados
- preferências temporárias
- intenção operacional da conversa
- políticas ativas candidatas

### 2. Memory classifier

Classifica o candidato em:

- durável
- temporário
- ambíguo
- irrelevante

### 3. Consolidator

Mescla fatos novos com fatos antigos.

Exemplos:

- reforça preferência existente
- reduz peso de preferência antiga
- evita duplicata
- registra contradição

### 4. Reflection worker

Job menos frequente, mais caro, para:

- detectar padrões
- reclassificar preferências
- gerar resumos de período
- consolidar semantic memory

### 5. Policy signal worker

Job barato, local, sem prompt extra para:

- registrar reforço
- registrar correção
- registrar uso bem-sucedido
- aplicar decay leve
- alimentar fila de revisão

## Triggers propostos

### Trigger por turno

Sempre que um turno fecha:

- enqueue de extração leve

### Trigger por idle

Se a conversa ficou parada por X minutos:

- consolidar working memory
- gerar nota curta da sessão

### Trigger por reset

Ao resetar:

- gerar resumo de sessão
- salvar episodic memory

### Trigger por compaction

Antes da compaction:

- flush de fatos importantes

### Trigger periódico

Cron:

- reavaliar preferências
- consolidar padrões
- reduzir peso de fatos temporários antigos

## Regra principal

Background workers nunca devem escrever memória cega. Toda promoção precisa ter:

- evidência
- score
- tipo de memória compatível

Para políticas ativas:

- o peso deve vir de sinais acumulados
- não de um número inicial alto vindo do modelo

## Relação com OpenClaw

O paralelo mais próximo é:

- active memory antes da resposta
- hooks internos
- memory flush antes de compaction
- reflection/feedback em background

Esse é o modelo que vale a pena copiar conceitualmente.
