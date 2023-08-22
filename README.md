# Дипломный проект
## Сервис рецептов FOODGRAM

```
https://shubanoid.hopto.org
```

### Описание
Вкус жизни начинается здесь!
Проект Foodgram это социальная сеть для обмена любимыми вкусными рецептами.
В сети можно публиковать рецепты Вашего кулинарного творчества, размещать аппетитные фото, создавать свой набор любимых блюд и формировать список покупок для быстрого шоппинга. 

### Технологии
Python 3.9
Django 3.2

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Shubarina/foodgram-project-react.git
```

```
cd foodgram
```

Cоздать и активировать виртуальное окружение:

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

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Авторы
Анна Шубарина

Суперпользователь:
login: superanna
email: shuba@mail.ru
password: 230983