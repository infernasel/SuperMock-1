"""
Inline Mode Support for SuperMock

Allows testing bots with inline queries (when users type @botname in any chat).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class InlineModeSimulator:
    """Simulate inline mode queries for testing inline bots"""
    
    def __init__(self, mock_server):
        self.mock_server = mock_server
        self.inline_results_cache: Dict[str, List[Dict[str, Any]]] = {}
    
    def send_inline_query(self, query: str, from_user: Optional[Dict] = None, offset: str = "") -> Dict[str, Any]:
        """
        Send an inline query to the bot
        
        Args:
            query: The query text (what user typed after @botname)
            from_user: User information (optional)
            offset: Pagination offset (optional)
            
        Returns:
            The created update object
        """
        if from_user is None:
            from_user = {
                "id": self.mock_server.chat_id,
                "is_bot": False,
                "first_name": "TestUser",
                "username": "test_user"
            }
        
        inline_query = {
            "id": str(uuid.uuid4()),
            "from": from_user,
            "query": query,
            "offset": offset,
            "chat_type": "sender"
        }
        
        update = {
            "update_id": self.mock_server._next_update_id(),
            "inline_query": inline_query
        }
        
        self.mock_server.updates_queue.put(update)
        
        return update
    
    def send_chosen_inline_result(self, result_id: str, query: str, from_user: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Simulate user choosing an inline result
        
        Args:
            result_id: ID of the chosen result
            query: The original query
            from_user: User information (optional)
            
        Returns:
            The created update object
        """
        if from_user is None:
            from_user = {
                "id": self.mock_server.chat_id,
                "is_bot": False,
                "first_name": "TestUser",
                "username": "test_user"
            }
        
        chosen_result = {
            "result_id": result_id,
            "from": from_user,
            "query": query,
            "inline_message_id": f"inline_{uuid.uuid4()}"
        }
        
        update = {
            "update_id": self.mock_server._next_update_id(),
            "chosen_inline_result": chosen_result
        }
        
        self.mock_server.updates_queue.put(update)
        
        return update
    
    def cache_inline_results(self, query_id: str, results: List[Dict[str, Any]]):
        """
        Cache inline results (simulates what the bot sends back)
        
        Args:
            query_id: The inline query ID
            results: List of inline results
        """
        self.inline_results_cache[query_id] = results
    
    def get_cached_results(self, query_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached inline results for a query"""
        return self.inline_results_cache.get(query_id)
    
    def clear_cache(self):
        """Clear all cached inline results"""
        self.inline_results_cache.clear()
