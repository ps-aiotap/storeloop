# StoreLoop Deployment Guide

This guide explains how to deploy StoreLoop to a production environment using Docker, Nginx, and PostgreSQL.

## Prerequisites

- A VPS or cloud server (e.g., AWS EC2, DigitalOcean Droplet, Linode)
- Docker and Docker Compose installed
- Domain name (optional but recommended)
- Basic knowledge of Linux, Docker, and networking

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/storeloop.git
cd storeloop
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your production settings:
- Set `DEBUG=False`
- Generate a strong `SECRET_KEY`
- Update `ALLOWED_HOSTS` with your domain name
- Configure database credentials
- Add Razorpay API keys
- Configure email settings
- Enable security settings

### 3. Set Up Nginx Configuration

Create the Nginx configuration directory:

```bash
mkdir -p nginx/conf.d
```

Create `nginx/conf.d/storeloop.conf`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /var/www/html/static/;
    }
    
    location /media/ {
        alias /var/www/html/media/;
    }
}
```

### 4. SSL Configuration (Optional but Recommended)

Install Certbot on your host machine:

```bash
apt-get update
apt-get install certbot python3-certbot-nginx
```

Obtain SSL certificate:

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Update Nginx configuration to use SSL:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /var/www/html/static/;
    }
    
    location /media/ {
        alias /var/www/html/media/;
    }
}
```

### 5. Build and Start the Services

```bash
docker-compose build
docker-compose up -d
```

### 6. Create a Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. Set Up Database Backups

Create a backup script `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/storeloop_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup the database
docker-compose exec -T db pg_dump -U storeloop_user storeloop > $BACKUP_FILE

# Compress the backup
gzip $BACKUP_FILE

# Delete backups older than 30 days
find $BACKUP_DIR -name "storeloop_*.sql.gz" -type f -mtime +30 -delete
```

Make the script executable:

```bash
chmod +x backup.sh
```

Add a cron job to run daily backups:

```bash
crontab -e
```

Add the following line:

```
0 2 * * * /path/to/storeloop/backup.sh
```

### 8. Monitoring and Logging

Set up monitoring with Prometheus and Grafana or use a service like Datadog or New Relic.

For logging, consider using the ELK stack (Elasticsearch, Logstash, Kibana) or a service like Loggly.

### 9. Updating the Application

To update the application:

```bash
git pull
docker-compose build
docker-compose down
docker-compose up -d
docker-compose exec web python manage.py migrate
```

## Scaling Considerations

### Horizontal Scaling

For higher traffic loads, consider:
- Using a load balancer (e.g., Nginx, HAProxy)
- Running multiple web containers
- Using a managed database service

### Vertical Scaling

Increase resources on your server:
- CPU
- RAM
- Disk space

## Troubleshooting

### Check Logs

```bash
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### Database Issues

Connect to the database:

```bash
docker-compose exec db psql -U storeloop_user -d storeloop
```

### Application Issues

Access the Django shell:

```bash
docker-compose exec web python manage.py shell
```

Run Django checks:

```bash
docker-compose exec web python manage.py check --deploy
```