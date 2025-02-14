from enum import Enum
from zk import const

class UserPrivilege(Enum):
    ADMIN = const.USER_ADMIN
    USER = "User"
    
    @classmethod
    def from_device_privilege(cls, privilege: int) -> 'UserPrivilege':
        return cls.ADMIN if privilege == const.USER_ADMIN else cls.USER
        
    def __str__(self) -> str:
        return self.value