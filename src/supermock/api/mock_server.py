"""
Mock Telegram Bot API Server

This module implements a mock server that mimics the Telegram Bot API.
It allows developers to test their bots locally without connecting to the real Telegram API.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import threading
import queue
from typing import Dict, List, Any, Optional


class TelegramMockServer:
    """Mock implementation of Telegram Bot API Server"""
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.message_id_counter = 1
        self.update_id_counter = 1
        self.chat_id = 12345  # Default chat ID for testing
        self.updates_queue: queue.Queue = queue.Queue()
        self.messages_history: List[Dict[str, Any]] = []
        self.bot_token: Optional[str] = None
        self.id_lock = threading.Lock()
        
        self._setup_routes()
    
    def _get_request_data(self) -> Dict[str, Any]:
        """Extract request data from various formats"""
        if request.is_json:
            return request.get_json() or {}
        elif request.form:
            # Convert form data to dict, handling nested JSON strings
            data = {}
            for key, value in request.form.items():
                try:
                    # Try to parse JSON values
                    data[key] = json.loads(value)
                except:
                    data[key] = value
            return data
        elif request.data:
            try:
                return json.loads(request.data)
            except:
                return {}
        return {}
    
    def _setup_routes(self):
        """Setup Flask routes for Telegram Bot API endpoints"""
        
        @self.app.route('/bot<token>/getMe', methods=['GET', 'POST'])
        def get_me(token):
            self.bot_token = token
            return jsonify({
                "ok": True,
                "result": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot",
                    "can_join_groups": True,
                    "can_read_all_group_messages": False,
                    "supports_inline_queries": False
                }
            })
        
        @self.app.route('/bot<token>/getUpdates', methods=['GET', 'POST'])
        def get_updates(token):
            data = self._get_request_data()
            try:
                offset = int(data.get('offset', 0))
                limit = int(data.get('limit', 100))
                timeout = int(data.get('timeout', 0))
            except (ValueError, TypeError):
                offset, limit, timeout = 0, 100, 0
            
            updates = []
            try:
                # Try to get updates from queue with timeout
                if timeout > 0:
                    update = self.updates_queue.get(timeout=min(timeout, 30))
                    if update['update_id'] >= offset:
                        updates.append(update)
                else:
                    # Get all available updates
                    while not self.updates_queue.empty() and len(updates) < limit:
                        update = self.updates_queue.get_nowait()
                        if update['update_id'] >= offset:
                            updates.append(update)
            except queue.Empty:
                pass
            
            return jsonify({
                "ok": True,
                "result": updates
            })
        
        @self.app.route('/bot<token>/sendMessage', methods=['POST'])
        def send_message(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            text = data.get('text', '')
            reply_markup = data.get('reply_markup')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": text
            }
            
            if reply_markup:
                message['reply_markup'] = reply_markup
            
            self.messages_history.append({
                "type": "bot",
                "message": message
            })
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/setWebhook', methods=['POST'])
        def set_webhook(token):
            data = self._get_request_data()
            url = data.get('url', '')
            
            return jsonify({
                "ok": True,
                "result": True,
                "description": f"Webhook was set to {url}" if url else "Webhook was deleted"
            })
        
        @self.app.route('/bot<token>/deleteWebhook', methods=['POST'])
        def delete_webhook(token):
            return jsonify({
                "ok": True,
                "result": True,
                "description": "Webhook was deleted"
            })
        
        @self.app.route('/bot<token>/getWebhookInfo', methods=['GET', 'POST'])
        def get_webhook_info(token):
            return jsonify({
                "ok": True,
                "result": {
                    "url": "",
                    "has_custom_certificate": False,
                    "pending_update_count": 0
                }
            })
        
        @self.app.route('/bot<token>/sendPhoto', methods=['POST'])
        def send_photo(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            caption = data.get('caption', '')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "photo": [{"file_id": "mock_photo_id", "width": 100, "height": 100}],
                "caption": caption
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendDocument', methods=['POST'])
        def send_document(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            caption = data.get('caption', '')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "document": {"file_id": "mock_doc_id", "file_name": "document.txt"},
                "caption": caption
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/editMessageText', methods=['POST'])
        def edit_message_text(token):
            data = self._get_request_data()
            
            message = {
                "message_id": data.get('message_id', 1),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": data.get('chat_id'),
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": data.get('text', ''),
                "edit_date": int(datetime.now().timestamp())
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/answerCallbackQuery', methods=['POST'])
        def answer_callback_query(token):
            return jsonify({
                "ok": True,
                "result": True
            })
        
        @self.app.route('/bot<token>/sendVideo', methods=['POST'])
        def send_video(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            caption = data.get('caption', '')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "video": {
                    "file_id": "mock_video_id",
                    "width": 1920,
                    "height": 1080,
                    "duration": 10
                },
                "caption": caption
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendAudio', methods=['POST'])
        def send_audio(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            caption = data.get('caption', '')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "audio": {
                    "file_id": "mock_audio_id",
                    "duration": 180,
                    "title": "Mock Audio"
                },
                "caption": caption
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendVoice', methods=['POST'])
        def send_voice(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "voice": {
                    "file_id": "mock_voice_id",
                    "duration": 5
                }
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendSticker', methods=['POST'])
        def send_sticker(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "sticker": {
                    "file_id": "mock_sticker_id",
                    "width": 512,
                    "height": 512,
                    "emoji": "😀"
                }
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendLocation', methods=['POST'])
        def send_location(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            latitude = data.get('latitude', 0.0)
            longitude = data.get('longitude', 0.0)
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendPoll', methods=['POST'])
        def send_poll(token):
            data = self._get_request_data()
            chat_id = data.get('chat_id')
            question = data.get('question', 'Poll question?')
            options = data.get('options', ['Option 1', 'Option 2'])
            
            message = {
                "message_id": self._next_message_id(),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "poll": {
                    "id": f"poll_{self.message_id_counter}",
                    "question": question,
                    "options": [{"text": opt, "voter_count": 0} for opt in options],
                    "is_closed": False,
                    "is_anonymous": True,
                    "type": "regular",
                    "allows_multiple_answers": False
                }
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/deleteMessage', methods=['POST'])
        def delete_message(token):
            return jsonify({
                "ok": True,
                "result": True
            })
        
        @self.app.route('/bot<token>/editMessageReplyMarkup', methods=['POST'])
        def edit_message_reply_markup(token):
            data = self._get_request_data()
            
            message = {
                "message_id": data.get('message_id', 1),
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": data.get('chat_id'),
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": "Message with updated markup",
                "edit_date": int(datetime.now().timestamp())
            }
            
            return jsonify({
                "ok": True,
                "result": message
            })
        
        @self.app.route('/bot<token>/sendChatAction', methods=['POST'])
        def send_chat_action(token):
            return jsonify({
                "ok": True,
                "result": True
            })
        
        @self.app.route('/bot<token>/getChatMember', methods=['POST', 'GET'])
        def get_chat_member(token):
            data = self._get_request_data()
            user_id = data.get('user_id', self.chat_id)
            
            return jsonify({
                "ok": True,
                "result": {
                    "user": {
                        "id": user_id,
                        "is_bot": False,
                        "first_name": "TestUser",
                        "username": "test_user"
                    },
                    "status": "member"
                }
            })
        
        @self.app.route('/bot<token>/getChat', methods=['POST', 'GET'])
        def get_chat(token):
            return jsonify({
                "ok": True,
                "result": {
                    "id": self.chat_id,
                    "type": "private",
                    "first_name": "TestUser",
                    "username": "test_user"
                }
            })
        
        @self.app.route('/bot<token>/answerInlineQuery', methods=['POST'])
        def answer_inline_query(token):
            data = self._get_request_data()
            inline_query_id = data.get('inline_query_id')
            results = data.get('results', [])
            
            # Store results for testing purposes
            if hasattr(self, 'inline_results_cache'):
                self.inline_results_cache[inline_query_id] = results
            
            return jsonify({
                "ok": True,
                "result": True
            })
        
        @self.app.route('/bot<token>/editMessageTextInline', methods=['POST'])
        def edit_message_text_inline(token):
            data = self._get_request_data()
            
            return jsonify({
                "ok": True,
                "result": True
            })
        
        @self.app.route('/bot<token>/editMessageReplyMarkupInline', methods=['POST'])
        def edit_message_reply_markup_inline(token):
            return jsonify({
                "ok": True,
                "result": True
            })
    
    def _next_message_id(self) -> int:
        """Generate next message ID"""
        with self.id_lock:
            msg_id = self.message_id_counter
            self.message_id_counter += 1
            return msg_id

    def _next_update_id(self) -> int:
        """Generate next update ID"""
        with self.id_lock:
            update_id = self.update_id_counter
            self.update_id_counter += 1
            return update_id
    
    def send_user_message(self, text: str, from_user: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Simulate a user sending a message to the bot
        
        Args:
            text: Message text
            from_user: User information (optional)
            
        Returns:
            The created update object
        """
        if from_user is None:
            from_user = {
                "id": self.chat_id,
                "is_bot": False,
                "first_name": "TestUser",
                "username": "test_user"
            }
        
        message = {
            "message_id": self._next_message_id(),
            "from": from_user,
            "chat": {
                "id": self.chat_id,
                "type": "private",
                "first_name": from_user.get("first_name", "TestUser"),
                "username": from_user.get("username", "test_user")
            },
            "date": int(datetime.now().timestamp()),
            "text": text
        }
        
        update = {
            "update_id": self._next_update_id(),
            "message": message
        }
        
        self.updates_queue.put(update)
        self.messages_history.append({
            "type": "user",
            "message": message
        })
        
        return update
    
    def send_callback_query(self, data: str, message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Simulate a user clicking an inline button
        
        Args:
            data: Callback data
            message_id: Message ID (optional)
            
        Returns:
            The created update object
        """
        callback_query = {
            "id": str(self._next_update_id()),
            "from": {
                "id": self.chat_id,
                "is_bot": False,
                "first_name": "TestUser",
                "username": "test_user"
            },
            "message": {
                "message_id": message_id or self.message_id_counter - 1,
                "from": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "MockBot",
                    "username": "mock_bot"
                },
                "chat": {
                    "id": self.chat_id,
                    "type": "private"
                },
                "date": int(datetime.now().timestamp()),
                "text": "Button message"
            },
            "chat_instance": "123456789",
            "data": data
        }
        
        update = {
            "update_id": self._next_update_id(),
            "callback_query": callback_query
        }
        
        self.updates_queue.put(update)
        
        return update
    
    def get_messages_history(self) -> List[Dict[str, Any]]:
        """Get all messages history"""
        return self.messages_history
    
    def clear_messages(self):
        """Clear messages history"""
        self.messages_history.clear()
    
    def run(self, debug: bool = False):
        """Start the mock server"""
        print(f"SuperMock Telegram Bot API Server started at http://{self.host}:{self.port}")
        print(f"Use this as your bot API base URL: http://{self.host}:{self.port}/bot<YOUR_TOKEN>")
        print(f"Example: http://{self.host}:{self.port}/bot123456:ABC-DEF/getMe")
        self.app.run(host=self.host, port=self.port, debug=debug, use_reloader=False)