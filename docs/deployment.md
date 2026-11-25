# Deployment

## Build Containers

```bash
docker compose build
```

## Start Containers

```bash
docker compose up
```

## Create Migrations

```bash
docker compose exec django python manage.py makemigrations
```

## Apply Migrations

```bash
docker compose exec django python manage.py migrate
```

## Create Superuser

```bash
docker compose exec django python manage.py createsuperuser
```

## Run Tests

```bash
docker compose exec django pytest
```

## Stop Containers

```bash
docker compose down
```