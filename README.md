# Payments System Django Interview

## Описание
Платежная система на Django REST Framework для обработки платежей и управления балансами организаций.

## Технологии
- Python 3.9
- Django 4.2
- Django REST Framework
- MySQL
- JWT Authentication

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте .env файл:
```
DATABASE_URL=mysql://user:password@localhost:3306/dbname
SECRET_KEY=your-secret-key
```
5. Примените миграции:
```bash
python manage.py migrate
```

## API Endpoints

### Аутентификация
- `POST /api/token/` - Получение JWT токена
- `POST /api/token/refresh/` - Обновление JWT токена

### Основные эндпоинты
- `POST /api/webhook/bank/` - Webhook для платежей
- `GET /api/organizations/{inn}/balance/` - Баланс организации

## JWT Аутентификация
- Access токен: 30 минут
- Refresh токен: 1 день
- Заголовок: `Authorization: Bearer <token>`

## Тестирование
```bash
pytest
```