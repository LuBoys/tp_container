# Un autre langage pour le deuxième microservice : PHP.
FROM php:8.4-cli-alpine

WORKDIR /app

# Le volume sera monté ici pour conserver les scores.
RUN mkdir -p /data && chown www-data:www-data /data
COPY --chown=www-data:www-data index.php .

USER www-data
EXPOSE 8081
CMD ["php", "-S", "0.0.0.0:8081", "index.php"]
