FROM nginx:alpine

RUN apk add --no-cache openssl

COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/certs \
    && openssl req -x509 -nodes -newkey rsa:2048 \
       -subj "/CN=localhost" \
       -keyout /etc/nginx/certs/legacy.key \
       -out /etc/nginx/certs/legacy.crt \
       -days 365 >/dev/null 2>&1