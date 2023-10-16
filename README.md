# Сервис рецептов FOODGRAM 
### *Вкус жизни начинается здесь!*
Проект Foodgram это социальная сеть для обмена рецептами, в которой можно публиковать рецепты с аппетитными фото, добавлять чужие рецепты в избранное и подписываться на авторов, а также формировать список покупок для быстрого шоппинга. 

## Технологии
Проект **Foodgram** - это онлайн-сервис и API для него. 
Проект упакован в контейнеры. В файле `docker-compose.yml` настроен запуск проекта на удаленном сервере с помощью Docker Compose. 
Автоматизация деплоя проекта (CI/CD) настроена с применением Github Actions, pipeline составлена в файле `.github/workflow`.  
В проекте использованы следующие технологии: Python, Django, Django REST framework, Nginx, Gunicorn, Docker, PostgreSQL, CI/CD  

## Как запустить проект локально:
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Shubarina/foodgram-project-react.git
cd foodgram
```
2. Cоздать и активировать виртуальное окружение, обновить пакетный менеджер:
```
python3 -m venv env
```
* Если у вас Linux/macOS
    ```
    source env/bin/activate
    ```
* Если у вас windows
    ```
    source env/scripts/activate
    ```
3. Обновить пакетный менеджер и установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Выполнить миграции и запустить проект:
```
python3 manage.py migrate
python3 manage.py runserver
```
## Как развернуть проект на удаленном сервере


## Авторы
Анна Шубарина
