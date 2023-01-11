FROM node:16-alpine AS base
WORKDIR /app
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm install
COPY dashboard/. .

FROM zenika/alpine-chrome:with-node AS test
USER root
WORKDIR /app
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm install
COPY dashboard/. .
RUN chown -R chrome:chrome /app
USER chrome

FROM base AS build
RUN npm run build:docker

FROM nginx:alpine AS prod
COPY --from=build /app/dist/dashboard/. /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
