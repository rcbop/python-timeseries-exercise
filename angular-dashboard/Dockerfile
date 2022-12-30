FROM node:16-alpine AS build
WORKDIR /app
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm install
COPY dashboard/. .
RUN npm run build:docker

FROM nginx:alpine
COPY --from=build /app/dist/dashboard/. /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
