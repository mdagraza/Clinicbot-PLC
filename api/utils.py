import requests

from log.logger import write_log

def safe_request(method, url, endpoint, **kwargs):
    url = f"{url}/api/{endpoint}/"
    r = None
    try:
        r = requests.request(method, url, timeout=3, **kwargs)
        r.raise_for_status()
        return r

    except requests.exceptions.ConnectionError:
        write_log(f"No se pudo conectar al servidor (URL o puerto incorrecto) o sin conexión a Internet, URL: {url}", level="critical")
    except requests.exceptions.Timeout:
        write_log(f"La solicitud excedió el tiempo de espera, URL: {url}", level="error")
    except requests.exceptions.HTTPError as e:
        write_log(f"Error HTTP {e.response.status_code}: {e.response.text}, URL: {url}", level="error")
    except requests.exceptions.RequestException as e:
        write_log(f"Error inesperado: {e}, URL: {url}", level="error")

    return r
