# SuperMock - Local Telegram Bot API Mock Server

**SuperMock** is a powerful local mock server for testing Telegram bots without connecting to the real Telegram API. It provides a complete mock implementation of the Telegram Bot API and includes an interactive terminal chat interface for manual testing.

## Features

- **Full Bot API Mock**: Implements 25+ Telegram Bot API endpoints
- **Multiple Testing Interfaces**: 
  - Interactive Terminal Chat
  - **Modern Web UI with WebSocket** (NEW!)
  - Programmatic API access
- **Long Polling Support**: Compatible with bots using `getUpdates`
- **Webhook Support**: Mock webhook endpoints for testing
- **Group Chat Simulation** (NEW!): Test your bot in group scenarios
- **Inline Mode Support** (NEW!): Test inline queries and results
- **Library Compatible**: Works with popular Telegram bot libraries:
  - `python-telegram-bot`
  - `aiogram`
  - `pyTelegramBotAPI` (telebot)
  - And any other library using standard Bot API
- **Testing Ready**: Perfect for automated testing and CI/CD pipelines
- **Web Interface**: Beautiful, real-time web UI with WebSocket support
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Easy Setup**: Simple installation and configuration
- **History Management**: Save, load, and export conversation history
- **Flexible Configuration**: YAML/JSON configuration files

## Installation

### From source:

```bash
git clone https://github.com/infernasel/SuperMock-1.git
cd SuperMock-1
pip install -e .
```

### Requirements:

- Python 3.7+
- Flask 2.0+
- Requests 2.25+

## Quick Start

### 1. Start the Mock Server (for automated testing)

```bash
supermock server
```

The server will start at `http://localhost:8081`

### 2. Start Interactive Terminal Chat

```bash
supermock chat
```

This will start both the mock server and an interactive terminal interface where you can chat with your bot.

### 3. Start Web-Based UI (NEW!)

```bash
supermock web
```

This starts both the API server and a modern web interface:
- **API Server**: http://localhost:8081
- **Web UI**: http://localhost:8082

Open the web UI in your browser for a beautiful, real-time chat interface!

See [WEB_UI.md](WEB_UI.md) for detailed web UI documentation.

### 3. Configure Your Bot

Point your bot to use the mock server instead of the real Telegram API:

#### For python-telegram-bot:

```python
from telegram.ext import Application

# Use the mock server URL
application = Application.builder() \
    .token("YOUR_TOKEN") \
    .base_url("http://localhost:8081/bot") \
    .build()
```

#### For aiogram:

```python
from aiogram import Bot, Dispatcher

# Use the mock server URL
bot = Bot(token="YOUR_TOKEN", 
          base_url="http://localhost:8081/bot{token}")
```

#### For pyTelegramBotAPI (telebot):

```python
import telebot

# Use the mock server URL
telebot.apihelper.API_URL = "http://localhost:8081/bot{0}/{1}"
bot = telebot.TeleBot("YOUR_TOKEN")
```

## Usage Examples

### Example 1: Simple Echo Bot Test

```python
# bot.py
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("Hello! I'm a test bot.")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    application = Application.builder() \
        .token("test_token") \
        .base_url("http://localhost:8081/bot") \
        .build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
```

**Terminal 1**: Start SuperMock
```bash
supermock chat
```

**Terminal 2**: Run your bot
```bash
python bot.py
```

Now you can interact with your bot in Terminal 1!

### Example 2: Automated Testing

```python
# test_bot.py
import pytest
from supermock.api import TelegramMockServer
import threading
import time

@pytest.fixture
def mock_server():
    """Setup mock server for testing"""
    server = TelegramMockServer(port=8082)
    thread = threading.Thread(target=lambda: server.run(), daemon=True)
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield server

def test_bot_responds_to_start(mock_server):
    """Test that bot responds to /start command"""
    # Send /start command
    mock_server.send_user_message("/start")
    
    # Wait for bot to process
    time.sleep(1)
    
    # Check messages history
    messages = mock_server.get_messages_history()
    
    # Find bot's response
    bot_messages = [m for m in messages if m["type"] == "bot"]
    assert len(bot_messages) > 0
    assert "Hello" in bot_messages[0]["message"]["text"]
```

