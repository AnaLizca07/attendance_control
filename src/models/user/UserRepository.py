from typing import Dict, List
from models.user.UserInfo import UserInfo
from models.user.UserPrivilege import UserPrivilege
from config.Logging import Logger

class UserRepository:
    def __init__(self, connector):
        self.connector = connector
        self.log = Logger.get_logger()
    
    def get_users_info(self) -> Dict[int, Dict]:
        try:
            conn = self.connector.connect()
            if not conn:
                raise ConnectionError("Connection failed")
                
            users = conn.get_users() 
            return self._process_users(users)
            
        except Exception as e:
            self._handle_error(f"Error getting users info: {str(e)}")
            return {}
        finally:
            if self.connector:
                self.connector.disconnect()
            
    def _fetch_users(self) -> List:
        return self.connector.get_users()
    
    def _process_users(self, users: List) -> Dict[int, Dict]:
        return {
            user.user_id: self._create_user_info(user).to_dict()
            for user in users
        }
    
    def _create_user_info(self, user) -> UserInfo:
        return UserInfo(
            user_id=user.user_id,
            name=user.name,
            privilege=UserPrivilege.from_device_privilege(user.privilege)
        )
    
    def _handle_error(self, error_message: str) -> None:
        self.log.error(error_message) 