# SuperMock Web UI Guide

## Overview

SuperMock Web UI provides a modern, browser-based interface for testing your Telegram bots. It offers real-time message display, statistics, and an intuitive chat interface.

## Features

- 🌐 **Modern Web Interface**: Clean, responsive design that works on desktop and mobile
- ⚡ **Real-time Updates**: WebSocket support for instant message delivery
- 📊 **Live Statistics**: Track message counts and bot activity
- 💬 **Chat Interface**: Telegram-like chat experience
- 🎨 **Beautiful Design**: Gradient themes and smooth animations
- 📱 **Mobile Responsive**: Works great on phones and tablets

## Quick Start

### Start Web UI

```bash
supermock web
```

The web interface will be available at:
- **Web UI**: http://localhost:8082
- **API Server**: http://localhost:8081

### Custom Ports

```bash
supermock web --port 8081 --webport 8082
```

### Public Access

```bash
supermock web --host 0.0.0.0 --webhost 0.0.0.0
```

## Using the Web UI

### 1. Open in Browser

Navigate to http://localhost:8082 in your web browser.

### 2. Configure Your Bot

Point your bot to the API server:

```python
from telegram.ext import Application

application = Application.builder() \
    .token("YOUR_TOKEN") \
    .base_url("http://localhost:8081/bot") \
    .build()
```

### 3. Start Chatting

1. Type a message in the input field at the bottom
2. Press **Send** or hit **Enter**
3. Your bot receives the message and can respond
4. Bot responses appear automatically in real-time

### 4. Monitor Activity

The right sidebar shows:
- Total message count
- User vs Bot message breakdown
- API endpoint URL
- Usage instructions

## Features in Detail

### Real-time Messages

Messages appear instantly thanks to WebSocket technology. No need to refresh!

### Message Types

The UI displays:
- **User messages**: Aligned right in purple bubbles
- **Bot messages**: Aligned left in white bubbles
- **Timestamps**: For each message

### Clear History

Click the **Clear** button to reset the conversation and start fresh.

### Statistics

Live statistics show:
- Total messages
- User messages sent
- Bot responses received

## API Endpoints

The Web UI communicates with these endpoints:

- `GET /` - Main web interface
- `GET /api/messages` - Get message history
- `POST /api/send` - Send user message
- `POST /api/callback` - Send callback query
- `POST /api/clear` - Clear message history
- `GET /api/stats` - Get statistics

## WebSocket Events

The Web UI uses Socket.IO for real-time communication:

- `connect` - Client connected
- `disconnect` - Client disconnected
- `new_message` - New message received
- `send_message` - Send message from client

## Screenshots

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🚀 SuperMock Web Interface               ● Connected        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                                              [TestUser 10:30]│
│                                         ┌───────────────────┐│
│                                         │ Hello bot!        ││
│                                         └───────────────────┘│
│                                                              │
│ [MockBot 10:30]                                             │
│ ┌────────────────────────────┐                              │
│ │ Hi! How can I help you?    │                              │
│ └────────────────────────────┘                              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Type your message...                     [Send]    [Clear]  │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Port Already in Use

If port 8082 is already in use, specify a different port:

```bash
supermock web --webport 8083
```

### Connection Issues

1. Ensure the API server is running
2. Check firewall settings
3. Verify the ports are not blocked
4. Try using `--host 0.0.0.0` for network access

### Messages Not Appearing

1. Check browser console for errors (F12)
2. Verify WebSocket connection in Network tab
3. Ensure your bot is configured correctly
4. Try refreshing the page

## Advanced Usage

### Multiple Bots

You can test multiple bots simultaneously by:
1. Starting SuperMock on different ports
2. Opening multiple browser tabs
3. Each bot connects to its own instance

### Integration Testing

The Web UI can be used alongside automated tests:

```python
# Start web UI
# Open browser to http://localhost:8082
# Run your test suite
# Watch the interaction in real-time
```

### Remote Testing

For testing from other devices on your network:

```bash
supermock web --host 0.0.0.0 --webhost 0.0.0.0
```

Then access from another device using your computer's IP:
```
http://192.168.1.100:8082
```

## Tips & Tricks

1. **Keep the Web UI open** while developing for instant feedback
2. **Use multiple browser windows** to test complex scenarios
3. **Check the statistics** to monitor bot performance
4. **Clear history** between test runs for clean tests
5. **Use the API URL** from the sidebar to quickly copy the endpoint

## Comparison: Terminal vs Web UI

| Feature | Terminal UI | Web UI |
|---------|------------|--------|
| Interface | Text-based | Graphical |
| Accessibility | Terminal only | Any browser |
| Real-time | Yes | Yes |
| Statistics | Basic | Detailed |
| Mobile Support | No | Yes |
| Multiple Users | No | Yes |
| Screenshots | No | Yes |

## Next Steps

- Try the [Terminal UI](../README.md#2-start-interactive-terminal-chat) for CLI-based testing
- Check out [Docker deployment](DOCKER.md) for production use
- Read the [API documentation](../README.md) for more details

---

Made with ❤️ for Telegram Bot Developers
