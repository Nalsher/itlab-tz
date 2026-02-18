# Запуск проекта (Docker)

1. Клонируйте репозиторий и перейдите в папку проекта:

```
git clone <project-url>
cd <project-dir>
```

2. Создайте env файли по примеру .env.exmaple и заполните его данными
```
cp .env .env.example
```

3. Поднимите контейнеры
```
docker compose up --build -d
```

4. Для запуска celery выполните команду:
``` 
docker compose exec <django_service_name> celery -A itlabdjango.celery worker
```

---

# Таблица эндпоинтов API

| Метод | URL | Заголовки | Body | Описание | Ответ |
|-------|-----|-----------|------|----------|-------|
| POST | /api/register/ | — | `{ "username": "string", "email": "string", "password": "string" }` | Регистрация нового пользователя | `201 Created` с данными пользователя, `400` при ошибке |
| POST | /api/login/ | — | `{ "email": "string", "password": "string" }` | Авторизация пользователя и получение JWT | `200 OK` с токенами `access` и `refresh`, профилем и telegram_token; `401` при неверных данных |
| POST | /api/telegram/ | — | `{ "token": "string", "chat_id": "string" }` | Регистрация Telegram chat_id для уведомлений | `200 OK` при успешной регистрации, `401` при неверном токене |
| GET | /api/task/ | `Authorization: Bearer <token>` или `Chat-Id` | — | Получение списка задач текущего пользователя | `200 OK` с пагинацией: `results`, `count`, `total_pages`, `next`, `previous` |
| POST | /api/task/ | `Authorization: Bearer <token>` или `Chat-Id` | `{ "title": "string", "description": "string", "due_date": "YYYY-MM-DDTHH:MM:SS", "tags": ["string"] }` | Создание новой задачи | `201 Created` с данными задачи; ошибки при валидации `400` |
| GET | /api/task/{id}/ | `Authorization: Bearer <token>` или `Chat-Id` | — | Получение конкретной задачи пользователя | `200 OK` с данными задачи, `404` если не найдено |
| PUT | /api/task/{id}/ | `Authorization: Bearer <token>` или `Chat-Id` | `{ "title": "string", "description": "string", "due_date": "YYYY-MM-DDTHH:MM:SS", "tags": ["string"] }` | Полное обновление задачи | `200 OK` с обновлёнными данными, `403` если нет прав, `404` если не найдено |
| PATCH | /api/task/{id}/ | `Authorization: Bearer <token>` или `Chat-Id` | Частичные данные задачи | Частичное обновление задачи | `200 OK` с обновлёнными данными, `403` если нет прав, `404` если не найдено |
| DELETE | /api/task/{id}/ | `Authorization: Bearer <token>` или `Chat-Id` | — | Удаление задачи | `204 No Content` при успешном удалении, `403` если нет прав, `404` если не найдено |
| GET | /api/tag/ | `Authorization: Bearer <token>` | — | Получение списка тегов | `200 OK` с пагинацией и данными тегов |
| POST | /api/tag/ | `Authorization: Bearer <token>` | `{ "title": "string" }` | Создание нового тега | `201 Created` с данными тега, `400` при ошибке |
| PUT | /api/tag/{id}/ | `Authorization: Bearer <token>` | `{ "title": "string" }` | Обновление тега | `200 OK` с обновлёнными данными, `403` если нет прав, `404` если не найдено |
| DELETE | /api/tag/{id}/ | `Authorization: Bearer <token>` | — | Удаление тега | `204 No Content` при успешном удалении, `403` если нет прав, `404` если не найдено |

---

# Архитектура микросервиса и Telegram-бота

## 1. Общая структура проекта

Проект состоит из двух основных частей:  

1. **Backend (Django + DRF)**  
   - API для работы с пользователями, задачами и тегами.  
   - Асинхронная отправка уведомлений через Celery и Telegram.  
   - JWT + Telegram-token аутентификация.  
   - Фильтры, поиск и пагинация через DRF и django-filters.  

