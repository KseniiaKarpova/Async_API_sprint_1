GIT: [https://github.com/KseniiaKarpova/Async_API_sprint_1](https://github.com/KseniiaKarpova/Async_API_sprint_1)
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
[http://127.0.0.1:8080/api/openapi](http://127.0.0.1:8080/api/openapi)

Пример:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8080/api/v1/persons/6dd77305-18ee-4d2e-9215-fd1a496ccfdf/film' \
  -H 'accept: application/json'
```
