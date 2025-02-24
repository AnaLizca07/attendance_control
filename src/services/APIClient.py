import requests
from typing import Dict, Optional
import json
from datetime import datetime
from config.Logging import Logger
import os

class APIClient:
    """
    Client for interacting with a remote API to send attendance and device data.
    
    This client handles authentication with the remote API using token-based authentication
    and provides methods for sending attendance and device data to specific endpoints.
    
    Attributes:
        log: Logger instance for event logging.
        session (requests.Session): Session object to maintain connection state.
        token (Optional[str]): Authentication token received from the API.
        base_url (str): Base URL for the API from environment variables.
        token_path (str): Endpoint path for authentication from environment variables.
        attendance_path (str): Endpoint path for attendance data from environment variables.
        device_path (str): Endpoint path for device data from environment variables.
        email (str): Login email from environment variables.
        password (str): Login password from environment variables.
    """
    def __init__(self):
        """
        Initializes the API client with configuration from environment variables.
        
        Loads API configuration and credentials from environment variables:
        - URL_BASE: Base URL for the API
        - TOKEN: Authentication endpoint path
        - ATTENDANCE: Attendance data endpoint path
        - DEVICE: Device data endpoint path
        - LOGIN_EMAIL: Email for authentication
        - LOGIN_PASSWORD: Password for authentication
        """
        self.log = Logger.get_logger()
        self.session = requests.Session()
        self.token: Optional[str] = None
        self.base_url = os.getenv('URL_BASE')

        #Paths
        self.token_path = os.getenv('TOKEN')
        self.attendance_path = os.getenv('ATTENDANCE')
        self.device_path = os.getenv('DEVICE')

        #Credentials
        self.email = os.getenv('LOGIN_EMAIL')
        self.password = os.getenv('LOGIN_PASSWORD')


    def login(self, email: str, password: str) -> bool:
        """
        Authenticates with the API using provided credentials.
        
        This method makes an authentication request to the API, processes the response,
        and stores the received token for future requests if successful.
        
        Args:
            email (str): Email for authentication.
            password (str): Password for authentication.
            
        Returns:
            bool: True if authentication was successful, False otherwise.
        """
        try:

            auth_headers = {
                'email': email,
                'password': password
            }

            response = self.session.get(
                f"{self.base_url}{self.token_path}",
                headers=auth_headers
            )

            self.log.debug(f"Status code: {response.status_code}")
            self.log.debug(f"Response: {response.text[:200]}")

            response.raise_for_status()
            try:
                data = response.json()
                self.log.debug(f"JSON Response: {data}")
                
                if data.get('status') == 400 or 'Invalid credentials' in str(data):
                    self.log.error(f"API rejected authentication: {data}")
                    return False
                
                self.token = data.get('hash')

                if self.token:
                    self.session.headers.update({
                        'X-CSRF-TOKEN': self.token
                    })
                    self.log.debug("Login successful")
                    return True
                else:
                    self.log.error("No token found in response")
                    return False

            except json.JSONDecodeError:
                self.log.error("Response is not valid JSON")
                return False

        except requests.exceptions.RequestException as e:
            self.log.error(f"Login request error: {str(e)}")
            return False
        except Exception as e:
            self.log.error(f"Unexpected error during login: {str(e)}")
            return False
        
    def ensure_authenticated(self) -> bool:
        """
        Ensures the client has a valid authentication token.
        
        If a token already exists, it assumes it's valid. Otherwise, it attempts
        to login using the credentials from environment variables.
        
        Returns:
            bool: True if the client is authenticated, False otherwise.
        """
        if self.token:
            return True
        
        return self.login(self.email, self.password)
    

    def send_attendance_data(self, attendance_data: Dict) -> bool:
        """
        Sends attendance data to the API.
        
        This method ensures the client is authenticated before sending the data
        to the attendance endpoint using a PUT request.
        
        Args:
            attendance_data (Dict): Attendance data to send to the API.
            
        Returns:
            bool: True if the data was sent successfully, False otherwise.
        """
        if not self.ensure_authenticated():
            return False  
         
        try:
            response = self.session.put(
                f"{self.base_url}{self.attendance_path}",
                json=attendance_data
            )
            response.raise_for_status()

            self.log.info(f"Data sent successfully. Status code: {response.status_code}")
            return True
        
        except requests.exceptions.RequestException as e:
            self.log.error(f"Error sending data: {str(e)}")
            return False
        

    def send_device_data(self, device_data: Dict) -> bool:
        """
        Sends device data to the API.
        
        This method ensures the client is authenticated before sending the data
        to the device endpoint using a PUT request.
        
        Args:
            device_data (Dict): Device data to send to the API.
            
        Returns:
            bool: True if the data was sent successfully, False otherwise.
        """
        if not self.ensure_authenticated():
            return False  
         
        try:
            response = self.session.put(
                f"{self.base_url}{self.device_path}",
                json=device_data
            )
            response.raise_for_status()

            self.log.info(f"Data sent successfully. Status code: {response.status_code}")
            return True
        
        except requests.exceptions.RequestException as e:
            self.log.error(f"Error sending data: {str(e)}")
            return False
        
        