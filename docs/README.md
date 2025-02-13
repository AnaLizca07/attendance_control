# Attendance_Controll

## Descripción
 **Attendance_Control** es un sistema de control de asistencia basado en el uso de un huellero biométrico. Su principal función es gestionar los registros de asistencia de manera eficiente, generando y almacenando los datos en archivos JSON mediante Python. Posteriormente, estos datos se envían a la nube para su almacenamiento y administración, facilitando el acceso y la supervisión en tiempo real.

## Características
+ Registro de asistencia mediante mediante huellero biométrico.
+ Generación automática de archvios JSON con los registros.
+ Envío seguro de los datos a la nube para su gestión.
+ Interfaz simple y eficiente para la administración de asistencias.

## Tecnologías Utilizadas
+ **Python**: Para el procesamiento y generacion de los archivos JSON
+ **Huella biométrica**: Como método principal de registro de asistencia.
+ **Almacenamiento en la nube**: Para el control y monitoreo remoto de los datos.

## Instalación y Uso
### Requisitos previos 
Tener **Python >=3.11.3** instalado en el sistema.
### Instalación
1. Clonar repositorio:
```bash
git clone https://github.com/AnaLizca07/attendance_control.git
```
2. Instalar dependencias necesarias:
```bash
pip install -r requirements.txt
```
### Depencias Necesarias
```ini
Cython
distlib
filelock
platformdirs
ply
pyzk
shiboken6
six
thriftpy2
zk
zklib
```