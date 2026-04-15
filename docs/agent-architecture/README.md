# Agent Architecture

Este diretório define a base arquitetural do agente que queremos construir a partir deste projeto.

Objetivo:

- ter um agente conversacional único, persistente e expansível
- permitir memória útil sem congelar preferências como se fossem permanentes
- suportar skills/plugins e integrações privadas no futuro
- rodar extrações e consolidação em segundo plano
- manter uma separação clara entre conversa, memória, automações e capacidades externas

Princípios:

1. O agente não "lembra" magicamente. Ele lê contexto persistido e memória derivada.
2. O transcript bruto não é memória. Ele é a matéria-prima para extrações.
3. Preferências do usuário têm peso temporal. O que vale hoje pode não valer amanhã.
4. Skills são capacidades isoladas, com contrato, permissões e política de uso.
5. Background jobs existem para consolidar contexto sem bloquear a conversa principal.
6. A base precisa ser útil primeiro para recomendação conversacional, mas com desenho genérico.

Documentos:

- [01-product-scope.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/01-product-scope.md)
- [02-runtime-and-message-pipeline.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/02-runtime-and-message-pipeline.md)
- [03-memory-model.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/03-memory-model.md)
- [04-skills-and-integrations.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/04-skills-and-integrations.md)
- [05-background-extraction-and-reflection.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/05-background-extraction-and-reflection.md)
- [06-storage-and-data-contracts.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/06-storage-and-data-contracts.md)
- [07-roadmap.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/07-roadmap.md)
- [08-runtime-topology.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/08-runtime-topology.md)
- [09-terminal-first-deliverable.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/09-terminal-first-deliverable.md)
- [10-policy-signal-system.md](/Users/geanpedro/Documents/GitHub/pessoal/kdrama-ia/docs/agent-architecture/10-policy-signal-system.md)

Decisão estrutural inicial:

- vamos assumir um único usuário
- não vamos assumir preferências permanentes
- vamos tratar "gosto", "não gosto", "já vi", "talvez quero agora" e "restrições do momento" como tipos diferentes de memória
- vamos projetar skills para pesquisa web, fontes públicas, fontes privadas autorizadas e integrações internas

Restrição importante:

- esta arquitetura pode suportar pesquisa web e conectores privados autorizados
- ela não deve incluir skill voltada a pirataria, evasão de paywall, busca de conteúdo ilegal ou distribuição não autorizada
