# LootPrice — Estrategia de Afiliados, Lojas e Fontes de Dados

> **Versao:** 0.1.0-MVP
> **Ultima atualizacao:** 2026-06-26
> **Status:** Decisao arquitetural obrigatoria antes de novos crawlers
> **Audiencia:** Desenvolvedores, IAs de apoio, Scrum Master, Produto

---

## Objetivo

Este documento define como o LootPrice deve escolher lojas, coletar dados,
monetizar cliques e medir performance sem quebrar o produto no meio do
desenvolvimento por termos de uso, ausencia de afiliado, bloqueios de scraping
ou risco reputacional.

O ponto central e:

```text
Crawler/feed/API coleta dados.
Redirect interno monetiza e mede clique.
Termos da loja decidem se a fonte pode ser usada.
```

Programa de afiliados nao substitui crawler automaticamente. Ele apenas
resolve atribuicao comercial do clique. A coleta de catalogo, preco e
disponibilidade ainda precisa vir de uma fonte permitida: API, feed oficial,
scraper autorizado ou cadastro manual.

Este documento nao e aconselhamento juridico. Para lojas criticas ou com termos
ambiguos, a decisao final deve ser validada nos termos oficiais e, se possivel,
por contato direto com o programa de afiliados.

---

## Principios Obrigatorios

1. **Nenhuma loja nova entra apenas porque e tecnicamente raspavel.**
   Antes de criar crawler, deve existir decisao registrada sobre termos,
   metodo de ingestao e permissao de exibicao de preco.

2. **Frontend nunca deve apontar direto para URL afiliada externa.**
   Todo clique de compra passa por endpoint interno de outbound redirect para
   registrar metrica e aplicar `click_id`, `subid` ou parametro equivalente.

3. **Crawler nao deve ser responsavel por tracking comercial.**
   Crawler coleta `store_url`, preco, disponibilidade e metadados. A URL
   afiliada deve ser gerada em camada propria de afiliados/redirect.

4. **Se scraping nao for permitido, nao fazemos scraping.**
   Alternativas: feed/API oficial, importacao de CSV/XML, cadastro manual ou
   loja desativada.

5. **Marketplaces de keys devem ser separados visual e tecnicamente.**
   G2A, Eneba, Kinguin e similares exigem sinalizacao de marketplace, regiao de
   ativacao, vendedor e risco antes de serem exibidos junto de lojas
   autorizadas.

6. **Metricas de clique entram no MVP monetizado.**
   Sem tracking interno, o LootPrice nao consegue avaliar CTR, lojas com maior
   intencao de compra, posicao da oferta e reconciliacao futura de comissoes.

7. **Conversao e comissao dependem do parceiro.**
   O MVP deve registrar cliques. Conversoes reais entram quando a loja/rede
   oferecer postback, API, relatorio CSV ou outro meio confiavel.

---

## Arquitetura Recomendada

```text
                [ API oficial ]
                     │
                [ Feed afiliado ]
                     │
                [ Scraper permitido ]
                     │
                [ Cadastro manual ]
                     │
                     ▼
              [ Ingestion Service ]
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 [ games/store_products ]       [ prices ]
        │                         │
        └────────────┬────────────┘
                     ▼
              [ FastAPI REST ]
                     │
              [ React SPA ]
                     │ clique
                     ▼
        GET /api/v1/out/{price_id}
                     │
       registra affiliate_click + click_id
                     │
       monta URL afiliada por loja/campanha
                     │
                     ▼
              302 para a loja
```

### Separacao de URLs

| Campo/conceito | Uso |
|---|---|
| `store_products.store_url` | URL canonica limpa do produto na loja. Vem da fonte de dados. |
| `prices.affiliate_url` | Campo legado/compatibilidade. Nao deve ser exposto direto ao frontend quando houver redirect interno. |
| `affiliate_link_template` | Regra por loja/campanha para montar link afiliado com `click_id`/`subid`. |
| `/api/v1/out/{price_id}` | URL publica do LootPrice que registra clique e redireciona. |

### Tipos de Ingestao

| Tipo | Quando usar | Observacao |
|---|---|---|
| `api` | Loja oferece API oficial e termos permitem uso comercial/comparador. | Preferido quando disponivel. |
| `feed` | Programa de afiliados fornece CSV/XML/API de produtos. | Melhor caminho para monetizacao. |
| `scraper` | Termos permitem coleta ou existe autorizacao explicita. | Exige rate limit, logs e testes de contrato. |
| `manual` | Loja nao tem fonte automatica, mas permite link/oferta cadastrada. | Bom para MVP ou campanhas pontuais. |
| `disabled` | Termos incertos, loja bloqueada ou risco alto demais. | Nao coletar, nao exibir. |

---

## Matriz Inicial de Lojas

Esta matriz e uma avaliacao inicial para orientar o backlog. Cada loja ainda
precisa de validacao formal antes da implementacao.

