![foodgram CI/CD workflow](https://github.com/Shadowmoses1314/foodgram-project-react/actions/workflows/foodgram_main.yml/badge.svg)


# Foodgram
___
Проект Foodgram - это онлайн-сервис и API для него.
___
## Стек:
- Python 3.7
- Django 3.2.6
- Django REST framework 3.12.4
- Nginx
- Docker
- Postgres


___
### Описание
**На этом сервисе пользователи смогут:**
- публиковать рецепты,
- подписываться на публикации других пользователей,
- добавлять рецепты в список «Избранное»,
- скачивать сводный список продуктов для приготовления одного или нескольких выбранных блюд.
___
### Установка и запуск
Для установки на локальной машине потребуется:
- Клонировать репозиторий
```
git clone  https://github.com/Shadowmoses1314/foodgram-project-react.git
```
- Зайти в главный репозиторий  

```
cd infra
```

##### Создайте файл _.env_ с переменными окружения для работы с базой данных
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
##### Запуск приложения
Перейти в директорию с проектом в папку с файлом docker-compose.yaml
Собрать контейнеры и запустить их
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

```
### Для репозитория настроен CI/CD.

**Для работы с удаленным сервером (на ubuntu):**

1. Сделайте Fork данного репозитория

2. Подготовьте vps с ubuntu и docker

- Выполните вход на свой удаленный сервер
  

- Установите docker на сервер:
```
sudo apt install docker.io 
```
- Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP

  
- Скопируйте файлы _docker-compose.yaml_ и _nginx.conf_ из вашего проекта на сервер 
  в _home/<ваш_username>/docker-compose.yaml_ и _home/<ваш_username>/nginx.conf_ соответственно.
```
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
- Cоздайте .env файл и впишите:
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
- Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
___
### Проверка работоспособности
Комманда `git push` является триггером workflow. 
После любого изменения в проекте выполните `git add .  && git commit -m "..." && git push`

проверить работоспособность сайта:
```
http://158.160.5.6/recipes
```

зайти в админку:
```
http://158.160.5.6/admin
```

### Почта и пароль суперюзера:
email:  `ShadowMoses1314@mail.ru `
Password: `Admin `


#### *Backend написан:*
[ShadowMoses1314](https://github.com/Shadowmoses1314)

