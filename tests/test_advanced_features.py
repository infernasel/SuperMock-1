"""
Unit tests for group chat and inline mode simulators
"""

import pytest
from supermock.api import TelegramMockServer
from supermock.utils import GroupChatSimulator, InlineModeSimulator
import threading
import time


@pytest.fixture
def mock_server():
    """Create a mock server for testing"""
    import random
    port = random.randint(9500, 9999)
    server = TelegramMockServer(host='localhost', port=port)
    
    # Start server in background
    server_thread = threading.Thread(target=lambda: server.run(debug=False), daemon=True)
    server_thread.start()
    time.sleep(1.5)
    
    yield server
    
    server.clear_messages()


def test_group_chat_creation(mock_server):
    """Test creating a group chat"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group", member_count=5)
    
    assert group_id < 0  # Group IDs are negative
    assert group_sim.get_group_info(group_id) is not None
    assert group_sim.get_group_info(group_id)['title'] == "Test Group"
    assert len(group_sim.get_group_members(group_id)) == 5


def test_group_message_sending(mock_server):
    """Test sending messages in group chat"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group")
    update = group_sim.send_group_message(group_id, "Hello group!")
    
    assert update is not None
    assert 'message' in update
    assert update['message']['text'] == "Hello group!"
    assert update['message']['chat']['type'] == "group"


def test_group_command(mock_server):
    """Test sending commands in group"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group")
    update = group_sim.send_group_command(group_id, "/start", mention_bot=True)
    
    assert update is not None
    assert '@mock_bot' in update['message']['text']


def test_add_remove_member(mock_server):
    """Test adding and removing group members"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group", member_count=2)
    
    initial_count = len(group_sim.get_group_members(group_id))
    assert initial_count == 2
    
    # Add a member
    new_user = {"id": 99999, "first_name": "NewUser", "username": "newuser"}
    group_sim.add_member(group_id, new_user)
    assert len(group_sim.get_group_members(group_id)) == 3
    
    # Remove a member
    group_sim.remove_member(group_id, 99999)
    assert len(group_sim.get_group_members(group_id)) == 2


def test_user_joined_event(mock_server):
    """Test user joined event"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group")
    new_user = {"id": 88888, "first_name": "Joiner", "username": "joiner"}
    
    update = group_sim.simulate_user_joined(group_id, new_user)
    
    assert update is not None
    assert 'new_chat_members' in update['message']
    assert update['message']['new_chat_members'][0]['id'] == 88888


def test_user_left_event(mock_server):
    """Test user left event"""
    group_sim = GroupChatSimulator(mock_server)
    
    group_id = group_sim.create_group("Test Group")
    members = group_sim.get_group_members(group_id)
    leaving_user = members[0]
    
    update = group_sim.simulate_user_left(group_id, leaving_user)
    
    assert update is not None
    assert 'left_chat_member' in update['message']
    assert update['message']['left_chat_member']['id'] == leaving_user['id']


def test_inline_query(mock_server):
    """Test inline query creation"""
    inline_sim = InlineModeSimulator(mock_server)
    
    update = inline_sim.send_inline_query("test query")
    
    assert update is not None
    assert 'inline_query' in update
    assert update['inline_query']['query'] == "test query"


def test_chosen_inline_result(mock_server):
    """Test chosen inline result"""
    inline_sim = InlineModeSimulator(mock_server)
    
    update = inline_sim.send_chosen_inline_result("result_123", "original query")
    
    assert update is not None
    assert 'chosen_inline_result' in update
    assert update['chosen_inline_result']['result_id'] == "result_123"
    assert update['chosen_inline_result']['query'] == "original query"


def test_inline_results_cache(mock_server):
    """Test caching inline results"""
    inline_sim = InlineModeSimulator(mock_server)
    
    query_id = "query_456"
    results = [
        {"id": "1", "title": "Result 1"},
        {"id": "2", "title": "Result 2"}
    ]
    
    inline_sim.cache_inline_results(query_id, results)
    cached = inline_sim.get_cached_results(query_id)
    
    assert cached is not None
    assert len(cached) == 2
    assert cached[0]['title'] == "Result 1"
    
    inline_sim.clear_cache()
    assert inline_sim.get_cached_results(query_id) is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
