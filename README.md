# Сервис рецептов FOODGRAM - "Продуктовый помощник"

## Описание
### *Вкус жизни начинается здесь!*
Проект Foodgram это социальная сеть для обмена рецептами, в которой можно публиковать рецепты с аппетитными фото, добавлять чужие рецепты в избранное и подписываться на авторов, а также формировать список покупок для быстрого шоппинга. 

## Технологии
Проект **Foodgram** - это онлайн-сервис и API для него. В проекте использованы следующие технологии:    
Python 3.9  
Django 3.2  
Django REST framework  
Nginx  
Docker  

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
```
python3 -m pip install --upgrade pip
```
3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Выполнить миграции и запустить проект:
```
python3 manage.py migrate
python3 manage.py runserver
```

## Авторы
Анна Шубарина
