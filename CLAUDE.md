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

### Back-end — `back-end/`
- **Framework**: Django 5 + Django Ninja
- **Auth**: JWT via `ninja-jwt` (access + refresh tokens)
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
| Serviço    | Imagem           | Porta  | Função                        |
|------------|------------------|--------|-------------------------------|
| postgres   | postgres:16      | 5432   | Banco de dados principal      |
| redis      | redis:7-alpine   | 6379   | Cache e filas                 |
| minio      | minio/minio      | 9000   | Storage S3-compatible         |
| minio-init | minio/mc         | —      | Cria buckets no boot          |
| backend    | build local      | 8000   | API Django Ninja              |
| frontend   | build local      | 3000   | SSR Nuxt 3                    |

---

## Arquitetura de Auth

### Fluxo de Login

```
[Browser] → GET /login
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

| Método | Path                        | Descrição                  |
|--------|-----------------------------|----------------------------|
| POST   | /api/auth/register/         | Criar conta                |
| POST   | /api/auth/token/            | Login (retorna JWT pair)   |
| POST   | /api/auth/token/refresh/    | Refresh do access token    |
| POST   | /api/auth/token/verify/     | Verificar validade token   |
| POST   | /api/auth/logout/           | Invalida refresh token     |
| GET    | /api/auth/me/               | Dados do usuário logado    |

### Endpoints Nuxt (BFF — server routes)

| Método | Path                        | Descrição                           |
|--------|-----------------------------|-------------------------------------|
| POST   | /api/auth/login             | Faz login, seta HttpOnly cookie     |
| POST   | /api/auth/register          | Registra novo usuário               |
| POST   | /api/auth/refresh           | Renova access_token via cookie      |
| POST   | /api/auth/logout            | Limpa cookie e invalida no backend  |
| GET    | /api/auth/me                | Retorna usuário logado (via token)  |

---

## Estrutura de Pastas

```
wolliz/
├── CLAUDE.md                   # Este arquivo
├── front-end/
│   ├── Dockerfile
│   ├── package.json
│   ├── nuxt.config.ts
│   ├── app.vue
│   ├── pages/
│   │   ├── index.vue           # Home (pública)
│   │   └── auth/
│   │       ├── login.vue       # Página de login
│   │       └── register.vue    # Página de cadastro
│   ├── stores/
│   │   └── auth.ts             # Pinia store de autenticação
│   ├── composables/
│   │   └── useAuth.ts          # Composable com helpers de auth
│   ├── middleware/
│   │   └── auth.ts             # Middleware de proteção de rotas
│   └── server/
│       └── api/
│           └── auth/
│               ├── login.post.ts
│               ├── register.post.ts
│               ├── refresh.post.ts
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
│       └── users/
│           ├── models.py       # User model customizado
│           ├── schemas.py      # Ninja schemas (input/output)
│           ├── api.py          # Ninja router
│           └── admin.py
└── infra/
    ├── docker/
    │   ├── docker-compose.yml
    │   └── .env.example
    └── k8s/                    # (futuro) manifests Kubernetes
```

---

## Modelo de Usuário

Campos do `User` customizado (`AbstractBaseUser`):

| Campo          | Tipo        | Descrição                     |
|----------------|-------------|-------------------------------|
| id             | UUID        | PK                            |
| email          | EmailField  | único, usado como login       |
| name           | CharField   | nome completo                 |
| phone          | CharField   | telefone (opcional)           |
| avatar         | ImageField  | foto de perfil (MinIO)        |
| is_active      | BooleanField| conta ativa                   |
| is_staff       | BooleanField| acesso ao admin Django        |
| created_at     | DateTimeField | data de criação             |
| updated_at     | DateTimeField | última atualização          |

---

## Variáveis de Ambiente

### Back-end (`.env`)
```
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DB_NAME=wolliz
DB_USER=wolliz
DB_PASSWORD=wolliz
DB_HOST=postgres
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_MEDIA=wolliz-media
MINIO_BUCKET_STATIC=wolliz-static
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ORIGINS=http://localhost:3000
ACCESS_TOKEN_LIFETIME_MINUTES=15
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Front-end (`.env`)
```
NUXT_API_BASE_URL=http://backend:8000       # server-side (dentro do Docker)
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000  # client-side
NUXT_PUBLIC_CDN_URL=http://localhost:9000/wolliz-static  # MinIO URL pública
```

---

## Decisões Técnicas

- **HttpOnly cookie para refresh token**: evita acesso via JS, protege contra XSS
- **Access token em memória (Pinia)**: não persiste em localStorage, mais seguro
- **BFF pattern (Nuxt server routes)**: o browser nunca chama o Django diretamente em auth
- **UUID como PK**: evita enumeração de IDs
- **Email como username**: mais natural para usuário final
- **MinIO**: S3-compatible self-hosted, fácil migração para AWS S3 em produção

---

## Comandos Úteis

```bash
# ── Início limpo (para sempre de um estado fresco) ─────────────────────────────
# Para tudo, remove volumes/imagens/orphans, recria .env se não existir e sobe tudo rebuilt
cd infra/docker && ([ -f .env ] || cp .env.example .env) && docker compose down -v --rmi all --remove-orphans && docker compose up --build --force-recreate -d && docker compose logs -f

# ── Dia a dia ─────────────────────────────────────────────────────────────────
# Subir (sem rebuild)
cd infra/docker && docker compose up -d

# Parar tudo (mantém volumes/dados)
cd infra/docker && docker compose down

# Ver logs de todos os serviços
cd infra/docker && docker compose logs -f

# Ver logs de um serviço específico
cd infra/docker && docker compose logs -f backend

# ── Django ────────────────────────────────────────────────────────────────────
# Rodar migrations
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py migrate

# Criar superusuário
docker compose -f infra/docker/docker-compose.yml exec backend python manage.py createsuperuser

# Adicionar dependência Python
cd back-end && uv add nome-do-pacote

# ── URLs ──────────────────────────────────────────────────────────────────────
# Frontend:      http://localhost:3000
# Backend docs:  http://localhost:8000/api/docs
# MinIO console: http://localhost:9001  (minioadmin / minioadmin)
```