| Loja | Categoria | Fonte preferida | Afiliado/monetizacao | Risco | Decisao recomendada |
|---|---|---|---|---|---|
| Steam | Plataforma oficial | API oficial quando permitido | Incerto/baixo para comparador afiliado | Medio | Usar como catalogo/preco se termos permitirem; nao depender como receita. |
| Epic Games Store | Plataforma oficial | API/parceria oficial | Suporte a criadores existe, mas nao equivale necessariamente a comparador afiliado | Medio/alto | Nao priorizar crawler; integrar apenas com permissao clara. |
| Xbox/Microsoft Store | Plataforma oficial | API/parceria oficial | Incerto para comparador de jogos | Medio/alto | Fase futura. Nao bloquear MVP. |
| Nintendo eShop | Plataforma oficial | API/parceria oficial | Incerto | Alto | Nao usar no MVP sem permissao formal. |
| PlayStation Store | Plataforma oficial | API/parceria oficial | Incerto | Alto | Nao usar no MVP sem permissao formal. |
| Nuuvem | Loja autorizada de keys | Feed/API/parceria; scraper so se permitido | Provavel via parceria direta ou rede | Medio | Boa candidata BR; validar termos antes do crawler. |
| Green Man Gaming | Loja autorizada de keys | Feed/API afiliado | Boa candidata | Baixo/medio | Priorizar validacao de programa e feed. |
| Fanatical | Loja autorizada de keys | Feed/API afiliado | Boa candidata | Baixo/medio | Priorizar validacao de programa e feed. |
| Humble Bundle | Loja/bundles | Feed/API/parceria | Possivel, mas modelo de bundles exige cuidado | Medio | Boa candidata futura; separar bundles de jogos avulsos. |
| GOG | Loja oficial DRM-free | API/feed/parceria | Incerto | Medio | Boa candidata de catalogo; validar afiliado. |
| Ubisoft Store | Publisher store | API/parceria | Incerto | Medio | Fase futura. |
| EA app / EA Store | Publisher store | API/parceria | Incerto | Medio | Fase futura. |
| Battle.net | Publisher store | API/parceria | Incerto | Medio/alto | Fase futura. |
| Eneba | Marketplace de keys | Feed/API afiliado | Provavel | Alto | Nao MVP inicial; exige camada de marketplace/riscos. |
| G2A | Marketplace de keys | Feed/API afiliado | Provavel | Alto | Nao MVP inicial; exige camada de marketplace/riscos. |
| Kinguin | Marketplace de keys | Feed/API afiliado | Provavel | Alto | Nao MVP inicial; exige camada de marketplace/riscos. |
| itch.io | Loja indie | API/parceria/manual | Incerto | Medio | Fase futura; interessante para catalogo indie. |

### Ordem Recomendada

1. **Nuuvem + Steam** continuam como escopo inicial, mas com ajuste:
   Steam como fonte de catalogo/preco, Nuuvem como candidata comercial BR.

2. **Green Man Gaming e Fanatical** devem ser avaliadas logo depois por terem
   perfil mais alinhado ao modelo de afiliado com lojas autorizadas.

3. **Humble e GOG** entram na segunda onda, apos validar como lidar com bundles,
   DRM-free e disponibilidade regional.

4. **Eneba, G2A e Kinguin** ficam fora do MVP inicial ate existirem campos,
   UX e regras para marketplace.

5. **Nintendo, PlayStation, Xbox e Epic** nao devem ser fonte principal do MVP
   sem API/parceria clara.

---

## Checklist Antes de Integrar Uma Loja

Uma issue de nova loja/crawler so pode sair de backlog quando estas respostas
estiverem registradas:

| Pergunta | Obrigatorio |
|---|---|
| A loja permite exibicao publica de preco em comparador? | Sim |
| A loja permite deep link para produto? | Sim |
| A loja permite tracking por `subid`, `click_id` ou equivalente? | Preferivel |
| A loja fornece API/feed oficial? | Preferivel |
| Se nao ha API/feed, os termos permitem scraping? | Obrigatorio para scraper |
| A loja limita caching de preco/disponibilidade? | Registrar TTL |
| Existe requisito de marca, disclaimer ou texto obrigatorio? | Registrar |
| Existe restricao geografica/regiao de ativacao? | Registrar |
| Existe risco de marketplace/vendedor terceiro? | Registrar |
| Como reconciliar conversoes/comissoes? | Registrar, mesmo que "manual/CSV" |

Se uma resposta critica for "nao", a loja deve ficar como `disabled` ou
`manual`, nao como `scraper`.

---

## Politica Para Marketplaces de Keys

Marketplaces podem gerar receita, mas trazem risco maior do que lojas
autorizadas. Antes de exibir G2A, Eneba, Kinguin ou equivalentes:

- adicionar `is_marketplace = true`;
- exibir selo/indicacao de marketplace no frontend;
- registrar regiao de ativacao quando disponivel;
- registrar vendedor/merchant quando disponivel;
- registrar rating/reputacao do vendedor quando disponivel;
- diferenciar loja autorizada de marketplace na ordenacao ou no visual;
- nao esconder que a oferta vem de terceiros;
- avaliar suporte, reembolso e disputa;
- nao misturar "menor preco absoluto" com "melhor recomendacao" sem criterio.