2. **Telegram-бот (Aiogram + Aiogram Dialog)**  
   - FSM для управления состояниями диалогов.  
   - Использует диалоговые окна (`Window`) для ввода данных и кнопок.  
   - Валидация пользовательского ввода на уровне хэндлеров.  
   - Асинхронные запросы к бэкенду через `aiohttp`.  

---

## 2. Backend архитектура

### 2.1 Модели

#### В качестве pk для сущностей task и tag используется time.time_ns(), я подумал что это будет уникально и не должно создавать колизиий при каких либо батч созадниях (хоть они тут и не используются) а если создания выполняются синхронно то это точно не создат проблем 
 
- **User**  
  - Расширение `AbstractUser`, добавлены `telegram_token` и `chat_id`.  
- **Task**  
  - Пользовательская задача с полями: `title`, `description`, `due_date`, `tags`, `user`.  
- **Tag**  
  - Теги для задач с уникальным `title`.  

### 2.2 Сериализация

- `TaskCreateUpdateSerializer` и `TaskReadSerializer` для раздельной сериализации создания и чтения.  
- `TagCreateUpdateSerializer` / `TagReadSerializer` – аналогично.  
- `RegisterSerializer`, `LoginSerializer`, `TokenRegistrySerializer` для работы с пользователями и токенами.  

### 2.3 Views и permissions

- Используется **ModelViewSet** с кастомной проверкой объектов (`has_object_permission`).  
- `get_user` позволяет работать с JWT или Telegram chat_id.  
- Асинхронная задача `due_date_notify` вызывается через Celery.  
- Валидация данных и обработка ошибок встроены в сериализаторы и вьюхи.  

### 2.4 Пагинация и фильтры

- `CustomPageNumberPagination` с полями: `current_page`, `total_pages`, `next`, `previous`.  
- Фильтры по тегам, заголовку и дате через `django-filters`.  
- Поиск через DRF `SearchFilter`.  

### 2.5 Celery

- Отправка уведомлений о сроках задач в Telegram через Celery и `aiogram.Bot`.  
- Поддержка ETA для отложенных сообщений.  

---

## 3. Telegram-бот

### 3.1 FSM и Dialogs

- Используется **Aiogram Dialog** для управления окнами:  
  - `StartStateGroup` – все состояния (главное меню, регистрация, создание задач, просмотр задач).  
  - `Window` + виджеты `Button`, `MessageInput`, `Start` для диалогов.  
  - `ResultFormatter` отображает сообщения о результате действий.  

### 3.2 Обработка данных

- Хэндлеры для ввода:
  - `title_handler`, `description_handler`, `date_handler`, `tags_handler`.  
- Асинхронные HTTP-запросы к бэкенду через `aiohttp`.  
- Результат действия (`result`) сохраняется в `dialog_manager.dialog_data` и отображается через `ResultFormatter`.  

### 3.3 Навигация

- Кнопки “Главная”, “Следующая/Предыдущая страница” и “Создать таску” управляют FSM.  
- Вся логика по пагинации и отображению задач вынесена в отдельные хэндлеры.  

---

## 4. Безопасность

- JWT-токены для API.  
- Проверка владельца задачи при обновлении/удалении (`has_object_permission`).  
- Telegram-token связывает пользователя с чат-ботом.  
- Валидация данных в сериализаторах и хэндлерах бота.  

---

## 5. Тестирование

**Backend**:  
  - Тесты на CRUD операций для Task и Tag.  
  - Тесты на регистрацию, логин и Telegram-token.  

---


# Сложности:
### Единственным моментом который можно было выделить это связь django + aiogram т.к не совсем было понятно нужно ли поднимать доп веб сервер с тг-ботом чтобы можно было огранизовать полноценную микросервисную архитектуру, я решил не поднимать доп веб сервер и обойтись отправкой хедеров с chat-id для доступа к эндпоинтам из телеграм бота

