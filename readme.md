# ClinicBot-PLC: Comunicación Industrial y Control

Este repositorio contiene el modulo de comunicacion industrial de **ClinicBot**. Su funcion principal es establecer el puente de datos entre el backend de gestion (Django/Python) y el hardware de automatizacion (PLC Siemens) utilizando el protocolo de comunicacion S7.

El proyecto se enmarca dentro de la iniciativa de Laboratorio Clinico Robotizado financiada por los fondos **Next Generation EU**.

## Caracteristicas Tecnicas

* **Comunicacion S7:** Implementacion del protocolo Siemens S7 mediante la libreria `python-snap7`.
* **Lectura/Escritura de DBs:** Gestion de bloques de datos (Data Blocks) para el intercambio de señales de control y estado.
* **Sincronizacion en Tiempo Real:** Monitorizacion de variables industriales para coordinar el brazo robotico con el sistema de analisis.
* **Interfaz de Diagnostico:** Scripts para verificar la conexion y el estado de las entradas/salidas del PLC.

## Tecnologias Utilizadas

* **Python 3.10+**
* **Snap7:** Libreria de comunicacion de codigo abierto para CPUs Siemens S7.
* **Siemens TIA Portal:** Para la configuracion del hardware y bloques de datos en el PLC (S7-1200 / S7-1500).
* **Docker:** Para entornos de prueba y simulacion de red.


## Requisitos Previos

1. **Configuracion del PLC:**
   - Permitir acceso "PUT/GET" en la configuracion de seguridad de la CPU.
   - El bloque de datos (DB) debe tener desactivada la "Optimizacion de acceso al bloque".
2. **Dependencias de Sistema:**
   - Es necesario tener instalada la libreria compilada de Snap7 (`snap7.dll` en Windows o `libsnap7.so` en Linux).

## Instalacion

```bash
# Clonar el repositorio
git clone https://github.com/mdagraza/Clinicbot-PLC.git
cd Clinicbot-PLC

# Instalar dependencias
pip install python-snap7