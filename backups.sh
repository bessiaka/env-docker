#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Создание бэкапа базы данных..."
docker-compose exec -T mysql mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" bitrix24_db | gzip > "$BACKUP_DIR/database.sql.gz"

echo "Создание бэкапа файлов..."
tar --exclude='./html/bitrix/cache' \
    --exclude='./html/bitrix/managed_cache' \
    --exclude='./html/upload/tmp' \
    -czf "$BACKUP_DIR/files.tar.gz" html/

echo "Бэкап конфигураций..."
tar -czf "$BACKUP_DIR/configs.tar.gz" confs/ docker-compose.yml .env

echo "Бэкап завершен: $BACKUP_DIR"