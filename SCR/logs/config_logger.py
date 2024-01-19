#SCR/logs/config_logger.py
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

class InfoErrorFilter(logging.Filter):
    def filter(self, record):
        # Permitir solo registros de nivel INFO y ERROR
        return record.levelno in (logging.INFO, logging.ERROR)

def configurar_logging(nivel=logging.INFO):
    logger = logging.getLogger()
    if logger.hasHandlers():
        return logger

    # Configuración básica
    filename = 'SCR/logs/sistema.log'
    format = '%(asctime)s - %(levelname)s - %(module)s - %(filename)s:%(lineno)d: %(message)s'
    maxBytes = 10485760  # 10MB
    backupCount = 5
    formatter = logging.Formatter(format)

    # File Handler
    file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console Handler con filtro personalizado
    console_handler = logging.StreamHandler()
    console_handler.addFilter(InfoErrorFilter())  # Aplicar el filtro
    console_handler.setFormatter(formatter)

    logger.setLevel(nivel)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("\n\n--------------- Nueva Sesión - {} - Nivel de Registro: {} ---------------\n\n".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), logging.getLevelName(logger.getEffectiveLevel())))

    return logger

# Configurar el logger con un nivel específico
configurar_logging(nivel=logging.DEBUG)