## Supported API Methods

SuperMock currently supports the following Telegram Bot API methods:

**Core Methods:**
- `getMe` - Get bot information
- `getUpdates` - Receive incoming updates (long polling)
- `setWebhook` - Set webhook URL
- `deleteWebhook` - Delete webhook
- `getWebhookInfo` - Get webhook information

**Messaging:**
- `sendMessage` - Send text messages
- `sendPhoto` - Send photos
- `sendVideo` - Send videos
- `sendAudio` - Send audio files
- `sendVoice` - Send voice messages
- `sendDocument` - Send documents
- `sendSticker` - Send stickers
- `sendLocation` - Send location
- `sendPoll` - Send polls

**Message Management:**
- `editMessageText` - Edit text messages
- `editMessageReplyMarkup` - Edit message reply markup
- `deleteMessage` - Delete messages
- `answerCallbackQuery` - Answer callback queries from inline keyboards

**Chat Actions:**
- `sendChatAction` - Send chat actions (typing, uploading, etc.)
- `getChatMember` - Get chat member information
- `getChat` - Get chat information

More methods can be easily added as needed!

## Configuration Options

### Server Options

```bash
supermock server --host 0.0.0.0 --port 8080 --debug
```

- `--host`: Host to bind the server (default: localhost)
- `--port`: Port to bind the server (default: 8081)
- `--debug`: Enable Flask debug mode

### Chat Options

```bash
supermock chat --host localhost --port 8081
```

- `--host`: Host to bind the server (default: localhost)
- `--port`: Port to bind the server (default: 8081)

### Configuration File

You can use a configuration file (YAML or JSON) for more advanced settings:

```bash
supermock server --config supermock.config.yaml
```

Example `supermock.config.yaml`:

```yaml
server:
  host: localhost
  port: 8081
  debug: false

bot:
  id: 123456789
  first_name: CustomBot
  username: custom_bot

logging:
  enabled: true
  level: INFO
  file: supermock.log

features:
  save_history: true
  history_file: .supermock_history.json
```

See `supermock.config.yaml.example` for all available options.

## Docker Support

SuperMock can be easily deployed using Docker:

```bash
# Build the image
docker build -t supermock:latest .

# Run the container
docker run -d -p 8081:8081 --name supermock supermock:latest

# Or use Docker Compose
docker-compose up -d
```

See [DOCKER.md](DOCKER.md) for detailed instructions.

## Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Advanced Features

### Group Chat Simulation

Test your bot in group chat scenarios:

```python
from supermock.api import TelegramMockServer
from supermock.utils import GroupChatSimulator

# Start mock server
server = TelegramMockServer()

# Create group chat simulator
group_sim = GroupChatSimulator(server)

# Create a group with 5 members
group_id = group_sim.create_group("Test Group", member_count=5)

# Send a message in the group
group_sim.send_group_message(group_id, "Hello everyone!")

# Send a command with @mention
group_sim.send_group_command(group_id, "/start", mention_bot=True)

# Simulate user joining
new_user = {"id": 99999, "first_name": "NewUser", "username": "newuser"}
group_sim.simulate_user_joined(group_id, new_user)
```

See `examples/group_chat_bot.py` for a complete group chat bot example.

### Inline Mode Testing

Test inline queries and results:

```python
from supermock.api import TelegramMockServer
from supermock.utils import InlineModeSimulator

# Start mock server
server = TelegramMockServer()

# Create inline mode simulator
inline_sim = InlineModeSimulator(server)

# Send an inline query
inline_sim.send_inline_query("search term")

# Simulate user choosing a result
inline_sim.send_chosen_inline_result("result_id", "original query")
```

See `examples/inline_bot.py` for a complete inline bot example.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3 (GPLv3) - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need for local bot testing without API quotas
- Built to support the Telegram bot development community

## Support

For issues, questions, or contributions, please visit:
- GitHub Issues: https://github.com/infernasel/SuperMock-1/issues

---

Made for Telegram Bot Developers
