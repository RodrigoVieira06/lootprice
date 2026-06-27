# LootPrice — Estrategia Frontend e Mobile

> **Versao:** 0.2.0
> **Ultima atualizacao:** 2026-06-27
> **Status:** Decisao arquitetural para a Fase 1.5
> **Audiencia:** Desenvolvedores frontend, IAs de apoio, Produto

---

## Objetivo

Preparar o frontend React SPA para uma fase futura de aplicativos Android e
iOS sem adicionar complexidade nativa no MVP.

A decisao para a Fase 1.5 e:

```text
Construir uma SPA web-first e mobile-ready.
Nao adicionar React Native, Expo, Tauri, Capacitor, Rust, Android ou iOS ao MVP frontend.
Isolar pontos dependentes de plataforma desde o inicio.
```

Para a fase mobile, React Native + Expo passa a ser a opcao preferencial se
Android/iOS virarem produto nativo importante. Tauri v2 continua candidato se
desktop ou reuso maximo da SPA forem objetivos fortes. Capacitor continua
candidato se o objetivo for empacotar a experiencia web em WebView com menor
custo operacional.

Antes de implementar apps Android/iOS, deve haver uma issue propria comparando
React Native + Expo, Tauri v2 e Capacitor com base em UX, reuso de codigo,
OAuth, storage seguro, links externos, CI, distribuicao e manutencao.

---

## Principios Obrigatorios

1. **O frontend do MVP continua sendo React SPA.**
   Vite, TSX, SCSS, Axios, Zod, React Hook Form, Zustand, Biome, Jest e pnpm
   continuam sendo a stack base.

2. **Nao introduzir dependencia mobile antes da fase mobile.**
   Sem React Native, Expo, `src-tauri`, `@tauri-apps/*`, Capacitor, Android SDK,
   Xcode, Rust ou scripts nativos na Fase 1.5 sem decisao registrada em
   `AGENTS.md`.

3. **Isolar comportamento dependente de plataforma.**
   Componentes e services de dominio nao devem espalhar acesso direto a
   `window.location`, `window.open`, `localStorage`, `sessionStorage`,
   `document` ou APIs nativas. Use adapters em `frontend/src/platform/`.

4. **Cliques de compra continuam passando pelo backend.**
   Web, React Native, Expo, Tauri, Capacitor ou qualquer app futuro devem abrir
   o `outbound_url` interno da API. Nunca usar `affiliate_url` externa como link
   primario.

5. **Auth deve ser preparado para web e mobile.**
   OAuth Google/Discord deve ficar centralizado em service/adapter, sem callback
   hardcoded em componentes. Deep links mobile ficam para a fase mobile.

6. **Storage de token deve ser substituivel.**
   Tokens sensiveis nao devem ser gravados em `localStorage` sem decisao
   explicita. A Fase 1.5 deve usar uma interface de storage para permitir troca
   futura por secure storage nativo.

7. **UI nasce responsiva e touch-friendly.**
   Busca, cards, detalhe de jogo, auth e botoes de compra devem funcionar bem
   em celular, tablet e desktop. Validar estados com viewport mobile.

---

## Estrutura Recomendada

Quando o frontend for criado, a estrutura esperada passa a incluir adapters de
plataforma:

```text
frontend/src/
├── components/
├── hooks/
├── pages/
├── platform/
│   ├── browser.ts
│   ├── outbound.ts
│   ├── storage.ts
│   └── authRedirect.ts
├── services/
├── store/
└── types/
```

Os nomes exatos podem variar, mas as responsabilidades nao:

| Adapter | Responsabilidade |
|---|---|
| `outbound` | Abrir `outbound_url` interno para registrar clique e redirecionar |
| `storage` | Expor interface substituivel para tokens/sessao |
| `authRedirect` | Centralizar inicio e callback de login social |
| `browser` | Isolar APIs globais do navegador quando forem necessarias |

---

## Regras Para Ofertas e Afiliados

- Toda UI de oferta recebe e usa `outbound_url`.
- O clique chama uma funcao unica, por exemplo `openOutboundOffer(outboundUrl)`.
- `openOutboundOffer()` deve validar URL interna antes de abrir.
- Oferta bloqueada, indisponivel ou sem permissao de redirect nao abre link.
- Em mobile futuro, o adapter deve abrir o redirect interno em navegador externo
  ou webview aprovada, preservando registro em `/api/v1/out/{price_id}`.
- Nunca montar URL afiliada no frontend.
- Nunca expor token afiliado, campaign secret ou template comercial no bundle.

---

## Auth e Sessao

Para login local:

- chamadas HTTP ficam em `services/auth`;
- storage de tokens passa por adapter;
- refresh/logout nao devem depender diretamente de componente React.

Para OAuth:

- componentes apenas disparam acao de login social;
- URLs de inicio (`/auth/google`, `/auth/discord`) ficam no service;
- callback web fica isolado;
- deep links mobile entram apenas na fase mobile.

---

## Criterios Para a Fase Mobile

Antes de adicionar qualquer stack mobile, criar issue propria com:

- comparativo React Native + Expo vs Tauri v2 vs Capacitor para Android/iOS;
- decisao sobre objetivo do produto:
  - mobile nativo importante: React Native + Expo ganha peso;
  - desktop tambem e objetivo: Tauri ganha peso;
  - reuso maximo da SPA/WebView: Capacitor ou Tauri ganham peso;
- estrategia de compartilhamento entre SPA e app mobile: tipos, schemas Zod,
  services de API e regras de negocio podem ser compartilhados; componentes DOM
  e SCSS nao devem ser assumidos como reutilizaveis em React Native;
- estrategia de OAuth com deep links;
- storage seguro para tokens;
- abertura de links externos e conformidade de afiliados;
- assinatura Android/iOS, contas de desenvolvedor e distribuicao;
- CI separado para builds mobile;
- testes de smoke em dispositivo/emulador;
- atualizacao de `AGENTS.md`, skills e docs.

### Referencia React Native + Expo Para Avaliacao

Quando a fase mobile for iniciada, considerar estes pontos:

- React Native + Expo e a opcao preferencial se Android/iOS forem produto nativo
  importante para o LootPrice.
- O app pode compartilhar tipos TypeScript, schemas Zod, services de API,
  regras de auth e regras de outbound com a SPA.
- Componentes visuais, navegacao e estilos devem ser implementados em stack
  nativa. Nao assumir reuso direto de componentes React DOM ou SCSS da SPA.
- Expo reduz custo inicial de setup mobile, entrega tooling de desenvolvimento
  e facilita evolucao para builds/distribuicao mobile.
- Avaliar Expo Router ou React Navigation para navegacao.
- Avaliar SecureStore/Keychain/Keystore para tokens, sem `localStorage`.
- Avaliar Linking/WebBrowser para OAuth e abertura de `outbound_url`.
- Validar politica de lojas e afiliados para abertura de links externos em
  Android/iOS.

Referencias oficiais:

- https://reactnative.dev/docs/environment-setup
- https://docs.expo.dev/
- https://docs.expo.dev/develop/development-builds/introduction/

### Referencia Tauri Para Avaliacao

Quando a fase mobile for iniciada, considerar estes pontos:

- Tauri v2 pode empacotar frontend web em desktop/mobile, mas adiciona Rust e
  toolchain nativa.
- Android exige Android Studio, SDK Platform, Platform-Tools, NDK, Build-Tools,
  Command-line Tools e targets Rust Android.
- iOS exige macOS com Xcode completo e targets Rust iOS. Build iOS nao deve ser
  planejado em Linux.
- Se escolhido, Tauri deve entrar em PR proprio com `src-tauri`,
  `tauri.conf.json`, dependencias `@tauri-apps/*`, crates/plugins Rust, scripts
  e CI mobile.
- Plugins provaveis: `@tauri-apps/plugin-opener` para abrir `outbound_url` no
  navegador/sistema e `@tauri-apps/plugin-deep-link` para OAuth/deep links.
- Todo uso de Tauri deve ficar atras dos adapters em `frontend/src/platform/`.
- Capabilities/permissoes devem ser minimas e validar dominios/rotas antes de
  abrir URLs externas.
- Distribuicao exige signing, versionamento nativo, contas de desenvolvedor e
  testes em emulador/dispositivo.

Referencias oficiais:

- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/plugin/opener/
- https://v2.tauri.app/plugin/deep-linking/
- https://v2.tauri.app/distribute/google-play/
- https://v2.tauri.app/distribute/app-store/

### Referencia Capacitor Para Avaliacao

Quando a fase mobile for iniciada, considerar estes pontos:

- Capacitor e candidato se o objetivo for manter a SPA como experiencia central
  em WebView com acesso a APIs nativas.
- Tende a ter menor mudanca de UI que React Native, mas entrega UX menos nativa
  quando comparado a um app React Native bem implementado.
- Assim como Tauri, deve ficar atras dos adapters de `frontend/src/platform/`.
- Deve ser comparado com Tauri quando o criterio principal for reuso da SPA.

Referencia oficial:

- https://capacitorjs.com/docs

---

## Decisao Registrada

Para o LootPrice, a decisao a partir de 2026-06-27 e:

```text
Fase 1.5 entrega React SPA mobile-ready.
Fase mobile futura compara React Native + Expo, Tauri v2 e Capacitor.
React Native + Expo e preferencial se mobile nativo virar prioridade.
```
