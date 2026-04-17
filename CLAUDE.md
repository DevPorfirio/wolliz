# Wolliz

## Visão Geral

Wolliz é um marketplace imobiliário com foco em performance,
SEO e escalabilidade. O projeto está dividido em 3 camadas: `front-end`, `back-end` e `infra`.

---

## Stack

### Front-end — `front-end/`
- **Framework**: Nuxt 3 (SSR — Server-Side Rendering)
- **Runtime**: Node.js (servidor Nuxt processa cada request e envia HTML ao cliente)
- **Assets estáticos**: Servidos pelo MinIO (S3-compatible) via CDN URL
  - O que vai pro MinIO: bundles JS/CSS (`/_nuxt/`), imagens de imóveis, ícones
  - O que fica no servidor Node: renderização SSR de páginas dinâmicas
- **Estado global**: Pinia
- **Auth**: Access token em memória (Pinia), refresh token em HttpOnly cookie
- **HTTP client**: `$fetch` (ofetch) via composables
- **Estilo**: CSS customizado (sem Tailwind por padrão)
- **Mapa**: Mapbox GL JS (client-side only, via plugin `.client.ts`)

### Back-end — `back-end/`
- **Framework**: Django 5.2 LTS + Django REST Framework (DRF)
- **Auth**: JWT via `djangorestframework-simplejwt` (access + refresh tokens)
- **ORM**: Django ORM com PostgreSQL
- **Storage**: `django-storages` + MinIO (S3-compatible) para arquivos e imagens
- **Cache**: Redis (django-redis)
- **Server**: Uvicorn (produção) / `runserver` (dev)
- **User model**: customizado (`AbstractBaseUser`) em `apps/users`
- **Package manager**: `uv` (substitui pip/poetry) — deps em `pyproject.toml`

### Infra — `infra/`
- **Fase 1 (atual)**: Docker Compose para desenvolvimento local
- **Fase 2 (futuro)**: Kubernetes (K8s) com manifests em `infra/k8s/`

#### Serviços Docker
| Serviço    | Imagem           | Porta  | Função                                         |
|------------|------------------|--------|------------------------------------------------|
| postgres   | postgres:16      | 5432   | Banco de dados principal                       |
| redis      | redis:7-alpine   | 6379   | Cache e filas                                  |
| minio      | minio/minio      | 9000   | Storage S3-compatible                          |
| minio-init | minio/mc         | —      | Cria buckets no boot                           |
| migrate    | build local      | —      | Roda migrations + seed mock (se habilitado)    |
| backend    | build local      | 8000   | API Django + DRF                               |
| frontend   | build local      | 3000   | SSR Nuxt 3                                     |

---

## Arquitetura de Auth

### Fluxo de Login

```
[Browser] → GET /auth/login
    → [Nuxt Server SSR] renderiza página de login → HTML pro cliente

[Browser] → POST /api/auth/login (Nuxt server route / BFF)
    → [Nuxt Server] chama Django API: POST /api/auth/token/
    → [Django] valida credenciais, retorna { access, refresh }
    → [Nuxt Server] seta cookie HttpOnly `refresh_token`
    → [Nuxt Server] retorna { access_token } pro browser
    → [Browser / Pinia] armazena access_token em memória
```

### Fluxo de Refresh

```
[Browser] → request com access_token expirado (401)
    → [Nuxt composable] chama POST /api/auth/refresh (Nuxt server route)
    → [Nuxt Server] lê cookie HttpOnly `refresh_token`
    → [Nuxt Server] chama Django API: POST /api/auth/token/refresh/
    → [Django] retorna novo { access }
    → [Nuxt Server] retorna novo access_token pro browser
    → [Pinia] atualiza access_token em memória
```

### Endpoints Django Auth

| Método | Path                        | Descrição                   |
|--------|-----------------------------|-----------------------------|
| POST   | /api/auth/register          | Criar conta                 |
| POST   | /api/auth/token             | Login (retorna JWT pair)    |
| POST   | /api/auth/token/refresh     | Refresh do access token     |
| POST   | /api/auth/token/verify      | Verificar validade token    |
| POST   | /api/auth/logout            | Invalida refresh token      |
| GET    | /api/auth/me                | Dados do usuário logado     |
| PATCH  | /api/auth/profile           | Atualiza nome e telefone    |
| POST   | /api/auth/change-password   | Altera senha                |
| POST   | /api/auth/forgot-password   | Inicia recuperação de senha |
| POST   | /api/auth/avatar            | Upload de foto de perfil    |

