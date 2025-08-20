FROM invoiceninja/invoiceninja:5

# Alpine Linux용 PostgreSQL 드라이버 설치
RUN apk add --no-cache \
    postgresql-dev \
    postgresql-client \
    && docker-php-ext-install pdo_pgsql pgsql
