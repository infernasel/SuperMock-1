"""
Simple Test Suite for Bot Testing with SuperMock

This example demonstrates how to write automated tests for Telegram bots using SuperMock.
"""

import pytest
import threading
import time
from supermock.api import TelegramMockServer


@pytest.fixture
def mock_server():
    """Setup and teardown mock server for testing"""
    server = TelegramMockServer(host='localhost', port=8082)
    
    # Start server in background thread
    server_thread = threading.Thread(target=lambda: server.run(debug=False), daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    yield server
    
    # Cleanup
    server.clear_messages()


def test_server_starts_successfully(mock_server):
    """Test that the mock server starts and responds"""
    assert mock_server is not None
    assert mock_server.port == 8082


def test_send_user_message(mock_server):
    """Test sending a user message to the bot"""
    # Send a message from user
    update = mock_server.send_user_message("Hello, bot!")
    
    # Verify the update was created
    assert update is not None
    assert "message" in update
    assert update["message"]["text"] == "Hello, bot!"


def test_bot_response_recorded(mock_server):
    """Test that bot responses are recorded in history"""
    # Initially no messages
    assert len(mock_server.get_messages_history()) == 0
    
    # Send a user message
    mock_server.send_user_message("Test message")
    
    # Check history
    history = mock_server.get_messages_history()
    assert len(history) == 1
    assert history[0]["type"] == "user"
    assert history[0]["message"]["text"] == "Test message"


def test_multiple_messages(mock_server):
    """Test sending multiple messages"""
    messages = ["Message 1", "Message 2", "Message 3"]
    
    for msg in messages:
        mock_server.send_user_message(msg)
    
    history = mock_server.get_messages_history()
    assert len(history) == 3
    
    for i, msg in enumerate(messages):
        assert history[i]["message"]["text"] == msg


def test_callback_query(mock_server):
    """Test sending callback query (button click)"""
    update = mock_server.send_callback_query("button_data")
    
    assert update is not None
    assert "callback_query" in update
    assert update["callback_query"]["data"] == "button_data"


def test_clear_messages(mock_server):
    """Test clearing message history"""
    # Add some messages
    mock_server.send_user_message("Message 1")
    mock_server.send_user_message("Message 2")
    
    assert len(mock_server.get_messages_history()) == 2
    
    # Clear messages
    mock_server.clear_messages()
    
    assert len(mock_server.get_messages_history()) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
