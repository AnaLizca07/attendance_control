from enum import Enum
from zk import const

class UserPrivilege(Enum):
    """
    Enum that represents user privilege levels in the system.
    
    Attributes:
        ADMIN: Administrator privilege level, value from const.USER_ADMIN.
        USER: Regular user privilege level, value is the string "User".
    """
    ADMIN = const.USER_ADMIN
    USER = "User"
    
    @classmethod
    def from_device_privilege(cls, privilege: int) -> 'UserPrivilege':
        """
        Converts a device privilege integer to the corresponding UserPrivilege enum.
        
        Args:
            privilege (int): The privilege level from the device.
            
        Returns:
            UserPrivilege: ADMIN if the privilege matches const.USER_ADMIN, otherwise USER.
        """
        return cls.ADMIN if privilege == const.USER_ADMIN else cls.USER
        
    def __str__(self) -> str:
        """
        Returns the string representation of the privilege.
        
        Returns:
            str: The value of the enum (either const.USER_ADMIN or "User").
        """
        return self.value