No MVP inicial, a recomendacao e nao incluir marketplaces cinzas ate que estes
campos e a UX estejam implementados.

---

## Metricas Obrigatorias

### `affiliate_clicks`

Tabela/evento minimo para o MVP monetizado:

```text
id UUID
click_id UUID/string unico
store_id UUID
store_product_id UUID
price_id UUID nullable
game_id UUID
user_id UUID nullable
session_id VARCHAR nullable
placement VARCHAR
position INTEGER nullable
price_brl NUMERIC(10,2)
destination_url TEXT
referrer TEXT nullable
user_agent TEXT nullable
ip_hash TEXT nullable
clicked_at TIMESTAMPTZ
```

Eventos esperados:

| Evento | Quando dispara |
|---|---|
| `offer_click` | Usuario clica em oferta e chama `/api/v1/out/{price_id}`. |
| `redirect_success` | Backend conseguiu montar URL e respondeu 302. |
| `redirect_blocked` | Loja/produto esta desativado, sem permissao ou sem URL valida. |

Campos `ip_hash` e `user_agent` exigem politica de privacidade. Nao armazenar
IP bruto sem decisao explicita.

### `affiliate_conversions`

Fase 2, quando houver postback/API/CSV:

```text
id UUID
click_id VARCHAR
store_id UUID
external_order_id_hash VARCHAR nullable
commission_brl NUMERIC(10,2)
order_value_brl NUMERIC(10,2)
status VARCHAR  -- pending | approved | rejected | paid
converted_at TIMESTAMPTZ nullable
reported_at TIMESTAMPTZ
```

Sem postback/API/relatorio da loja, o LootPrice mede clique e intencao, mas nao
conversao real.

---

## Implicacoes Por Area

### Backend

- `stores` deve guardar metodo de ingestao, flags de permissao, risco e status
  de compliance.
- Runner deve ignorar lojas `disabled` ou sem permissao para a fonte escolhida.
- Crawler deve retornar URL limpa (`store_url`) e nao depender de URL afiliada.
- API publica deve retornar URL interna de outbound redirect, nao URL afiliada
  externa direta.
- Endpoint `/api/v1/out/{price_id}` deve aplicar rate limit, validar loja/produto
  ativo, registrar clique e redirecionar.
- Alteracoes de schema exigem Alembic e testes.

### Frontend

- Botoes de compra usam `outbound_url` interno.
- UI deve sinalizar marketplace, risco/regiao e ultima atualizacao.
- Pagina de detalhe deve manter comparacao clara, mas nao esconder contexto de
  loja versus marketplace.
- Em ofertas bloqueadas ou sem permissao, mostrar estado indisponivel em vez de
  link externo.

### Infra e Analytics

- Nginx/Cloudflare devem preservar IP real apenas quando necessario e de forma
  compativel com privacidade.
- Logs de redirect nao devem vazar tokens afiliados sensiveis.
- Campanhas e templates afiliados devem vir de `.env` ou tabela segura, nunca
  hardcoded.
- Dashboard/admin futuro deve mostrar cliques por loja, jogo, placement e CTR.

### Scrum/Backlog

- Toda issue de nova loja precisa conter uma secao "Compliance e afiliado".
- Issues de crawler devem ter dependencia de decisao de fonte (`api`, `feed`,
  `scraper`, `manual`, `disabled`).
- Issues existentes de Steam/Nuuvem precisam ser atualizadas com criterios de
  permissao e tracking.

---

## Fontes Iniciais Para Validacao

Links oficiais ou institucionais consultados/indicados como ponto de partida.
Eles nao substituem os termos finais do programa de afiliados de cada loja.

| Loja | Link |
|---|---|
| Steamworks Web API | https://partner.steamgames.com/doc/webapi/ISteamApps |
| Steamworks IStoreService | https://partner.steamgames.com/doc/webapi/IStoreService |
| Epic Support-A-Creator | https://sac.epicgames.com/overview |
| Epic Games Store | https://store.epicgames.com/ |
| Microsoft/Xbox Store | https://www.xbox.com/games/all-games |
| Nintendo eShop | https://www.nintendo.com/us/store/games/ |
| PlayStation Store | https://www.playstation.com/ps-store/ |
| Nuuvem | https://www.nuuvem.com/br-pt/ |
| Green Man Gaming | https://www.greenmangaming.com/ |
| Fanatical | https://www.fanatical.com/ |
| Humble Bundle | https://www.humblebundle.com/ |
| GOG | https://www.gog.com/ |
| G2A institucional | https://www.g2a.co/ |
| Eneba institucional | https://www.eneba.com/us/about-us |
| Kinguin seller/marketplace | https://www.kinguin.net/sell-on-kinguin |

---

## Decisao Registrada

Para o LootPrice, a decisao de arquitetura a partir de 2026-06-26 e:

```text
Nao existe "crawler por padrao".
Cada loja deve declarar fonte permitida, permissao comercial, risco e estrategia
de afiliado antes de qualquer implementacao.
```

O MVP deve continuar com Steam/Nuuvem como base tecnica inicial, mas com a camada
de afiliados/tracking planejada antes do frontend de detalhe de jogo.
