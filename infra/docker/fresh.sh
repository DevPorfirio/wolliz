#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

[ -f .env ] || cp .env.example .env

docker compose down -v --rmi all --remove-orphans
docker compose up --build --force-recreate -d

echo "Aguardando backend ficar pronto..."
until docker compose exec backend python manage.py migrate --check > /dev/null 2>&1; do
  sleep 2
done

docker compose exec backend python manage.py migrate

docker compose logs -f