### Endpoints Nuxt (BFF — server routes)

| Método | Path                        | Descrição                           |
|--------|-----------------------------|-------------------------------------|
| POST   | /api/auth/login             | Faz login, seta HttpOnly cookie     |
| POST   | /api/auth/register          | Registra novo usuário               |
| POST   | /api/auth/refresh           | Renova access_token via cookie      |
| POST   | /api/auth/logout            | Limpa cookie e invalida no backend  |
| GET    | /api/auth/me                | Retorna usuário logado (via token)  |

### Endpoints Django Properties

| Método | Path                        | Descrição                                            |
|--------|-----------------------------|------------------------------------------------------|
| GET    | /api/properties/search      | Busca imóveis por lat/lng/radius_km (público)        |
| GET    | /api/properties/{uuid}      | Detalhe de um imóvel + galeria de imagens (público)  |

### Restauração automática de sessão

O plugin `front-end/plugins/auth.ts` roda no boot da app (SSR + client) e tenta
restaurar a sessão a partir do cookie HttpOnly `refresh_token`. Sem ele, abrir
uma nova aba (ou abrir um imóvel em nova aba via target="_blank") deixava a
store Pinia vazia e o usuário aparecia deslogado mesmo com cookie válido.

Detalhe importante de SSR: cookies setados dentro de uma route handler interna
(`/api/auth/refresh`) **não propagam** para a resposta da página. Por isso o
plugin chama o Django diretamente em SSR, lendo/escrevendo o cookie no `event`
da requisição da página — assim o cookie rotacionado chega ao browser.

---

## Estrutura de Pastas

```
wolliz/
├── CLAUDE.md                   # Este arquivo
├── front-end/
│   ├── Dockerfile
│   ├── package.json            # inclui mapbox-gl
│   ├── nuxt.config.ts
│   ├── app.vue
│   ├── pages/
│   │   ├── index.vue           # Home com SearchBar
│   │   ├── search.vue          # Busca de imóveis (split-view mapa + lista)
│   │   ├── properties/
│   │   │   └── [id].vue        # Página de detalhe do imóvel (galeria, mapa/street view)
│   │   └── auth/
│   │       ├── login.vue       # Página de login
│   │       └── register.vue    # Página de cadastro
│   ├── components/
│   │   ├── AppLogo.vue         # Logo (link para /)
│   │   ├── AppFooter.vue       # Rodapé compartilhado (modo padrão e compact)
│   │   ├── AppUserMenu.vue     # Menu auth (Entrar/Criar conta ou avatar+dropdown)
│   │   ├── SearchBar.vue       # Input de busca com geocoding Mapbox
│   │   ├── PropertyCard.vue    # Card de imóvel (abre detalhe em nova aba)
│   │   ├── PropertyList.vue    # Grid de imóveis com filtros e colunas responsivas
│   │   └── PropertyMap.vue     # Mapa Mapbox (client-only) com pins coloridos + popup CTA
│   ├── composables/
│   │   ├── useAuth.ts
│   │   └── usePropertySearch.ts  # Busca de imóveis, URL como fonte de verdade
│   ├── plugins/
│   │   ├── mapbox.client.ts    # Inicializa Mapbox GL JS (client-side only)
│   │   └── auth.ts             # Restaura sessão do cookie HttpOnly em todo boot
│   ├── stores/
│   │   └── auth.ts             # Pinia store de autenticação
│   ├── middleware/
│   │   └── auth.ts             # Middleware de proteção de rotas
│   └── server/
│       └── api/
│           └── auth/
│               ├── login.post.ts
│               ├── register.post.ts
│               ├── refresh.post.ts   # Persiste refresh rotacionado de volta no cookie
│               ├── logout.post.ts
│               └── me.get.ts
├── back-end/
│   ├── Dockerfile
│   ├── pyproject.toml          # deps gerenciadas pelo uv
│   ├── .python-version         # pin Python 3.12 para o uv
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── apps/
│       ├── users/
│       │   ├── models.py       # User model customizado
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── admin.py
│       └── properties/
│           ├── models.py       # Property + PropertyImage
│           ├── serializers.py  # PropertyCardSerializer + PropertyDetailSerializer
│           ├── views.py        # PropertySearchView + PropertyDetailView
│           ├── urls.py
│           ├── admin.py
│           └── management/
│               └── commands/
│                   └── seed_properties.py  # Mock data + 5 fotos sample por imóvel
└── infra/
    ├── docker/
    │   ├── docker-compose.yml
    │   ├── fresh.sh            # Start limpo (sempre seta SEED_MOCK_DATA=true)
    │   └── .env.example
    └── k8s/                    # (futuro) manifests Kubernetes
```

