from typing import Dict, List
from models.user.UserInfo import UserInfo
from models.user.UserPrivilege import UserPrivilege
from config.Logging import Logger

class UserRepository:
    """
    Repository class responsible for retrieving and processing user data from a connector source.
    
    This class provides methods to fetch user information and convert it into the application's
    domain model representation.
    """
    
    def __init__(self, connector):
        """
        Initialize the UserRepository with a data connector.
        
        Args:
            connector: The connector object used to communicate with the data source.
        """
        self.connector = connector
        self.log = Logger.get_logger()
    
    def get_users_info(self) -> Dict[int, Dict]:
        """
        Retrieves all users' information from the data source.
        
        Returns:
            Dict[int, Dict]: A dictionary mapping user IDs to their information dictionaries.
            Returns an empty dictionary if an error occurs.
        
        Raises:
            ConnectionError: If connection to the data source fails.
        """
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
        """
        Fetches the raw user data from the connector.
        
        Returns:
            List: A list of raw user objects from the data source.
        """
        return self.connector.get_users()
    
    def _process_users(self, users: List) -> Dict[int, Dict]:
        """
        Processes a list of raw user objects into a dictionary of user information.
        
        Args:
            users (List): List of raw user objects from the data source.
            
        Returns:
            Dict[int, Dict]: A dictionary mapping user IDs to their information dictionaries.
        """
        return {
            user.user_id: self._create_user_info(user).to_dict()
            for user in users
        }
    
    def _create_user_info(self, user) -> UserInfo:
        """
        Creates a UserInfo object from a raw user object.
        
        Args:
            user: Raw user object from the data source.
            
        Returns:
            UserInfo: A domain model UserInfo object with the user's data.
        """
        return UserInfo(
            user_id=user.user_id,
            name=user.name,
            privilege=UserPrivilege.from_device_privilege(user.privilege)
        )
    
    def _handle_error(self, error_message: str) -> None:
        """
        Logs an error message.
        
        Args:
            error_message (str): The error message to log.
        """
        self.log.error(error_message)