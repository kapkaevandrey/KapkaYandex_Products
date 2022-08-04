# KapkaYandex Market
KapkaYandex_Products

![market_workflow](https://github.com/kapkaevandrey/KapkaYandex_Products/actions/workflows/market_workflow.yml/badge.svg)

### _Описание проекта_
> ***Малкольм Стивенсон Форбс***
>>То, за что вы платите, и то, что вы ожидаете получить, – не одно и то же.
>>
Бэкенд для веб-сервиса сравнения цен на товары. Учебный проект в рамках проектного задания для поступления в Школу бэкенд-разработки Яндекс.

### _Технологии_
 - __[Python 3.10.1](https://docs.python.org/3/)__
 - __[Fast API 0.78](https://fastapi.tiangolo.com/)__
 - __[FastAPI Users 10.0.7](https://fastapi-users.github.io/fastapi-users/10.0/)__
 - __[SQLAlchemy 1.4.37](https://www.sqlalchemy.org/)__
 - __[Alembic 1.8.0](https://alembic.sqlalchemy.org/en/latest/)__
 - __[Pydantic 1.9.1](https://alembic.sqlalchemy.org/en/latest/)__
 - __[Uvicron 0.17.6](https://www.uvicorn.org/)__
 - __[Docker](https://www.docker.com/)__


## _Как запустить проект_:
________________________________________
________________________________________

### _Локальный запуск_
________________________________________
Клонировать репозиторий и перейти в него в командной строке:
```bash
https://github.com/kapkaevandrey/KapkaYandex_Products.git
```

```bash
cd KapkaYandex_Products
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
python3 pip install -r requirements.txt
```

Заполните файл __.env__, предварительно создав его в главной директории проекта. Для примера в директории проекта есть файл ```example.env```

Пример заполнения для локального запуска
```
APP_TITLE=Market                                <----название приложения
APP_DESCRIPTION=application for                 <----описание приложения
DATABASE_URL=sqlite+aiosqlite:///./market.db    <---данные для подключения к БД
FIRST_SUPERUSER_EMAIL=king.arthur@camelot.bt    <---emai суперюзера который будет создан при первой инициалзации БД
FIRST_SUPERUSER_PASSWORD=guinevere              <---password суперюзера который будет создан при первой инициалзации БД
```
☑️ ___Примечание___: в приведённом выше примере в качестве БД используется **[SQLite](https://www.sqlite.org/index.html)** 
с асинхронным драйвером **[aiosqlite](https://pypi.org/project/aiosqlite/)**, драйвер присутствует в списке зависимостей (для реализации тестирования).


Выполните миграции Alembic
```shell
alembic upgrade head
```
Запустите приложение
```shell
uvicorn app.main:app
```
в режиме автоматического отслеживания изменений. Внимание работает **[watchgod](https://pypi.org/project/watchgod/)**
```shell
uvicorn app.main:app --reload
```
Документация к проекту будет доступна по адресу http://127.0.0.1:8000/docs или http://127.0.0.1:8000/redoc
### _Запуск в контейнере Docker_
________________________________________
Установите Docker, просто следуйте [инструкции](https://docs.docker.com/desktop/linux/install/) на официальном сайте.
Изучите файл [docker-compose.yml](https://github.com/kapkaevandrey/KapkaYandex_Products/blob/main/docker-compose.yml) в репозитории проекта. 

Обратите внимание, что сборка контейнера осуществляется с использованием 
готового образа ([15052016/market:latest](https://hub.docker.com/r/15052016/market)) расположенного на DockerHub. 

В проекте настроено __CI__ так что образ обновляется при каждом обновлении в репозитории. 
Подробности в файле [market_workflow](https://github.com/kapkaevandrey/KapkaYandex_Products/blob/main/.github/workflows/market_workflow.yml)

#### _Запуск с использованием готового образа_
Дополните файл __.env__ данными для создания базы данных PostgreSQL
```
POSTGRES_DB=market.db                           <----имя базы данных
POSTGRES_USER=postrges                          <----имя пользователя
POSTGRES_PASSWORD=postgres                      <----пароль пользователя
POSTGRES_PORT=5432                              <----порт доступа
```
Имя хоста в данном случае совпадает с именем контейнера **_db_**
В итоге в файле __.env__ имя переменной ```DATABASE_URL``` должно выглядеть примерно следующим образом:
```
DATABASE_URL==postgresql+asyncpg://db:postgres@postgres:5432/market.db
```
Выполните из директории с проектом команду:
```shell
docker-compose up
```
Документация к проекту будет доступна по адресу http://127.0.0.1/docs или http://127.0.0.1/redoc

#### _Запуск с использованием образа собранного из исходных файлов проекта_
Для такого подхода вам придётся изменить файл `docker-compose.yaml`
>Замените
>```yaml
> image: 15052016/market:latest
>```
>на
> ```yaml
> build: .
>```
В данном случае образ будет собран по образу `Dockerfile` в директории проекта.

Выполните из директории с проектом команду:
```shell
docker-compose up
```
Документация к проекту будет доступна по адресу http://127.0.0.1/docs или http://127.0.0.1/redoc
### _Описание работы сервиса и пользовательские роли_:
__________________________________________
Сервис позволяет создавать товары и категории образуя иерархическую древовидную структуру.
Каждый товар может быть прикреплён к определённой категории и, в свою очередь,
каждая категория может быть прикреплена к другой категории. Сервис позволяет отслеживать изменение цены 
как определённого товара,
так и определённой категории товаров. Последняя рассчитывается автоматически как среднеарифметическое значение 
цены всех товаров находящей в этой и всех дочерних категориях.
При удалении товаров или категорий цены обновляются автоматически.

_______________________________________________________
### _Пользовательские роли в сервисе_:
1. **Аноним :alien:**
2. **Аутентифицированный пользователь :sunglasses:**
3. **Администратор (superuser) :innocent:**
(Использование прав доступа отсутствует в задании, но вполне актуально для подобного сервиса)
> ***Бен Паркер*** 
>>С большой силой приходит большая ответственность.

### _Регистрация и получение токена_:
______________________________________
#### _Регистрация нового пользователя_:
>```/auth/register```
>
>Payload
>```json
>{
>"username": "MikeWazowski@monsters.inc",
>"password": "JamesP.Sullivan"
>}
>```
>Response sample (status code = 201)
>```json
>{
>"id": "3370b7f9-9cfd-4689-9ae3-11de51e28b70",
>"email": "MikeWazowski@monsters.inc",
>"is_active": true,
>"is_superuser": false,
>"is_verified": false
>}
>```
#### _Получение JWT токена_:
Получить токен вы можете используя **POST** с ```data``` содержащим поля ```username``` и ```password```
>```/auth/jwt/login```
>
>Пример запроса с использованием библиотеки requests
>```python
>import requests
>
>data = {
>    'username': 'MikeWazowski@monsters.inc',
>    'password': 'JamesP.Sullivan'
>}
>
>data = requests.post(
>    'http://127.0.0.1:8000/auth/jwt/login',
>    data=data
>)
>```
>Response sample (status code = 200) ```data.json()```
> ```json lines
> {
> "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMzM3MGI3ZjktOWNmZC00Njg5LTlhZTMtMTFkZTUxZTI4YjcwIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2NTQzNzExMzR9.ZmyiCND1aH2x0d29tFgn3inlF_Fmi2tywMVJLZgt2BM",
> "token_type": "bearer"
> }


### _Примеры запросов_:
_________________________________
Здесь могли быть примеры запросов, но они гораздо лучше описаны в сгенерированной документации. 

[host/docs]() - Swagger 

[host/redoc]() - Redoc

При локальном запуске http://127.0.0.1:8000/docs


________________________________

### Автор проекта:
#### Андрей ***Lucky*** Капкаев
>*Улыбайтесь - это всех раздражает :relaxed:.*
