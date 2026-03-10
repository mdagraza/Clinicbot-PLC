import configparser, os

from log.logger import write_log

_config = None

def leer_config():
  global _config
  _config = configparser.ConfigParser(
    inline_comment_prefixes=(';')
  )
  base_path = os.path.dirname(os.path.abspath(__file__))
  config_path = os.path.join(base_path, 'config.ini')
  
  if not os.path.exists(config_path):
      write_log(f"ERROR: Archivo de configuración no encontrado : {config_path}", level="error")
      return None
  
  _config.read(config_path)

def config_ini(cabecera):
  global _config
  if _config is None:
    leer_config()
  
  return dict(_config[cabecera])