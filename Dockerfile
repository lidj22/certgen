FROM nginx:latest

COPY ./out/server.crt /etc/nginx/ssl/server.crt
COPY ./out/server.key /etc/nginx/ssl/server.key

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf