"""
Terminal-based Chat UI for SuperMock

Provides an interactive terminal interface that mimics Telegram chat
for testing bots locally.
"""

import sys
import threading
import time
from typing import Optional
from datetime import datetime


class TerminalChat:
    """Terminal-based chat interface for interacting with mock Telegram bot"""
    
    def __init__(self, mock_server):
        self.mock_server = mock_server
        self.running = False
        self.last_message_count = 0
        
    def _display_message(self, msg_type: str, sender: str, text: str, timestamp: Optional[str] = None):
        """Display a message in the terminal"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == "user":
            # User messages aligned to the right
            print(f"\n{'':>60}{sender} [{timestamp}]")
            print(f"{'':>50}┌{'─' * 28}┐")
            # Word wrap for long messages
            words = text.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= 26:
                    line += word + " "
                else:
                    print(f"{'':>50}│ {line:<26} │")
                    line = word + " "
            if line:
                print(f"{'':>50}│ {line:<26} │")
            print(f"{'':>50}└{'─' * 28}┘")
        else:
            # Bot messages aligned to the left
            print(f"\n[{timestamp}] {sender}")
            print(f"┌{'─' * 48}┐")
            # Word wrap for long messages
            words = text.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= 46:
                    line += word + " "
                else:
                    print(f"│ {line:<46} │")
                    line = word + " "
            if line:
                print(f"│ {line:<46} │")
            print(f"└{'─' * 48}┘")
    
    def _monitor_bot_messages(self):
        """Monitor and display bot responses"""
        while self.running:
            messages = self.mock_server.get_messages_history()
            if len(messages) > self.last_message_count:
                new_messages = messages[self.last_message_count:]
                for msg_data in new_messages:
                    if msg_data["type"] == "bot":
                        msg = msg_data["message"]
                        text = msg.get("text", "")
                        if msg.get("photo"):
                            text = f"📷 [Photo] {msg.get('caption', '')}"
                        elif msg.get("document"):
                            text = f"📄 [Document] {msg.get('caption', '')}"
                        
                        timestamp = datetime.fromtimestamp(msg["date"]).strftime("%H:%M")
                        self._display_message("bot", "🤖 MockBot", text, timestamp)
                
                self.last_message_count = len(messages)
            
            time.sleep(0.5)
    
    def _display_header(self):
        """Display chat header"""
        print("\n" + "=" * 80)
        print("  SuperMock - Telegram Bot Testing Terminal".center(80))
        print("=" * 80)
        print("\n🤖 MockBot")
        print("─" * 80)
        print("\nType your messages below. Commands:")
        print("  /start - Send /start command")
        print("  /help - Send /help command")
        print("  /quit or /exit - Exit the chat")
        print("─" * 80)
    
    def start_interactive(self):
        """Start interactive terminal chat session"""
        self._display_header()
        self.running = True
        
        # Start monitoring thread for bot messages
        monitor_thread = threading.Thread(target=self._monitor_bot_messages, daemon=True)
        monitor_thread.start()
        
        try:
            while self.running:
                try:
                    user_input = input("\n💬 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['/quit', '/exit']:
                        print("\n👋 Exiting chat...")
                        self.running = False
                        break
                    
                    # Display user message
                    self._display_message("user", "You 💬", user_input)
                    
                    # Send to mock server
                    self.mock_server.send_user_message(user_input)
                    
                    # Wait a bit for bot response
                    time.sleep(0.5)
                    
                except KeyboardInterrupt:
                    print("\n\n👋 Chat interrupted. Exiting...")
                    self.running = False
                    break
                except EOFError:
                    print("\n\n👋 End of input. Exiting...")
                    self.running = False
                    break
        
        finally:
            self.running = False
            print("\n" + "=" * 80)
            print("  Thank you for using SuperMock!".center(80))
            print("=" * 80 + "\n")
    
    def stop(self):
        """Stop the terminal chat"""
        self.running = False
