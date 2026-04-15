# Product Scope

## Visão

O produto desejado não é só um recomendador de K-drama. É um agente pessoal com quem o usuário conversa ao longo do tempo e que:

- mantém continuidade entre conversas
- aprende preferências sem assumir que são permanentes
- sabe o que já foi visto, rejeitado, salvo ou deixado para depois
- faz perguntas de desambiguação quando falta contexto
- usa habilidades externas para pesquisar, consolidar e responder melhor

## Escopo inicial

O primeiro domínio continua sendo entretenimento e recomendação, com foco em:

- K-dramas
- reviews e recomendações
- preferências narrativas
- histórico do que o usuário já viu

Mas a base deve servir depois para:

- pesquisa geral na internet
- consolidação de links e fontes autorizadas
- integrações privadas
- automações pessoais

## O que o agente precisa saber distinguir

1. Fato durável
   Ex.: "já vi *Signal*"

2. Preferência estável
   Ex.: "costumo gostar de mistério e viagem no tempo"

3. Preferência situacional
   Ex.: "hoje quero algo leve"

4. Restrição negativa forte
   Ex.: "não recomende novamente o que eu já vi"

5. Restrição negativa fraca ou temporária
   Ex.: "agora não quero romance fofo"

6. Estado operacional
   Ex.: "essa conversa virou pesquisa de reviews no Reddit"

## Meta de comportamento

O agente ideal deve:

- perguntar antes de assumir
- lembrar sem parecer aleatório
- atualizar contexto com o tempo
- usar ferramentas quando necessário
- não recomendar itens já consumidos, salvo se o usuário pedir explicitamente

## Fora de escopo da base

- multiusuário
- múltiplos canais de chat ao mesmo tempo
- automação empresarial pesada
- execução de skills sem política de permissão

