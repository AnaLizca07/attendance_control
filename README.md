# Attendance_Controll

### Authors
- Ana Lucelly
- Sergio Chica 

## Description
**Attendance_Control** is an attendance control system based on the use of a biometric fingerprint scanner. Its main function is to efficiently manage attendance records, generating and storing data in JSON files using Python. This data is then sent to the cloud for storage and management, facilitating daily access and monitoring.

## Features
- Attendance registration through a biometric fingerprint scanner.
- Automatic generation of JSON files with attendance records.
- Log storage in SQLite
- Secure data transfer to the cloud for management.

## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
- **Biometric fingerprint scanner**: As the primary method for attendance registration.
- **Python**: For processing and generating JSON files.
- **SQLite**: For logging error logs or validations.
- **Cloud storage**: For remote control and monitoring of the data.

## Installation and Usage

### Prerequisites
- Ensure **Python >=3.11.3** is installed on the system.
- Ensure **pip 22.3.1** is installed on the system.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AnaLizca07/attendance_control.git
    ```
2. Create the virtual environment:
   ```bash
   python -m venv virtual_attendance_control 
    ```
3. Activate the virtual environment:
   ```bash
   virtual_attendance_control/Scripts/activate
    ```
4. Install the required dependencies:
   ```bash
   pip install --no-deps -r requirements.txt
    ```
   >--no-deps: Prevents pip from installing dependencies of the listed packages.
### Usage
1. Setting environment variables:

    >[Environment variables](.env.example)
2. Execute program:
   ```bash
   python Main.py
    ```
### Required Dependencies
   ```bash
    pip 
    setuptools 
    wheel
    future
    load-dotenv
    ntplib
    python-dotenv
    pytz
    pyzk
    zk
```
- `ntplib`: Provides an interface for querying NTP (Network Time Protocol) servers, useful for synchronizing the system clock with time servers on the Internet.
- `pip`: Python’s package manager, used to install, update, and manage third-party libraries and dependencies
- `pytz`: Provides support for time zones, allowing conversion between different time zones based on the IANA time zone database.
- `pyzk`: A library used to interact with biometric devices from the ZKTeco brand, such as fingerprint readers and access control systems.
- `pyzmq`: A binding for ZeroMQ, an asynchronous messaging library that enables efficient communication between processes and networked computers.
- `setuptools`: A tool for managing Python packages, providing advanced functions for installation, distribution, and development of modules.
- `wheel`: A `setuptools` companion that enables the creation and management of `.whl` package files, making package installations faster and more efficient.
- `future`: Provides compatibility between Python 2 and 3, allowing you to write code that works on both versions without major modifications.
- `load-dotenv`: Similar to `python-dotenv`, it is used to load environment variables from a `.env` file, making it easier to configure projects without exposing credentials in the source code.
- `zk`: A library related to handling biometric devices, similar to `pyzk`, allowing interaction with access control devices such as ZKTeco.