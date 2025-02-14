from dataclasses import dataclass
from typing import Dict
from models.user.UserPrivilege import UserPrivilege

@dataclass
class UserInfo:
    user_id: int
    name: str
    privilege: UserPrivilege
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'privilege': str(self.privilege)
        }