# Запуск проекта
### 1 step

create **.env** file based on **.env.example**<br>

### 2 step
Сборка проекта
```bash
docker-compose up -d --build
```

### 3 step
Заполнение базы данных из sqlite в Postgres

```bash
curl -XGET http://0.0.0.0:8888/migrate
```

### 4 step
Посмотреть результат загрузки данных через Админку
```bash
curl -XGET http://127.0.0.1/api/v1/movies/
```


### 5 step
Swagger для FastApi: 
[http://0.0.0.0:7000/api/openapi](http://0.0.0.0:7000/api/openapi)

Пример:
```bash
curl -X 'GET' \
  'http://0.0.0.0:7000/api/v1/persons/6dd77305-18ee-4d2e-9215-fd1a496ccfdf/film' \
  -H 'accept: application/json'
```
