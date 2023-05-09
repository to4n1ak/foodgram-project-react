# FOODGRAM

IP: 51.250.19.14


### Проект домашнего задания Яндекс.Практикум
«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Как запустить проект:
- Клонируем репозиторий и переходим в него:
git git clone git@github.com:to4n1ak/foodgram-project-react.git
cd foodgram-project-react

- Создаем и активируем виртуальное окружение:
python3 -m venv venv
source /venv/bin/activate (source /venv/Scripts/activate - для Windows)
python -m pip install --upgrade pip

- Ставим зависимости из requirements.txt:
pip install -r requirements.txt

- Переходим в папку с файлом docker-compose.yaml:
cd infra

- Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
docker-compose up -d --build

- Выполняем миграции:
docker-compose exec web python manage.py makemigrations reviews
docker-compose exec web python manage.py migrate

- Создаем суперпользователя:
docker-compose exec web python manage.py createsuperuser

- Собираем статику:
docker-compose exec web python manage.py collectstatic --no-input

- Создаем дамп базы данных (нет в текущем репозитории):
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json

- Останавливаем контейнеры:
docker-compose down -v
