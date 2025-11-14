# SuperMock Examples

This directory contains example bots and test cases demonstrating how to use SuperMock.

## Examples

### 1. Echo Bot (`echo_bot.py`)

A simple bot that echoes back any message sent to it.

**How to run:**

1. Terminal 1 - Start SuperMock in chat mode:
   ```bash
   supermock chat
   ```

2. Terminal 2 - Run the echo bot:
   ```bash
   python examples/echo_bot.py
   ```

3. In Terminal 1, type messages and see the bot echo them back!

**Or for server-only mode:**

1. Terminal 1:
   ```bash
   supermock server
   ```

2. Terminal 2:
   ```bash
   python examples/echo_bot.py
   ```

### 2. Inline Keyboard Bot (`inline_keyboard_bot.py`)

A bot that demonstrates inline keyboard buttons.

**How to run:**

Same steps as Echo Bot, but run `inline_keyboard_bot.py` instead.

When you send `/start`, the bot will show you buttons to click.

### 3. Test Example (`test_example.py`)

Automated tests showing how to test bots with SuperMock.

**How to run:**

```bash
pytest examples/test_example.py -v
```

## Requirements

Before running the examples, make sure you have the required dependencies:

```bash
pip install -r requirements-dev.txt
```

This will install:
- SuperMock (flask, requests)
- python-telegram-bot (for the bot examples)
- pytest (for the test examples)

## Creating Your Own Bot

To create your own bot that works with SuperMock:

1. Install your preferred Telegram bot library
2. Configure the bot to use SuperMock's base URL:
   - For python-telegram-bot: `base_url="http://localhost:8081/bot"`
   - For aiogram: `base_url="http://localhost:8081/bot{token}"`
   - For pyTelegramBotAPI: `telebot.apihelper.API_URL = "http://localhost:8081/bot{0}/{1}"`
3. Start SuperMock: `supermock server` or `supermock chat`
4. Run your bot!

## Testing Your Bot

For automated testing:

```python
from supermock.api import TelegramMockServer
import threading
import time

# Start mock server
server = TelegramMockServer(port=8082)
thread = threading.Thread(target=lambda: server.run(), daemon=True)
thread.start()
time.sleep(1)

# Configure your bot to use http://localhost:8082
# Then run your test assertions

# Send test messages
server.send_user_message("/start")
time.sleep(0.5)

# Check bot responses
messages = server.get_messages_history()
assert len(messages) > 0
```
