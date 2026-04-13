FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Copia o uv diretamente da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dependências de sistema (libpq para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia só o pyproject.toml primeiro para aproveitar cache de camada do Docker
COPY pyproject.toml .python-version ./

# Extrai deps do pyproject.toml e instala via uv (tudo em uma linha para o Docker não confundir com instruções)
RUN python3 -c "import tomllib; deps=tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']; open('/tmp/req.txt','w').write('\n'.join(deps))" \
    && uv pip install --system -r /tmp/req.txt

# Copia o restante do código
COPY . .

EXPOSE 8000
