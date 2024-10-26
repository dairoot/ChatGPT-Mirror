FROM node:22-slim AS builder

WORKDIR /app

COPY ./frontend/package.json ./frontend/package.json
COPY ./frontend/package-lock.json ./frontend/package-lock.json

RUN cd frontend && npm install 

COPY ./frontend/ ./frontend/

RUN cd frontend && npm run build

FROM python:3.12-alpine

LABEL maintainer="dairoot"

WORKDIR /app

ENV DJANGO_ENV=PRODUCTION

RUN apk add --update caddy

COPY ./backend/requirements.txt ./backend/requirements.txt

RUN cd backend && pip install -U pip && pip install -r requirements.txt

COPY ./backend/ ./backend/

COPY ./Caddyfile /app/Caddyfile

COPY --from=builder /app/frontend/dist ./frontend/dist

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 50002

CMD ["/usr/local/bin/entrypoint.sh"]

