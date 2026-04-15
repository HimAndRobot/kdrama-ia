# Memory Model

## Problema

Memória boa não é só salvar "gosta" e "não gosta".

Se o sistema salvar de forma rígida:

- "não quer romance fofo"

isso vira erro quando a preferência era só daquele momento.

## Modelo proposto

A memória será separada em camadas.

## 1. Transcript

É o histórico bruto da conversa.

Função:

- auditoria
- reconstrução parcial de contexto
- matéria-prima para extrações

Não deve ser tratado como memória pronta.

## 2. Episodic memory

Memória de episódios e eventos recentes.

Exemplos:

- pediu recomendações com foco em mistério
- comentou que já viu determinado drama
- rejeitou uma sugestão hoje

Características:

- tem timestamp forte
- vale mais perto do momento em que foi dita
- pode perder força com o tempo

## 3. Semantic memory

Memória consolidada e mais abstrata.

Exemplos:

- costuma preferir suspense acima de romance
- valoriza trama movida por mistério real
- tende a rejeitar romance como motor principal

Características:

- deriva de vários episódios
- não nasce de uma única mensagem
- precisa de score de confiança

## 4. Catalog memory

Memória factual de entidades.

Exemplos:

- já viu `Signal`
- abandonou `True Beauty`
- salvou `Mouse` para depois

Características:

- alta utilidade prática
- alta importância para recomendação
- política de deduplicação clara

## 5. Working memory

Estado curto da conversa atual.

Exemplos:

- está comparando thrillers escolares
- quer resultados com reviews do Reddit
- quer fontes externas para consolidar a resposta

Essa memória não precisa virar persistência longa sempre.

## 6. Active policy memory

Não é memória recuperável comum.

É uma camada de regras ativas do agente.

Exemplos:

- iniciar a primeira mensagem com determinada fórmula
- evitar certa expressão
- priorizar MDL em pesquisas de drama

Características:

- vive separada de preferência e identidade
- precisa de `policy_slot`
- suporta revisão, reforço, downgrade e desativação
- o peso não nasce do modelo; nasce de sinais acumulados

## Estrutura de cada fato

Cada item de memória deve carregar:

- `type`
- `subject`
- `value`
- `source`
- `evidence`
- `confidence`
- `temporal_weight`
- `first_seen_at`
- `last_seen_at`
- `status`

## Classes recomendadas

### Durable fact

Ex.: já viu um título específico.

### Stable preference

Ex.: costuma gostar de suspense psicológico.

### Temporary preference

Ex.: hoje quer algo leve ou sem romance.

### Active constraint

Ex.: nesta conversa não repetir títulos já citados.

### Pending ambiguity

Ex.: não ficou claro se o usuário viu ou só ouviu falar.

## Regras de consolidação

1. Uma única fala não deveria virar preferência estável sem evidência extra.
2. Preferência temporária deve expirar ou perder peso.
3. "Já vi" deve ter alta prioridade na prevenção de recomendações repetidas.
4. Contradições não apagam o passado; elas criam nova evidência.
5. Resumo de memória deve ser derivado, não manualmente improvisado pelo agente principal.

## Aplicação ao seu caso

Quando o usuário diz:

- "já vi esse"

isso entra como `catalog_memory.seen = true`

Quando diz:

- "não quero romance fofo"

isso entra primeiro como `temporary_preference`

Só depois de repetição ou padrão vira `stable_preference`.
