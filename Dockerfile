FROM nginx:latest

COPY ./nginx/nginx.conf /etc/nginx/conf.d/
COPY ./out/server.crt /etc/ssl/certs/
COPY ./out/server.key /etc/ssl/private

EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
