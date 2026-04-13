FROM node:22-alpine

WORKDIR /app

# Instala dependências
COPY package.json package-lock.json* ./
RUN npm install

# Copia o código (em dev o volume sobrescreve, mas necessário para build)
COPY . .

EXPOSE 3000
