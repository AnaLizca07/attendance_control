from dataclasses import dataclass
from typing import Dict
from models.user.UserPrivilege import UserPrivilege

@dataclass
class UserInfo:
    """
    Class that represents basic user information in the system.
    
    Attributes:
        user_id (int): Unique identifier for the user.
        name (str): User's name.
        privilege (UserPrivilege): User's privilege level, using the UserPrivilege enum.
    """
    user_id: int
    name: str
    privilege: UserPrivilege
    
    def to_dict(self) -> Dict:
        """
        Converts the UserInfo instance to a dictionary.
        
        Returns:
            Dict: Dictionary containing user data. The privilege is converted to a string.
        """
        return {
            'user_id': self.user_id,
            'name': self.name,
            'privilege': str(self.privilege)
        }