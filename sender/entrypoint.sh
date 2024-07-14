#!/bin/sh

# Проверяем доступность базы данных перед выполнением миграций
echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Выполнение миграций (на случай, если их нужно выполнить при запуске контейнера)
python manage.py migrate --noinput

# Запуск приложения
exec "$@"
