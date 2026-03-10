from api.auth import obtener_token
from api.utils import safe_request

from log.logger import write_log

def enviar_datos(api_config: dict, datos):
    _token = obtener_token(api_config)

    headers = {
        "Authorization": f"Bearer {_token}",
        "Content-Type": "application/json"
    }

    write_log(f"Enviando al servidor : {datos}")

    r = safe_request("POST", api_config["url"], api_config["endpoint"], json=datos, headers=headers)

    if r is None:
        return 0
    
    if r:
        return 1
    elif r.status_code == 401:
        write_log("Token expirado o inválido, obteniendo nuevo token.", level="warning")
        obtener_token(api_config, force_refresh=True)
        return 0
    elif r.status_code == 409:
        return 2
    else:
        return 0