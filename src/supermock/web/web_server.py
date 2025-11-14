"""
Web UI Server for SuperMock

Provides a web-based interface for testing Telegram bots.
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetime
from typing import Optional, Dict, Any
import threading
import time


class WebUIServer:
    """Web-based UI server for SuperMock"""
    
    def __init__(self, mock_server, host: str = "localhost", port: int = 8082):
        self.mock_server = mock_server
        self.host = host
        self.port = port
        self.app = Flask(__name__, 
                        static_folder='static',
                        template_folder='templates')
        self.app.config['SECRET_KEY'] = 'supermock-secret-key'
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        self._setup_routes()
        self._setup_socketio()
        self._start_message_monitor()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main page"""
            return render_template('index.html')
        
        @self.app.route('/api/messages', methods=['GET'])
        def get_messages():
            """Get message history"""
            return jsonify({
                'success': True,
                'messages': self.mock_server.get_messages_history()
            })
        
        @self.app.route('/api/send', methods=['POST'])
        def send_message():
            """Send a user message"""
            data = request.get_json()
            text = data.get('text', '')
            
            if not text:
                return jsonify({'success': False, 'error': 'No text provided'}), 400
            
            update = self.mock_server.send_user_message(text)
            
            return jsonify({
                'success': True,
                'update': update
            })
        
        @self.app.route('/api/callback', methods=['POST'])
        def send_callback():
            """Send a callback query (button click)"""
            data = request.get_json()
            callback_data = data.get('data', '')
            message_id = data.get('message_id')
            
            if not callback_data:
                return jsonify({'success': False, 'error': 'No callback data'}), 400
            
            update = self.mock_server.send_callback_query(callback_data, message_id)
            
            return jsonify({
                'success': True,
                'update': update
            })
        
        @self.app.route('/api/clear', methods=['POST'])
        def clear_messages():
            """Clear message history"""
            self.mock_server.clear_messages()
            return jsonify({'success': True})
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get server statistics"""
            messages = self.mock_server.get_messages_history()
            user_messages = [m for m in messages if m['type'] == 'user']
            bot_messages = [m for m in messages if m['type'] == 'bot']
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_messages': len(messages),
                    'user_messages': len(user_messages),
                    'bot_messages': len(bot_messages),
                    'server_uptime': 'N/A',  # TODO: implement
                    'api_base_url': f"http://{self.mock_server.host}:{self.mock_server.port}"
                }
            })
    
    def _setup_socketio(self):
        """Setup WebSocket handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            print(f"🌐 Web client connected")
            emit('connected', {'status': 'ok'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            print(f"🌐 Web client disconnected")
        
        @self.socketio.on('send_message')
        def handle_send_message(data):
            """Handle sending message from web UI"""
            text = data.get('text', '')
            if text:
                update = self.mock_server.send_user_message(text)
                emit('message_sent', {'update': update})
    
    def _start_message_monitor(self):
        """Start monitoring for new messages and broadcast via WebSocket"""
        self.last_message_count = 0
        
        def monitor():
            while True:
                try:
                    # Block until a new message is available
                    msg_data = self.mock_server.web_ui_queue.get()
                    self.socketio.emit('new_message', msg_data)
                except Exception as e:
                    print(f"Error in monitor thread: {e}")
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def run(self, debug: bool = False):
        """Start the web UI server"""
        print(f"🌐 SuperMock Web UI started at http://{self.host}:{self.port}")
        print(f"📱 Open in browser: http://{self.host}:{self.port}")
        self.socketio.run(self.app, host=self.host, port=self.port, debug=debug, allow_unsafe_werkzeug=True)
