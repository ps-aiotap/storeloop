# Service Separation Guide

## Docker Compose Files Fixed

**AT Identity:**
```yaml
# at_identity/docker-compose.yml
version: '3'
services:
  web:
    build: .
    restart: always
    env_file:
      - ./.env
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn core.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8001:8000"
    network_mode: "host"

volumes:
  static_volume:
  media_volume:
```

**StoreLoop:**
```yaml
# storeloop/docker-compose.yml
version: '3'
services:
  web:
    build: .
    restart: always
    env_file:
      - ./.env
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn core.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8000:8000"
    network_mode: "host"

  nginx:
    image: nginx:1.21
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - static_volume:/var/www/html/static
      - media_volume:/var/www/html/media
    depends_on:
      - web
    restart: always
    network_mode: "host"

volumes:
  static_volume:
  media_volume:
```

**Artisan CRM:**
```yaml
# artisan_crm/docker-compose.yml
version: '3'
services:
  web:
    build: .
    restart: always
    env_file:
      - ./.env
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    command: >
      sh -c "python manage.py migrate &&
             gunicorn core.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8002:8000"
    network_mode: "host"
    environment:
      - DB_HOST=localhost
      - AT_IDENTITY_URL=http://localhost:8001/api/

volumes:
  static_volume:
  media_volume:
```

## Key Fixes:
1. **Fixed port binding** - Container binds to 8000, host maps to service port
2. **Added network_mode: "host"** - Allows container to access localhost DB
3. **Added DB_HOST=localhost** - Points to local PostgreSQL
4. **Removed nginx from AT Identity/CRM** - Only StoreLoop needs it
5. **Added AT_IDENTITY_URL** - For service communication