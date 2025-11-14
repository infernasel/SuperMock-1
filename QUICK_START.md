# SuperMock Quick Start Guide

## Installation

```bash
git clone https://github.com/infernasel/SuperMock-1.git
cd SuperMock-1
pip install -e .
```

## Usage

### 1. Start the server only (for automated testing):

```bash
supermock server
```

Server will start at http://localhost:8081

### 2. Start interactive terminal chat:

```bash
supermock chat
```

This starts both the server and an interactive chat interface.

### 3. Configure your bot:

Point your bot to use SuperMock instead of real Telegram API:

**python-telegram-bot:**
```python
from telegram.ext import Application

app = Application.builder() \
    .token("YOUR_TOKEN") \
    .base_url("http://localhost:8081/bot") \
    .build()
```

**aiogram:**
```python
from aiogram import Bot

bot = Bot(token="YOUR_TOKEN", 
          base_url="http://localhost:8081/bot{token}")
```

**pyTelegramBotAPI:**
```python
import telebot

telebot.apihelper.API_URL = "http://localhost:8081/bot{0}/{1}"
bot = telebot.TeleBot("YOUR_TOKEN")
```

### 4. Run your bot:

```bash
python your_bot.py
```

Now you can test your bot locally without connecting to Telegram!

## Examples

See the `examples/` directory for complete working examples:
- `echo_bot.py` - Simple echo bot
- `inline_keyboard_bot.py` - Bot with inline buttons
- `test_example.py` - Automated testing example

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/
```

## License

Apache License 2.0 - see LICENSE file
