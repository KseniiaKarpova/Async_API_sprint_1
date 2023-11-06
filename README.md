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

