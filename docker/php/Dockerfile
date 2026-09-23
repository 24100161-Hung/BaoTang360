FROM php:8.3-fpm-alpine

# Cài dependencies hệ thống
RUN apk add --no-cache \
    git curl unzip bash \
    icu-dev oniguruma-dev libzip-dev \
    freetype-dev libjpeg-turbo-dev libpng-dev \
    nodejs npm \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql mbstring bcmath intl zip gd opcache

# Cài Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Cấu hình PHP
RUN echo "upload_max_filesize = 50M" > /usr/local/etc/php/conf.d/uploads.ini \
    && echo "post_max_size = 50M" >> /usr/local/etc/php/conf.d/uploads.ini \
    && echo "memory_limit = 512M" >> /usr/local/etc/php/conf.d/uploads.ini

WORKDIR /var/www/html

# Copy source (chỉ lần đầu, sau đó dùng volume)
COPY backend/ .

# Cài dependencies
RUN composer install --no-dev --optimize-autoloader --no-interaction || true

# Phân quyền
RUN chown -R www-data:www-data storage bootstrap/cache || true

EXPOSE 9000

CMD ["php-fpm"]