---

## Modelo de Usuário

Campos do `User` customizado (`AbstractBaseUser`):

| Campo      | Tipo           | Descrição                   |
|------------|----------------|-----------------------------|
| id         | UUID           | PK                          |
| email      | EmailField     | único, usado como login     |
| name       | CharField      | nome completo               |
| phone      | CharField      | telefone (opcional)         |
| avatar     | ImageField     | foto de perfil (MinIO)      |
| is_active  | BooleanField   | conta ativa                 |
| is_staff   | BooleanField   | acesso ao admin Django      |
| created_at | DateTimeField  | data de criação             |
| updated_at | DateTimeField  | última atualização          |

## Modelo de Imóvel

Campos do `Property` (`models.Model`):

| Campo         | Tipo           | Descrição                             |
|---------------|----------------|---------------------------------------|
| id            | UUID           | PK                                    |
| owner         | FK → User      | dono do anúncio (null em mocks)       |
| title         | CharField      | título do anúncio                     |
| description   | TextField      | descrição longa (opcional)            |
| property_type | CharField      | house / apartment / commercial / land |
| listing_type  | CharField      | sale / rent                           |
| price         | DecimalField   | valor em BRL                          |
| area_m2       | DecimalField   | área em m²                            |
| bedrooms      | SmallInt       | quartos                               |
| bathrooms     | SmallInt       | banheiros                             |
| parking_spots | SmallInt       | vagas                                 |
| latitude      | DecimalField   | coordenada (indexada)                 |
| longitude     | DecimalField   | coordenada (indexada)                 |
| address_line  | CharField      | endereço completo                     |
| city          | CharField      | cidade (indexada)                     |
| state         | CharField      | UF (SP, RJ, SC…)                      |
| zipcode       | CharField      | CEP (opcional)                        |
| is_active     | BooleanField   | anúncio ativo (indexado)              |
| created_at    | DateTimeField  | data de criação                       |
| updated_at    | DateTimeField  | última atualização                    |

Campos do `PropertyImage`:

| Campo      | Tipo          | Descrição                                            |
|------------|---------------|------------------------------------------------------|
| id         | UUID          | PK                                                   |
| property   | FK → Property | imóvel relacionado                                   |
| image      | ImageField    | arquivo no MinIO (`wolliz-media/properties/...`)     |
| is_cover   | BooleanField  | exibida no card / topo da galeria                    |
| order      | SmallInt      | ordem na galeria                                     |
| created_at | DateTimeField | data de criação                                      |

---

## Variáveis de Ambiente

```
# ─── PostgreSQL ───────────────────────────────────────────────────────────────
POSTGRES_DB=wolliz
POSTGRES_USER=wolliz
POSTGRES_PASSWORD=wolliz

# ─── Django ───────────────────────────────────────────────────────────────────
DJANGO_SECRET_KEY=change-me-in-production
DJANGO_DEBUG=True
DB_NAME=wolliz
DB_USER=wolliz
DB_PASSWORD=wolliz
DB_HOST=postgres
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ORIGINS=http://localhost:3000
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7

# ─── MinIO ────────────────────────────────────────────────────────────────────
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minio:9000           # hostname interno (Docker) usado pelo backend
MINIO_PUBLIC_ENDPOINT=localhost:9000 # hostname público — substituído nas URLs servidas ao browser
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_MEDIA=wolliz-media
MINIO_BUCKET_STATIC=wolliz-static

# ─── Seed / Mock Data ─────────────────────────────────────────────────────────
# true  → cria imóveis mock ao subir (para desenvolvimento)
# false → não popula dados (padrão para produção)
SEED_MOCK_DATA=true

# ─── Nuxt ─────────────────────────────────────────────────────────────────────
NUXT_API_BASE_URL=http://backend:8000
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_CDN_URL=http://localhost:9000/wolliz-static
NUXT_PUBLIC_MAPBOX_TOKEN=pk.your-token-here
```

