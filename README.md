# Attendance_Controll

## Description
**Attendance_Control** is an attendance control system based on the use of a biometric fingerprint scanner. Its main function is to efficiently manage attendance records, generating and storing the data in JSON files using Python. Subsequently, these data are sent to the cloud for storage and management, facilitating real-time access and supervision.

## Features
- Attendance registration using a biometric fingerprint scanner.
- Automatic generation of JSON files with attendance records.
- Secure data transfer to the cloud for management.
- Simple and efficient interface for attendance administration.

## Technologies Used
- **Python**: For processing and generating JSON files.
- **Biometric fingerprint scanner**: As the primary method for attendance registration.
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
2. Install the required dependencies:
   ```bash
   pip install --no-deps -r requirements.txt
    ```
### Required Dependencies
   ```bash
    ntplib  
    pip 
    pytz 
    pyzk    
    pyzmq 
    setuptools 
    wheel
```
- `ntplib`: Provides an interface for querying NTP (Network Time Protocol) servers, useful for synchronizing the system clock with time servers on the Internet.
- `pip`: Python’s package manager, used to install, update, and manage third-party libraries and dependencies
- `pytz`: Provides support for time zones, allowing conversion between different time zones based on the IANA time zone database.
- `pyzk`: A library used to interact with biometric devices from the ZKTeco brand, such as fingerprint readers and access control systems.
- `pyzmq`: A binding for ZeroMQ, an asynchronous messaging library that enables efficient communication between processes and networked computers.
- `setuptools`: A tool for managing Python packages, providing advanced functions for installation, distribution, and development of modules.
- `wheel`: A `setuptools` companion that enables the creation and management of `.whl` package files, making package installations faster and more efficient.