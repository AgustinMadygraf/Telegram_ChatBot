import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Crear un handler que escribe los mensajes de log en un archivo, rotando después de cierto tamaño
    log_file = os.path.join("logs", "app.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)  # 1MB por archivo, máximo 5 archivos
    file_handler.setLevel(logging.ERROR)  # Capturar solo errores y mensajes más críticos para el archivo
    file_handler.setFormatter(logging.Formatter(log_format))

    # Añadir el file handler al logger raíz
    logging.getLogger('').addHandler(file_handler)

# Llama a setup_logging al inicio de tu aplicación
setup_logging()