---

## Decisões Técnicas

- **HttpOnly cookie para refresh token**: evita acesso via JS, protege contra XSS
- **Access token em memória (Pinia)**: não persiste em localStorage, mais seguro
- **BFF pattern (Nuxt server routes)**: o browser nunca chama o Django diretamente em auth
- **UUID como PK**: evita enumeração de IDs
- **Email como username**: mais natural para usuário final
- **MinIO**: S3-compatible self-hosted, fácil migração para AWS S3 em produção
- **APPEND_SLASH=False**: API REST sem redirecionamento de barra final
- **Serviço `migrate` isolado**: migrations rodam uma única vez antes do backend subir, evitando race conditions ao escalar horizontalmente
- **Mapbox GL JS client-only**: plugin com sufixo `.client.ts`, componente `PropertyMap` sempre dentro de `<ClientOnly>` — evita crash de `window is not defined` no SSR
- **Haversine no ORM Django**: busca geoespacial sem PostGIS usando `ACos/Cos/Sin/Radians` do Django ORM + pré-filtro por bounding box (índice B-tree)
- **URL como fonte de verdade na busca**: `usePropertySearch` observa `route.query` — mover o mapa, paginar ou compartilhar o link sempre refletem o estado correto
- **Mock data com SEED_MOCK_DATA**: todos os mocks têm prefixo `[MOCK]` no título, permitem limpeza sem afetar dados reais. O `fresh.sh` sempre garante `SEED_MOCK_DATA=true`
- **Mock images compartilhadas**: o `seed_properties` baixa 5 fotos de exemplo (Unsplash) **uma única vez** para `properties/samples/` no MinIO e cada `PropertyImage` referencia o mesmo path — 5 arquivos físicos para 29 imóveis × 5 fotos
- **URLs em inglês**: todas as rotas do front-end e endpoints do back-end são em inglês (`/search`, `/api/properties/search`, etc.)
- **MinIO público + URL rewrite**: o bucket `wolliz-media` é `download` (anônimo) e o storage usa `querystring_auth=False` para gerar URLs sem assinatura. O serializer reescreve `http://minio:9000` → `http://localhost:9000` (`MINIO_PUBLIC_ENDPOINT`) antes de devolver pro browser, que não enxerga o hostname interno do Docker
- **Restauração de sessão no boot**: o plugin `plugins/auth.ts` roda em SSR + client e troca o `refresh_token` cookie por um novo access + dados do user antes da página renderizar — assim novas abas (incluindo `target="_blank"` dos cards) já chegam autenticadas
- **Refresh com rotação**: `ROTATE_REFRESH_TOKENS=True` no Django invalida o refresh antigo a cada uso. O Nuxt server route `/api/auth/refresh` agora persiste o refresh rotacionado de volta no cookie HttpOnly — sem isso, a segunda chamada de refresh retornava 401
- **Detalhe do imóvel abre em nova aba**: tanto o card na lista quanto o "Acessar imóvel" do popup do mapa têm `target="_blank"` — preserva o contexto de busca e aproveita a restauração automática de sessão

---

## Comandos Úteis

```bash
# ── Início limpo (fresh start) ────────────────────────────────────────────────
cd infra/docker && bash fresh.sh

# ── Dia a dia ─────────────────────────────────────────────────────────────────
cd infra/docker && docker compose up -d
cd infra/docker && docker compose down
cd infra/docker && docker compose logs -f
cd infra/docker && docker compose logs -f backend

# ── Django ────────────────────────────────────────────────────────────────────
# Criar migrations após alterar models
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py makemigrations

# Rodar migrations manualmente
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py migrate

# Criar superusuário
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py createsuperuser

# Recriar mocks (--clear limpa os existentes antes)
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py seed_properties --clear

# Adicionar dependência Python
cd back-end && uv add nome-do-pacote

# ── URLs ──────────────────────────────────────────────────────────────────────
# Frontend:         http://localhost:3000
# Busca de imóveis: http://localhost:3000/search?local=...&lat=...&lng=...
# Backend API:      http://localhost:8000/api/
# MinIO console:    http://localhost:9001  (minioadmin / minioadmin)
# Django Admin:     http://localhost:8000/admin/
```
