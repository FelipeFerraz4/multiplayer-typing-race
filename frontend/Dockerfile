# ===== BUILD =====
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci
RUN npm install -g @angular/cli@21

COPY . .

RUN ng build --configuration=production

# ===== RUN SSR =====
FROM node:22-alpine

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY package*.json ./

RUN npm ci --omit=dev

EXPOSE 4000

CMD ["node", "dist/frontend/server/server.mjs"]
