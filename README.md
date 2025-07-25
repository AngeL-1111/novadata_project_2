# 🚀 PROJECT 2 (kafka streaming)

## 🛠 Используемые технологии
- **Docker**
- **Kafka**
- **PostgreSQL**
- **ClickHouse**
- **DBeaver**

______________________________________________________________________________________
## 📌 Этапы работы
### 1️⃣ Развертывание `docker-compose` файла
Настроим контейнеры и поднимем сервисы
- `docker compose up -d`

### 2️⃣ Создание первой пары `producer`-`consumer` и наполнение таблицы user_logins в PostgreSQL
Находясь в дирректории проекта:
- `python producer_to_pg.py` запускаем продюсер для стриминга в PG;
- `python consumer_to_pg.py` запускаем консюмер для стриминга в PG; (в соседнем терминале)
- в DBeaver подключаемся к базе PG и смотрим наполенение таблицы `user_logins`:
    `SELECT * FROM public.user_logins;` Проверяем наличие поля `sent_to_kafka` и его наполнение `False` значениями по дефолту;
- в терминале, где был запущен консюмер, останавляем его командой `control + C`;

### 3️⃣ Создание новой пары `producer`-`consumer` для миграции таблицы uз PG в ClickHouse
- `python producer_from_pg_to_ch.py` запускаем продюсер для стриминга из PG в Клик;
- `python consumer_from_pg_to_ch.py` запускаем консюмер для стриминга из PG в Клик; (в соседнем терминале)
- в DBeaver подключаемся к базе CH и смотрим наполенение таблицы `user_logins`:
    `SELECT * FROM default.user_logins;` Проверяем на отсутствие дубликатов и полное соответствие по количеству строк с таблицей в PG;
- в терминале, где был запущен консюмер, останавляем его командой `control + C`;

______________________________________________________________________________________