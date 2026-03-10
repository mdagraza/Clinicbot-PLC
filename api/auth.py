import json, os
from datetime import datetime, timedelta
from api.utils import safe_request

from log.logger import write_log

_token = None
EXPIRATION_MARGEN = timedelta(minutes=1)

def obtener_token(api_config: dict, force_refresh=False):
    global _token
    if not _token:
        _token = leer_archivo_datos()

    if force_refresh or not _token["key"] or _token["expiration"] <= datetime.now() + EXPIRATION_MARGEN:
        bearer = {
            "user": api_config["user"],
            "pass": api_config["password"],
            "expires": int(api_config["tiempo_expiracion"])
        }
        r = safe_request("POST", api_config["url"], 'token', json=bearer)

        if r:
            _token["key"] = r.json()["access_token"]
            _token["expiration"] = datetime.now()+timedelta(hours=int(r.json()["expires_in_hours"]))
            with open(ruta_json("datos.json"), "w") as f:
                data = {
                    "key": _token["key"],
                    "expiration": _token["expiration"].timestamp()
                }
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            write_log("No se pudo obtener token", level="error")

        
    return _token["key"]

def leer_archivo_datos():
    try:
        with open(ruta_json("datos.json"), "r") as f:
            data = json.load(f)
            return {
                "key": data["key"],
                "expiration": datetime.fromtimestamp(data["expiration"])
            }
    except FileNotFoundError:
        default = {
            "key": "",
            "expiration": datetime.now()-timedelta(days=1)
        }
        return default
    
def ruta_json(nombre):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio_actual, nombre)
