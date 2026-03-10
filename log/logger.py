import logging
from logging.handlers import TimedRotatingFileHandler
import os

logger = None

def logger_setup(log_name):
  # Crear carpeta si no existe
  logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
  os.makedirs(logs_path, exist_ok=True)

  global logger
  logger = logging.getLogger(log_name)
  logger.setLevel(logging.INFO)

  # Handler que rota cada día
  handler = TimedRotatingFileHandler(
      (os.path.join(logs_path, f"{log_name}.log")),
      when="midnight", # Cambiar archivo a partir de medianoche
      interval=1, # Cambiar archivo cada 1 día
      backupCount=30, # Cuantos días de logs mantener
      encoding="utf-8",
      delay=True
  )

  # Cambiar el formato del nombre del archivo. Por defecto: log_name.log.2024-06-30
  def change_format(default_name):
    base = os.path.basename(default_name)
    name, formato, date = base.split(".")
    file_name = f"{date}_{name}.{formato}"
    return os.path.join(os.path.dirname(default_name), file_name)
  
  handler.namer = change_format

  # Formato del log
  formatter = logging.Formatter(
      "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
  )

  handler.setFormatter(formatter)

  # Añadir handler
  logger.addHandler(handler)

# Se escriben los logs aquí, para no tener que importar el logger constantemente que se quiera usar
def write_log(message, level="info"):
    log_func = getattr(logger, level.lower(), None) #getattr(object, name, [que devuelve si  no existe])
    if log_func:
        log_func(message)
    else:
        logger.warning(f"{level} INEXISTENTE | {message}")