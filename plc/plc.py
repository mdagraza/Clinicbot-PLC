import snap7, time

from log.logger import write_log

def data_plc(plc, plc_config: dict):
  if not plc.get_connected():
    connect_plc(plc_config)

  return plc.db_read(int(plc_config["numero_db"]), int(plc_config["primer_byte"]), int(plc_config["tamano"]))

def connect_plc(plc_config: dict):
  try:
    plc = snap7.client.Client()
    plc.connect(plc_config["ip"], int(plc_config["rack"]), int(plc_config["slot"]))
    return plc
  except Exception as e:
    write_log(f"Error al conectar al PLC: {e}", level="error")
    time.sleep(2)
    connect_plc(plc_config)