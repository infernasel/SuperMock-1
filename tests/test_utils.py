"""
Unit tests for utility modules
"""

import pytest
import json
import tempfile
from pathlib import Path
from supermock.utils import Config, HistoryManager


def test_config_default():
    """Test default configuration"""
    config = Config()
    
    assert config.get('server.host') == 'localhost'
    assert config.get('server.port') == 8081
    assert config.get('bot.first_name') == 'MockBot'


def test_config_set_get():
    """Test setting and getting configuration values"""
    config = Config()
    
    config.set('server.host', '0.0.0.0')
    assert config.get('server.host') == '0.0.0.0'
    
    config.set('custom.key', 'value')
    assert config.get('custom.key') == 'value'


def test_config_load_from_json():
    """Test loading configuration from JSON file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'server': {'host': '127.0.0.1', 'port': 9000},
            'bot': {'first_name': 'TestBot'}
        }, f)
        config_file = f.name
    
    try:
        config = Config(config_file)
        assert config.get('server.host') == '127.0.0.1'
        assert config.get('server.port') == 9000
        assert config.get('bot.first_name') == 'TestBot'
        # Default values should still be present
        assert config.get('bot.username') == 'mock_bot'
    finally:
        Path(config_file).unlink()


def test_history_manager_save_load():
    """Test saving and loading history"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        history_file = f.name
    
    try:
        manager = HistoryManager(history_file)
        
        # Initially no history
        assert manager.load_history() == []
        
        # Save some messages
        messages = [
            {'type': 'user', 'message': {'text': 'Hello'}},
            {'type': 'bot', 'message': {'text': 'Hi!'}}
        ]
        manager.save_history(messages)
        
        # Load and verify
        loaded = manager.load_history()
        assert len(loaded) == 2
        assert loaded[0]['type'] == 'user'
        assert loaded[1]['type'] == 'bot'
    finally:
        Path(history_file).unlink(missing_ok=True)


def test_history_manager_clear():
    """Test clearing history"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        history_file = f.name
    
    try:
        manager = HistoryManager(history_file)
        
        # Save and clear
        messages = [{'type': 'user', 'message': {'text': 'Test'}}]
        manager.save_history(messages)
        assert len(manager.load_history()) == 1
        
        manager.clear_history()
        assert not Path(history_file).exists()
    finally:
        Path(history_file).unlink(missing_ok=True)


def test_history_manager_export_txt():
    """Test exporting history to text format"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        history_file = f.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        export_file = f.name
    
    try:
        manager = HistoryManager(history_file)
        
        # Save messages
        from datetime import datetime
        now = int(datetime.now().timestamp())
        messages = [
            {'type': 'user', 'message': {'text': 'Hello', 'date': now}},
            {'type': 'bot', 'message': {'text': 'Hi there!', 'date': now}}
        ]
        manager.save_history(messages)
        
        # Export to txt
        manager.export_history(export_file, format='txt')
        
        # Verify export
        with open(export_file, 'r') as f:
            content = f.read()
            assert 'User: Hello' in content
            assert 'Bot: Hi there!' in content
    finally:
        Path(history_file).unlink(missing_ok=True)
        Path(export_file).unlink(missing_ok=True)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
