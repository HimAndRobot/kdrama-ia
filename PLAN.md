# KDrama IA - Agente de Recomendação

## Visão Geral

Um agente Python que recebe pedidos de recomendação de K-dramas e usa um modelo LLM local (Ollama, Gemma 4 E4B) com **tool calling** para consultar uma base de dados coletada do MDL. O agente roda ciclos de pensamento autônomos — decide sozinho o que consultar, quando parar e como apresentar o resultado.

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│                    USUÁRIO                       │
│         "Quero algo parecido com Reset"          │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              AGENTE (Python local)               │
│                                                  │
│  1. Recebe o pedido do usuário                   │
│  2. Envia pro LLM com system prompt + tools      │
│  3. LLM pensa e decide chamar uma tool           │
│  4. Agente executa a tool e retorna resultado    │
│  5. LLM pensa de novo (ciclo)                    │
│  6. Quando satisfeito → resposta final           │
└──────┬───────────────────────────┬──────────────┘
       │                           │
       ▼                           ▼
┌──────────────┐         ┌──────────────────┐
│  Ollama API  │         │  Base de Dados   │
│  (servidor)  │         │  (JSON local)    │
│  gemma4:e4b  │         │  data/*.json     │
└──────────────┘         └──────────────────┘
```

## Fluxo do Agente (Loop de Raciocínio)

```
INÍCIO
  │
  ▼
[LLM recebe pedido + lista resumida dos dramas disponíveis]
  │
  ▼
┌─────────────────────────────────────┐
│         CICLO DE PENSAMENTO         │◄──────────────┐
│                                     │               │
│  O LLM analisa o que tem e decide:  │               │
│                                     │               │
│  → "Preciso ver detalhes de X"      │──► tool call ─┘
│  → "Preciso ver reviews de X"       │──► tool call ─┘
│  → "Quero buscar por tag Y"         │──► tool call ─┘
│  → "Já tenho o suficiente"          │──► resposta final
│                                     │
└─────────────────────────────────────┘
```

### O que o LLM recebe no início (contexto inicial)

Uma **lista compacta** com todos os dramas da base — só o essencial pra ele ter noção do que existe:

```
Dramas disponíveis (16):
1. Reset (2022) — Thriller, Mystery, Sci-Fi — ★9.0 — 10 reviews
2. Mobius (2025) — Thriller, Mystery — ★8.3 — 9 reviews
3. Someday or One Day (2019) — Romance, Mystery, Sci-Fi — ★8.8 — 10 reviews
...
```

Isso é leve (~1KB) e dá ao LLM o mapa completo. Ele não precisa ler tudo de uma vez.

### O que o LLM pode consultar (Tools)

| Tool | Descrição | Retorna |
|------|-----------|---------|
| `get_drama_details(title)` | Detalhes completos de um drama | Synopsis, cast, genres, tags, rating, episódios, ano |
| `get_drama_reviews(title, limit?)` | Reviews de usuários | Lista de reviews com nota e texto |
| `search_by_genre(genre)` | Busca dramas por gênero | Lista de dramas que batem |
| `search_by_tag(tag)` | Busca dramas por tag | Lista de dramas que batem |
| `compare_dramas(title1, title2)` | Compara dois dramas | Lado a lado: gêneros, tags, rating, synopsis |
| `get_similar(title)` | Dramas recomendados para X | Lista de recomendações (se existirem na base) |
| `search_reviews(keywords)` | Busca texto livre em TODAS as reviews | Reviews que mencionam os termos (ex: "competent police", "child protagonist") |
| `search_reviews_for(title, keywords)` | Busca texto em reviews de UM drama específico | Trechos relevantes das reviews daquele drama |

### Exemplo de ciclo real

**Usuário:** "Quero um kdrama parecido com Reset mas com mais romance"

**Ciclo 1 — LLM pensa:**
> "O usuário quer algo parecido com Reset mas com romance. Vou ver os detalhes de Reset primeiro."

→ Chama `get_drama_details("Reset")`
→ Recebe: Thriller, Mystery, Sci-Fi, tags: Time Loop, Death, Investigation...

**Ciclo 2 — LLM pensa:**
> "Reset é thriller com time loop. Preciso achar algo com time loop + romance. Vou buscar por tag."

→ Chama `search_by_tag("Time Loop")`
→ Recebe: Reset, Someday or One Day, 365: Repeat the Year, Lovely Runner...

**Ciclo 3 — LLM pensa:**
> "Lovely Runner e Someday or One Day parecem ter romance. Vou ver detalhes dos dois."

→ Chama `get_drama_details("Lovely Runner")`
→ Recebe: Romance, Comedy, Sci-Fi, ★9.0, tags: Time Travel, Idol...

**Ciclo 4 — LLM pensa:**
> "Lovely Runner tem romance + viagem no tempo + nota 9.0. Vou ver reviews pra confirmar que o romance é forte."

→ Chama `get_drama_reviews("Lovely Runner", 3)`
→ Recebe: 3 reviews confirmando romance forte

**Ciclo 5 — LLM decide:**
> "Tenho informação suficiente. Lovely Runner é a melhor recomendação."

→ Resposta final pro usuário

## Controle de Ciclos

- **Máximo de ciclos:** 10 (evita loop infinito)
- **Cada ciclo:** 1 pensamento + 0 ou 1 tool call
- **Condição de parada:** LLM retorna resposta sem chamar tool
- **Feedback visual:** cada ciclo mostra o que o LLM está pensando (transparência)

## Stack Técnica

| Componente | Tecnologia |
|-----------|------------|
| Linguagem | Python |
| LLM | Ollama API (gemma4:e4b no servidor 192.168.1.132) |
| Base de dados | JSON local (gerado pelo scraper) |
| Interface | CLI (terminal) |
| Comunicação LLM | HTTP via `requests` (Ollama /api/chat com tools) |

## Estrutura de Arquivos

```
kdrama-ia/
├── scrape.mjs          # Scraper MDL (Node + Playwright)
├── agent.py            # Agente principal (loop de raciocínio)
├── tools.py            # Implementação das tools (consultas ao JSON)
├── chat.py             # Interface CLI do usuário
├── package.json        # Deps do scraper
├── data/
│   └── 697563-kai-duan.json  # Base coletada
└── PLAN.md             # Este arquivo
```

## Próximos Passos

1. **tools.py** — Funções que leem o JSON e retornam dados formatados
2. **agent.py** — Loop de raciocínio que conecta o LLM às tools
3. **chat.py** — Interface CLI que recebe pergunta e mostra o processo
4. Testar ciclo completo
5. Coletar mais dramas (mais URLs no scraper) para ampliar a base
