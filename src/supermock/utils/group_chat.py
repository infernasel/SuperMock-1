"""
Group Chat Simulation for SuperMock

Allows testing bots in group chat scenarios with multiple users.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random


class GroupChatSimulator:
    """Simulate group chat behavior for testing bots in group scenarios"""
    
    def __init__(self, mock_server):
        self.mock_server = mock_server
        self.groups: Dict[int, Dict[str, Any]] = {}
        self.group_id_counter = -1000000000  # Negative IDs for groups
        self.members: Dict[int, List[Dict[str, Any]]] = {}  # group_id -> members
    
    def create_group(self, title: str, member_count: int = 3) -> int:
        """
        Create a new group chat
        
        Args:
            title: Group title
            member_count: Number of members to create (default: 3)
            
        Returns:
            Group chat ID
        """
        group_id = self.group_id_counter
        self.group_id_counter -= 1
        
        self.groups[group_id] = {
            "id": group_id,
            "type": "group",
            "title": title,
            "all_members_are_administrators": False
        }
        
        # Create members
        members = []
        for i in range(member_count):
            member = {
                "id": 10000 + i,
                "is_bot": False,
                "first_name": f"User{i+1}",
                "username": f"user{i+1}"
            }
            members.append(member)
        
        self.members[group_id] = members
        
        return group_id
    
    def send_group_message(self, group_id: int, text: str, from_user: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send a message in a group chat
        
        Args:
            group_id: Group chat ID
            text: Message text
            from_user: User sending the message (optional, random if not provided)
            
        Returns:
            The created update object
        """
        if group_id not in self.groups:
            raise ValueError(f"Group {group_id} does not exist")
        
        # Select a random member if user not specified
        if from_user is None:
            from_user = random.choice(self.members[group_id])
        
        message = {
            "message_id": self.mock_server._next_message_id(),
            "from": from_user,
            "chat": self.groups[group_id],
            "date": int(datetime.now().timestamp()),
            "text": text
        }
        
        update = {
            "update_id": self.mock_server._next_update_id(),
            "message": message
        }
        
        self.mock_server.updates_queue.put(update)
        self.mock_server.messages_history.append({
            "type": "user",
            "message": message
        })
        
        return update
    
    def send_group_command(self, group_id: int, command: str, mention_bot: bool = True) -> Dict[str, Any]:
        """
        Send a command in a group chat
        
        Args:
            group_id: Group chat ID
            command: Command to send (e.g., "/start")
            mention_bot: Whether to mention the bot in the command
            
        Returns:
            The created update object
        """
        if mention_bot:
            command = f"{command}@mock_bot"
        
        return self.send_group_message(group_id, command)
    
    def add_member(self, group_id: int, user: Dict[str, Any]) -> bool:
        """
        Add a member to a group
        
        Args:
            group_id: Group chat ID
            user: User information dict
            
        Returns:
            True if successful
        """
        if group_id not in self.groups:
            return False
        
        if group_id not in self.members:
            self.members[group_id] = []
        
        self.members[group_id].append(user)
        return True
    
    def remove_member(self, group_id: int, user_id: int) -> bool:
        """
        Remove a member from a group
        
        Args:
            group_id: Group chat ID
            user_id: User ID to remove
            
        Returns:
            True if successful
        """
        if group_id not in self.members:
            return False
        
        self.members[group_id] = [m for m in self.members[group_id] if m["id"] != user_id]
        return True
    
    def get_group_members(self, group_id: int) -> List[Dict[str, Any]]:
        """Get all members of a group"""
        return self.members.get(group_id, [])
    
    def get_group_info(self, group_id: int) -> Optional[Dict[str, Any]]:
        """Get group information"""
        return self.groups.get(group_id)
    
    def simulate_user_joined(self, group_id: int, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate a user joining the group
        
        Args:
            group_id: Group chat ID
            user: User who joined
            
        Returns:
            The created update object
        """
        if group_id not in self.groups:
            raise ValueError(f"Group {group_id} does not exist")
        
        self.add_member(group_id, user)
        
        message = {
            "message_id": self.mock_server._next_message_id(),
            "from": user,
            "chat": self.groups[group_id],
            "date": int(datetime.now().timestamp()),
            "new_chat_members": [user]
        }
        
        update = {
            "update_id": self.mock_server._next_update_id(),
            "message": message
        }
        
        self.mock_server.updates_queue.put(update)
        
        return update
    
    def simulate_user_left(self, group_id: int, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate a user leaving the group
        
        Args:
            group_id: Group chat ID
            user: User who left
            
        Returns:
            The created update object
        """
        if group_id not in self.groups:
            raise ValueError(f"Group {group_id} does not exist")
        
        self.remove_member(group_id, user["id"])
        
        message = {
            "message_id": self.mock_server._next_message_id(),
            "from": user,
            "chat": self.groups[group_id],
            "date": int(datetime.now().timestamp()),
            "left_chat_member": user
        }
        
        update = {
            "update_id": self.mock_server._next_update_id(),
            "message": message
        }
        
        self.mock_server.updates_queue.put(update)
        
        return update
