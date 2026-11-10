"""Configuración por ambiente leída de variables de entorno.

La misma imagen Docker sirve para desarrollo, pruebas y producción; solo cambian
estas variables. Las credenciales nunca se escriben en el código.
"""

import os


def ambiente():
    return os.environ.get("APP_ENV", "desarrollo")


def url_base_de_datos():
    return os.environ.get("DATABASE_URL", "")
