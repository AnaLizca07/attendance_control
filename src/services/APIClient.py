import requests
from typing import Dict, Optional
import json
from datetime import datetime
import os

class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def login(self, email:str, password: str) -> bool:
        try:
            response = self.session.post(
                f"{os.getenv('URL_BASE')}{os.getenv('TOKEN')}", 
                json={
                    "email": email,
                    "password": password
                }
            )
            response.raise_for_status()

            data = response.json()
            self.token = data.get('token') #Validate the name with the postman collection when Luisa gives to me the project

            if self.token:
                self.session.headers.update({
                    'X-CSRF-TOKEN' : {self.token}
                })
                print("Login successful")
                return True

            print("Login failed: No token received")
            return False

        except requests.exceptions.RequestException as e:
            print(f"Login error: {str(e)}")
            return False
        
    def send_attendance_data(self, attendance_data: Dict) -> bool:
        if not self.token:
            email = os.getenv('LOGIN_EMAIL')
            password = os.getenv('LOGIN_PASSWORD')

            if not email or not password:
                print('Login credentials not found in enviroment variables')
                return False
            
            if not self.login(email, password):
                print("Automatic login failed.")
                return False
            
        try:
            response = self.session.post(
                f"{os.getenv('URL_BASE')}{os.getenv('ATTENDANCE')}"
            )
            response.raise_for_status()

            print(f"Data sent successfully. Status code: {response.status_code}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {str(e)}")
            return False