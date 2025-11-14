# SuperMock Features Guide

Complete guide to all SuperMock features and capabilities.

## Overview

SuperMock is a comprehensive local Telegram Bot API mock server that enables developers to test their bots without connecting to the real Telegram API. It supports all major bot testing scenarios.

## Testing Interfaces

### 1. Terminal UI
Command-line interactive chat interface.

```bash
supermock chat
```

**Features:**
- Real-time message display
- Bot response monitoring
- Colored message bubbles
- Keyboard interaction

### 2. Web UI
Modern browser-based interface with real-time updates.

```bash
supermock web
```

**Features:**
- Beautiful responsive design
- WebSocket for real-time updates
- Live statistics dashboard
- Mobile support
- Connection status indicator

### 3. Server Mode
Headless API server for automated testing.

```bash
supermock server
```

**Use Cases:**
- CI/CD pipelines
- Automated test suites
- Integration testing
- Development without UI

## Bot Testing Scenarios

### Private Chats

Test one-on-one interactions with your bot.

**Supported:**
- Text messages
- Media (photos, videos, audio, voice)
- Documents and stickers
- Locations and polls
- Inline keyboards
- Message editing and deletion

**Example:**
```python
from supermock.api import TelegramMockServer

server = TelegramMockServer()
server.send_user_message("Hello bot!")
```

### Group Chats (NEW!)

Test your bot in multi-user group scenarios.

**Supported:**
- Multiple users simulation
- Group commands with @mentions
- Member join/leave events
- Group statistics
- Role-based interactions

**Example:**
```python
from supermock.utils import GroupChatSimulator

group_sim = GroupChatSimulator(server)
group_id = group_sim.create_group("Test Group", member_count=5)
group_sim.send_group_message(group_id, "Hello everyone!")
group_sim.send_group_command(group_id, "/start", mention_bot=True)

# Simulate events
new_user = {"id": 99999, "first_name": "NewUser"}
group_sim.simulate_user_joined(group_id, new_user)
```

### Inline Mode (NEW!)

Test inline queries when users type @botname in any chat.

**Supported:**
- Inline query simulation
- Results handling
- Chosen result callbacks
- Results caching
- Inline message editing

**Example:**
```python
from supermock.utils import InlineModeSimulator

inline_sim = InlineModeSimulator(server)
inline_sim.send_inline_query("search term")
inline_sim.send_chosen_inline_result("result_id", "query")
```

## API Methods

### Core Methods (10)
- `getMe` - Bot information
- `getUpdates` - Long polling
- `setWebhook` - Webhook setup
- `deleteWebhook` - Webhook removal
- `getWebhookInfo` - Webhook info
- `sendChatAction` - Typing indicators
- `getChatMember` - Member info
- `getChat` - Chat information
- `deleteMessage` - Delete messages
- `editMessageReplyMarkup` - Edit keyboards

### Messaging (9)
- `sendMessage` - Text messages
- `sendPhoto` - Photos
- `sendVideo` - Videos
- `sendAudio` - Audio files
- `sendVoice` - Voice messages
- `sendDocument` - Documents
- `sendSticker` - Stickers
- `sendLocation` - Locations
- `sendPoll` - Polls

### Message Management (2)
- `editMessageText` - Edit text
- `answerCallbackQuery` - Button callbacks

### Inline Mode (3) NEW!
- `answerInlineQuery` - Answer queries
- `editMessageTextInline` - Edit inline messages
- `editMessageReplyMarkupInline` - Edit inline keyboards

**Total: 28+ API methods**

## Configuration

### YAML Configuration

```yaml
server:
  host: localhost
  port: 8081
  debug: false

bot:
  id: 123456789
  first_name: MyBot
  username: my_bot

logging:
  enabled: true
  level: INFO
  file: supermock.log

features:
  save_history: true
  history_file: .supermock_history.json
```

### JSON Configuration

```json
{
  "server": {
    "host": "localhost",
    "port": 8081
  },
  "bot": {
    "first_name": "MyBot",
    "username": "my_bot"
  }
}
```

## History Management

### Save Conversations

```python
from supermock.utils import HistoryManager

history_mgr = HistoryManager(".history.json")
history_mgr.save_history(messages)
```

### Load Previous Sessions

```python
messages = history_mgr.load_history()
```

### Export Formats

```python
# Export to text
history_mgr.export_history("chat.txt", format="txt")

# Export to JSON
history_mgr.export_history("chat.json", format="json")
```

## Docker Deployment

### Using Docker

```bash
docker build -t supermock .
docker run -p 8081:8081 supermock
```

### Using Docker Compose

```bash
docker-compose up -d
```

### Environment Variables

- `SUPERMOCK_HOST` - Server host (default: 0.0.0.0)
- `SUPERMOCK_PORT` - Server port (default: 8081)

## Library Compatibility

### python-telegram-bot

```python
from telegram.ext import Application

app = Application.builder() \
    .token("YOUR_TOKEN") \
    .base_url("http://localhost:8081/bot") \
    .build()
```

### aiogram

```python
from aiogram import Bot

bot = Bot(
    token="YOUR_TOKEN",
    base_url="http://localhost:8081/bot{token}"
)
```

### pyTelegramBotAPI (telebot)

```python
import telebot

telebot.apihelper.API_URL = "http://localhost:8081/bot{0}/{1}"
bot = telebot.TeleBot("YOUR_TOKEN")
```

## Testing Examples

### Unit Testing

```python
import pytest
from supermock.api import TelegramMockServer

@pytest.fixture
def server():
    return TelegramMockServer(port=8082)

def test_bot_response(server):
    server.send_user_message("/start")
    # Assert bot behavior
```

### Integration Testing

```python
# Start server
server = TelegramMockServer()
thread = threading.Thread(target=server.run, daemon=True)
thread.start()

# Run bot
# Test interactions
# Verify results
```

## Best Practices

1. **Use Different Ports**: Use unique ports for each test to avoid conflicts
2. **Clear History**: Clear message history between tests
3. **Mock Realistic Data**: Use realistic user IDs and names
4. **Test Edge Cases**: Test with empty strings, long texts, special characters
5. **Verify Responses**: Always check bot responses in message history
6. **Use Examples**: Start with provided examples and modify them

## Troubleshooting

### Port Already in Use

```bash
supermock server --port 8082
```

### Bot Not Responding

1. Check if SuperMock is running
2. Verify bot's base_url configuration
3. Check message history for errors

### WebSocket Connection Failed

1. Ensure web server is running
2. Check browser console for errors
3. Verify firewall settings

## Performance

- **Concurrent Requests**: Supports multiple concurrent connections
- **Message Queue**: Efficient queue-based update delivery
- **Memory Usage**: Minimal memory footprint
- **Response Time**: Near-instant message processing

## Limitations

- No actual file uploads/downloads (simulated)
- No real network requests to Telegram
- Limited to configured bot personality
- No rate limiting (by design)

## Future Features

- Advanced metrics dashboard
- File upload/download simulation
- API rate limiting simulation
- Custom event triggers
- Bot behavior recording/playback
- Performance profiling

---

For more information, see:
- [README.md](README.md) - Main documentation
- [WEB_UI.md](WEB_UI.md) - Web interface guide
- [DOCKER.md](DOCKER.md) - Docker deployment
- [QUICK_START.md](QUICK_START.md) - Quick start guide
