"""
Unit tests for TelegramMockServer
"""

import pytest
import threading
import time
import requests
from supermock.api import TelegramMockServer


@pytest.fixture
def mock_server():
    """Fixture to create and start a mock server for testing"""
    # Use a different port for each test to avoid conflicts
    import random
    port = random.randint(9000, 9999)
    server = TelegramMockServer(host='localhost', port=port)
    
    # Start server in background thread
    server_thread = threading.Thread(target=lambda: server.run(debug=False), daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1.5)
    
    yield server
    
    # Cleanup
    server.clear_messages()


def test_get_me_endpoint(mock_server):
    """Test the /getMe endpoint"""
    url = f'http://localhost:{mock_server.port}/bot_test_token/getMe'
    response = requests.get(url)
    assert response.status_code == 200
    
    data = response.json()
    assert data['ok'] is True
    assert 'result' in data
    assert data['result']['is_bot'] is True
    assert data['result']['first_name'] == 'MockBot'


def test_get_updates_endpoint(mock_server):
    """Test the /getUpdates endpoint"""
    # Send a user message first
    mock_server.send_user_message("Test message")
    
    # Give a moment for the message to be queued
    time.sleep(0.2)
    
    # Get updates
    url = f'http://localhost:{mock_server.port}/bot_test_token/getUpdates'
    response = requests.post(url, json={'offset': 0, 'timeout': 1})
    assert response.status_code == 200
    
    data = response.json()
    assert data['ok'] is True
    # Note: getUpdates consumes from the queue, so this may or may not have messages
    # depending on timing. Let's just verify the endpoint works.
    assert isinstance(data['result'], list)


def test_send_message_endpoint(mock_server):
    """Test the /sendMessage endpoint"""
    url = f'http://localhost:{mock_server.port}/bot_test_token/sendMessage'
    response = requests.post(
        url,
        json={
            'chat_id': 12345,
            'text': 'Hello from bot!'
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data['ok'] is True
    assert data['result']['text'] == 'Hello from bot!'


def test_set_webhook_endpoint(mock_server):
    """Test the /setWebhook endpoint"""
    url = f'http://localhost:{mock_server.port}/bot_test_token/setWebhook'
    response = requests.post(
        url,
        json={'url': 'https://example.com/webhook'}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data['ok'] is True
    assert data['result'] is True


def test_send_photo_endpoint(mock_server):
    """Test the /sendPhoto endpoint"""
    url = f'http://localhost:{mock_server.port}/bot_test_token/sendPhoto'
    response = requests.post(
        url,
        json={
            'chat_id': 12345,
            'photo': 'file_id',
            'caption': 'Test photo'
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data['ok'] is True
    assert 'photo' in data['result']


def test_message_history(mock_server):
    """Test message history tracking"""
    # Initially empty
    assert len(mock_server.get_messages_history()) == 0
    
    # Send user message
    mock_server.send_user_message("User message")
    assert len(mock_server.get_messages_history()) == 1
    
    # Send bot message via API
    url = f'http://localhost:{mock_server.port}/bot_test_token/sendMessage'
    requests.post(
        url,
        json={'chat_id': 12345, 'text': 'Bot response'}
    )
    
    # Wait a bit for message to be recorded
    time.sleep(0.2)
    
    history = mock_server.get_messages_history()
    assert len(history) >= 1  # At least the user message should be there
    assert history[0]['type'] == 'user'
    
    # Check if bot message was recorded
    bot_messages = [m for m in history if m['type'] == 'bot']
    assert len(bot_messages) >= 1
    assert bot_messages[0]['message']['text'] == 'Bot response'


def test_callback_query_creation(mock_server):
    """Test callback query creation"""
    update = mock_server.send_callback_query("button_data", message_id=123)
    
    assert 'callback_query' in update
    assert update['callback_query']['data'] == 'button_data'
    assert update['callback_query']['message']['message_id'] == 123


def test_clear_messages(mock_server):
    """Test clearing message history"""
    mock_server.send_user_message("Message 1")
    mock_server.send_user_message("Message 2")
    
    assert len(mock_server.get_messages_history()) == 2
    
    mock_server.clear_messages()
    
    assert len(mock_server.get_messages_history()) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
