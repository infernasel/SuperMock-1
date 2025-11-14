"""
History persistence for SuperMock
"""

import json
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime


class HistoryManager:
    """Manager for saving and loading conversation history"""
    
    def __init__(self, history_file: str = ".supermock_history.json"):
        self.history_file = Path(history_file)
    
    def save_history(self, messages: List[Dict[str, Any]]):
        """Save messages history to file"""
        history_data = {
            "saved_at": datetime.now().isoformat(),
            "messages": messages
        }
        
        with open(self.history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load messages history from file"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                history_data = json.load(f)
                return history_data.get('messages', [])
        except Exception:
            return []
    
    def clear_history(self):
        """Clear history file"""
        if self.history_file.exists():
            self.history_file.unlink()
    
    def export_history(self, export_file: str, format: str = 'json'):
        """Export history to different formats"""
        messages = self.load_history()
        
        export_path = Path(export_file)
        
        if format == 'json':
            with open(export_path, 'w') as f:
                json.dump(messages, f, indent=2)
        elif format == 'txt':
            with open(export_path, 'w') as f:
                for msg_data in messages:
                    msg_type = msg_data['type']
                    msg = msg_data['message']
                    text = msg.get('text', '[Non-text message]')
                    timestamp = datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S')
                    
                    sender = "Bot" if msg_type == "bot" else "User"
                    f.write(f"[{timestamp}] {sender}: {text}\n")
        else:
            raise ValueError(f"Unsupported export format: {format}")
