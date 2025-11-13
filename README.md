# MAX Productivity Bot

A productivity enhancement chatbot for MAX messenger.

## Features
- Task management
- Productivity statistics
- Interactive menu interface

## Local Setup

1. Clone repository:
```bash
   git clone <your-repo-url>
   cd max-productivity-bot
```

2. Create virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Configure environment:
   Create `.env` file with:
```
   BOT_TOKEN=your_token_here
```

5. Run bot:
```bash
   python3 bot.py
```

## Docker Setup

1. Build image:
```bash
   docker build -t max-productivity-bot .
```

2. Run container:
```bash
   docker run -e BOT_TOKEN=your_token_here max-productivity-bot
```

## Requirements
- Python 3.11+
- Dependencies listed in requirements.txt
