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
    Cython
    distlib
    filelock
    pip
    platformdirs
    ply
    pyzk
    setuptools
    shiboken6
    six
    zk
    zklib