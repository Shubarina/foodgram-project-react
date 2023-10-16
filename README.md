# Сервис рецептов FOODGRAM 
### *Вкус жизни начинается здесь!*
Проект Foodgram это социальная сеть для обмена рецептами, в которой можно публиковать рецепты с аппетитными фото, добавлять чужие рецепты в избранное и подписываться на авторов, а также формировать список покупок для быстрого шоппинга. 

## Технологии
Проект **Foodgram** - это онлайн-сервис и API для него. 
Проект упакован в контейнеры. В файле `docker-compose.yml` настроен запуск проекта на удаленном сервере с помощью Docker Compose. 
Автоматизация деплоя проекта (CI/CD) настроена с применением Github Actions, pipeline составлена в файле `.github/workflow`.  
В проекте использованы следующие технологии: Python, Django, Django REST framework, Nginx, Gunicorn, Docker, PostgreSQL, CI/CD  

## Как запустить проект на удаленном сервере:
1. Клонируйте репозиторий:
```
git clone https://github.com/Shubarina/foodgram-project-react.git
```
2. На сервере установлен Docker и Docker Compose.
3. Скопируйте на сервер файлы `docker-compose.yml` и `nginx.conf` из директории infra. Отредактируйте данные IP своего сервера.
4. Создайте файл `.env` и впишите в него переменные:
   ```DB_ENGINE=<django.db.backends.postgresql>
      DB_NAME=<имя базы данных postgres>
      DB_USER=<пользователь бд>
      DB_PASSWORD=<пароль>
      DB_HOST=<db>
      DB_PORT=<5432>
      SECRET_KEY=<секретный ключ проекта django>
   ```
6. На сервере соберите docker-compose и после успешного запуска соберите статику, примените миграции и создайте суперпользователя:
   ```
   sudo docker-compose up -d --build
   sudo docker-compose exec backend python manage.py collectstatic
   sudo docker-compose exec backend python manage.py migrate
   sudo docker-compose exec backend python manage.py createsuperuser
   ```
7. Для работы с Github Actions необходимо создать переменные окружения в разделе Secrets репозитория проекта:
   ```
   SECRET_KEY              # секретный ключ Django проекта
   DOCKER_PASSWORD         # пароль от Docker Hub
   DOCKER_USERNAME         # логин Docker Hub
   HOST                    # публичный IP сервера
   USER                    # имя пользователя на сервере
   PASSPHRASE              # *если ssh-ключ защищен паролем
   SSH_KEY                 # приватный ssh-ключ
   TELEGRAM_TO             # ID телеграм-аккаунта для отправки сообщения
   TELEGRAM_TOKEN          # токен бота, посылающего сообщение
   ```
   **Запуск workflow стартует после каждого обновления репозитория (push в ветку master)**
   
## Авторы
Анна Шубарина
