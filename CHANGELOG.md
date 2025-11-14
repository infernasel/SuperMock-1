# Changelog

All notable changes to SuperMock will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - v0.3.0

### Added
- **Web-Based UI**: Modern, browser-based interface for testing bots
  - Beautiful responsive design with gradient themes
  - Real-time message updates via WebSocket (Socket.IO)
  - Live statistics dashboard
  - Telegram-like chat interface
  - Mobile responsive design
  - Connection status indicator
  - Clear conversation feature

- **WebSocket Support**:
  - Socket.IO integration for real-time bidirectional communication
  - Automatic reconnection handling
  - Message broadcasting to all connected clients
  - Live message monitoring

- **Group Chat Simulation** (NEW):
  - Create and manage group chats
  - Simulate multiple users in groups
  - Send group messages and commands
  - Handle @mentions in groups
  - Member join/leave events
  - Group statistics and info

- **Inline Mode Support** (NEW):
  - Simulate inline queries (@botname query)
  - Handle inline results
  - Chosen inline result callbacks
  - Inline results caching
  - Support for inline message editing

- **New API Endpoints**:
  - `answerInlineQuery` - Answer inline queries
  - `editMessageTextInline` - Edit inline messages
  - `editMessageReplyMarkupInline` - Edit inline message markup

- **New CLI Command**:
  - `supermock web` - Start web-based UI
  - Custom port configuration for web UI (--webport)
  - Separate web host configuration (--webhost)

- **Web API Endpoints**:
  - `GET /` - Main web interface
  - `GET /api/messages` - Get message history
  - `POST /api/send` - Send user message
  - `POST /api/callback` - Send callback query
  - `POST /api/clear` - Clear message history
  - `GET /api/stats` - Get server statistics

- **Examples**:
  - `group_chat_bot.py` - Group chat bot demonstration
  - `inline_bot.py` - Inline mode bot demonstration

- **Documentation**:
  - Comprehensive WEB_UI.md guide
  - Usage examples for web interface
  - Screenshots and feature descriptions
  - Troubleshooting section

- **Testing**:
  - 9 new tests for group chat and inline mode
  - Total test count: 23 tests (100% passing)

### Changed
- Updated dependencies to include flask-socketio and flask-cors
- Enhanced CLI help text with web UI examples
- Updated README with web UI and new features information
- Expanded utils module with GroupChatSimulator and InlineModeSimulator

### Technical
- WebUIServer class for managing web interface
- Real-time message monitoring thread
- HTML/CSS/JavaScript frontend with modern design
- WebSocket event handlers for bidirectional communication
- GroupChatSimulator for testing group scenarios
- InlineModeSimulator for testing inline bots

## [0.2.0] - 2025-11-08

### Added
- **Extended API Support**: Added 15+ new Telegram Bot API methods
  - `sendVideo` - Send video messages
  - `sendAudio` - Send audio files
  - `sendVoice` - Send voice messages
  - `sendSticker` - Send stickers
  - `sendLocation` - Send location data
  - `sendPoll` - Send polls
  - `deleteMessage` - Delete messages
  - `editMessageReplyMarkup` - Edit inline keyboards
  - `sendChatAction` - Send typing indicators
  - `getChatMember` - Get chat member info
  - `getChat` - Get chat information

- **Configuration System**: 
  - YAML and JSON configuration file support
  - Configurable bot and user settings
  - Logging configuration
  - Feature flags

- **History Management**:
  - Save conversation history to JSON
  - Load previous conversations
  - Export history to TXT or JSON formats
  - Clear history functionality

- **Docker Support**:
  - Dockerfile for containerization
  - docker-compose.yml for easy deployment
  - Comprehensive Docker documentation (DOCKER.md)
  - Health check support

- **Logging System**:
  - Structured logging with configurable levels
  - Console and file logging support
  - Request/response logging

- **Examples**:
  - Advanced bot example (`advanced_bot.py`)
  - Demonstrates all new features
  - Inline keyboards, media, polls, etc.

- **Documentation**:
  - Configuration examples (YAML and JSON)
  - Docker deployment guide
  - Extended README with new features
  - Changelog (this file)

### Changed
- Improved API endpoint handling for better compatibility
- Enhanced error handling and logging
- Updated README with comprehensive feature list
- Expanded test suite (14 tests total)

### Fixed
- Form data handling for python-telegram-bot compatibility
- Request parsing for various content types

## [0.1.0] - 2025-11-08

### Added
- Initial release of SuperMock
- Core mock Telegram Bot API server
- Flask-based HTTP server
- Long polling support (`getUpdates`)
- Webhook support
- Terminal-based interactive chat UI
- CLI interface (`supermock server` and `supermock chat`)
- Core API methods:
  - `getMe`, `getUpdates`, `setWebhook`, `deleteWebhook`, `getWebhookInfo`
  - `sendMessage`, `sendPhoto`, `sendDocument`
  - `editMessageText`, `answerCallbackQuery`
- Unit tests (8 tests)
- Examples (echo bot, inline keyboard bot, test examples)
- Documentation (README.md, README.ru.md, QUICK_START.md)
- Apache 2.0 license
- NOTICE file for license compliance

[0.2.0]: https://github.com/infernasel/SuperMock-1/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/infernasel/SuperMock-1/releases/tag/v0.1.0
