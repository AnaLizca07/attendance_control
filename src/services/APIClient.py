import requests
from typing import Dict, Optional
import json
from datetime import datetime
import os

class APIClient:
    def __init__(self):
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


    def login(self, email:str, password: str) -> bool:
        try:
            response = self.session.post(
                f"{self.base_url}{self.token_path}", 
                json={
                    "email": email,
                    "password": password
                }
            )
            response.raise_for_status()

            data = response.json()
            self.token = data.get('token')

            if self.token:
                self.session.headers.update({
                    'X-CSRF-TOKEN' : self.token
                })
                print("Login successful")
                return True

            print("Login failed: No token received")
            return False

        except requests.exceptions.RequestException as e:
            print(f"Login error: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error during login: {str(e)}")
            return False
        
        
    def ensure_athenticated(self) -> bool:
        if self.token:
            return True
        
        return self.login(self.email, self.password)
    

    def send_attendance_data(self, attendance_data: Dict) -> bool:
        if not self._ensure_authenticated():
            return False  
         
        try:
            response = self.session.post(
                f"{self.base_url}{self.attendance_path}",
                json=attendance_data
            )
            response.raise_for_status()

            print(f"Data sent successfully. Status code: {response.status_code}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {str(e)}")
            return False
        

    def send_device_data(self, device_data: Dict) -> bool:
        if not self._ensure_authenticated():
            return False  
         
        try:
            response = self.session.post(
                f"{self.base_url}{self.device_path}",
                json=device_data
            )
            response.raise_for_status()

            print(f"Data sent successfully. Status code: {response.status_code}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {str(e)}")
            return False
        
        