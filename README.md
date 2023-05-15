# praktikum_new_diplom
```
docker-compose up -d
```

Запустить миграции и т.д.:

```
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py createsuperuser

docker-compose exec backend python manage.py collectstatic --no-input 

docker-compose exec backend python manage.py import_ings ingredients.csv

docker-compose exec backend python manage.py import_tags tags.csv

docker-compose exec backend python manage.py import_recipes recipes.csv
```
# .env
```
SECRET_KEY='secret_key'
DEBUG=False 
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```