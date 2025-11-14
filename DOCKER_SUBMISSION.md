# Docker Submission - Лесной Фокус

## Информация о проекте

- Репозиторий: https://github.com/deleoningram/max-hackathon-bot-408
- Docker Hub: deleoningram/forest-focus-bot:latest
- Команда: CHAT-aclysm4

## Способы получения образа

### 1. Docker Hub
```bash
docker pull deleoningram/forest-focus-bot:latest
docker run -e BOT_TOKEN=your_token forest-focus-bot:latest
```

### 2. Сборка из исходников
```bash
git clone https://github.com/deleoningram/max-hackathon-bot-408.git
cd max-hackathon-bot-408
docker build -t forest-focus-bot .
docker run -e BOT_TOKEN=your_token forest-focus-bot
```

### 3. Загрузка tar.gz файла

Файл `forest-focus-bot.tar.gz`
```bash
gunzip forest-focus-bot.tar.gz
docker load -i forest-focus-bot.tar
docker run -e BOT_TOKEN=your_token forest-focus-bot:latest
```

## Требования

- Docker 20.10 или выше
- 512MB RAM минимум
- Токен бота MAX

## Тестовый запуск

Замените `YOUR_BOT_TOKEN` на реальный токен:
```bash
docker run --rm -e BOT_TOKEN=YOUR_BOT_TOKEN forest-focus-bot:latest
```

При успешном запуске вы увидите:
```
🤖 Лесной Фокус бот запускается...
✅ База данных инициализирована
🌱 Доступно растений: 12
🚀 Бот запущен!
```

## Структура образа

- Базовый образ: python:3.11-slim
- Размер: 149MB
- Порты: не требуются (bot-based)
- Volumes: /app/data
