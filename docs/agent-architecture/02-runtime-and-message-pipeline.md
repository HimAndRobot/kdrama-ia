# Runtime And Message Pipeline

## Ideia central

Seguindo o modelo conceitual do OpenClaw, a resposta do agente não deve nascer direto do texto do usuário. Cada mensagem passa por um pipeline.

## Pipeline proposto

```text
user message
-> session load
-> recent context load
-> active memory recall
-> skill planning / tool policy
-> model response loop
-> tool execution
-> final answer
-> background extraction
-> memory/store updates
```

## Etapas

### 1. Session load

Carregar:

- transcript recente da sessão
- estado operacional da sessão
- últimos fatos já extraídos

Mesmo com um único usuário, a sessão continua importante porque:

- permite continuidade
- permite compaction depois
- evita depender de janela infinita de contexto

### 2. Recent context load

Trazer apenas uma cauda útil do transcript bruto:

- últimas N mensagens
- últimos resultados de tools
- pendências abertas

### 3. Active memory recall

Executar uma etapa separada antes da resposta principal:

- buscar fatos e preferências relevantes
- priorizar fatos recentes quando forem preferências temporárias
- priorizar fatos duráveis quando forem históricos fortes

Saída:

- um pacote de memória resumido
- nunca o banco bruto inteiro

### 4. Skill planning

Decidir:

- responder só com contexto atual
- usar busca local
- usar busca web
- usar skill especializada

### 5. Model response loop

Loop de agente:

- o modelo decide se precisa de skill/tool
- ferramenta roda
- resultado entra no contexto
- modelo conclui resposta

### 6. Background extraction

Depois da resposta, uma fila assíncrona processa:

- fatos novos
- mudanças de preferência
- novas entidades vistas
- possíveis resumos para memória diária

### 7. Memory/store update

Persistir atualizações sem travar a UX principal.

## Regras importantes

1. A conversa principal não deve esperar consolidação profunda.
2. Background extraction não deve reescrever fatos fortes sem evidência nova.
3. Recall não deve despejar tudo no prompt.
4. Skills devem operar por política declarada, não por improviso.

