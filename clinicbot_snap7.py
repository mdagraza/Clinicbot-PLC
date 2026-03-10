from snap7.util import *
import asyncio

from config.config import *
from api.enviar_datos import enviar_datos
from plc.plc import data_plc, connect_plc

from log.logger import logger_setup, write_log

#Configuración del logger
logger_setup("Clinicbot-Log")

#Configuraciones
plc_config = config_ini("PLC")
plc_vars_config = config_ini("PLC_VARIABLES")
api_config = config_ini("API_REST")
general_config = config_ini("GENERAL")

#Identificacion actual y anterior
identificacion = None
ult_identificacion = None

#Conexion al PLC
plc = connect_plc(plc_config)

#Lista de identificaciones leídas
identificaciones_leidas = []

#Leer variables
async def lectura_variables():
    while True:
        data = data_plc(plc, plc_config)

        if int(general_config["usar_trigger"]) == 0 or get_bool(data, int(plc_vars_config["trigger"].split('.')[0]), int(plc_vars_config["trigger"].split('.')[1])):
            identificacion = get_string(data, int(plc_vars_config["identificacion"]))

        if identificacion != ult_identificacion and identificacion and identificacion != "Error":
            datos = {
                "identificacion": identificacion,
                "color": get_int(data, int(plc_vars_config["color"])) #1: Azul | 2: Verde | 3: Rosa
            }
            identificaciones_leidas.append(datos)
        
        await asyncio.sleep(float(general_config["tiempo_espera_plc"]))

#Ejecucion de envio al API
async def envio_API():
    while True:
        if len(identificaciones_leidas) > 0:
            estado = enviar_datos(api_config, identificaciones_leidas[0])

            if estado == 1:
                write_log(f"Identificacion enviada: {identificaciones_leidas[0]}")
                global ult_identificacion
                ult_identificacion = identificacion
                identificaciones_leidas.remove(identificaciones_leidas[0])
            elif estado == 2:
                write_log(f"Identificacion repetida en servidor: {identificaciones_leidas[0]}", level="warning")
                identificaciones_leidas.remove(identificaciones_leidas[0])
            else:
                write_log(f"No se ha podido enviar la información al servidor", level="error")

        await asyncio.sleep(float(general_config["tiempo_espera_envio"]))

async def main():
    await asyncio.gather(lectura_variables(), envio_API())

asyncio.run(main())