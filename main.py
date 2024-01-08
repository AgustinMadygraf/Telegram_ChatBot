# -*- coding: utf-8 -*-
# main.py
import os
import json
import time
import sys
import telegram
import asyncio
from gpt4all import GPT4All
import TelegramChatArchiver
from bot.utils import limpiar_pantalla, guardar_chat_history
from bot.bot import send, send_a
from bot.processing import cargar_chat_history, procesar_respuesta
import config  
from utils.logger import setup_logging
import logging

setup_logging()

async def main():
    logging.info("Inicio del programa")
    limpiar_pantalla()
    logging.info(f"Versión de Python: {sys.version}")

    logging.info("Inicializando...")
    logging.info(f"El archivo seleccionado para trabajar es: {config.CHAT_HISTORY_PATH}")
    
    user_id_str = str(593052206)
    i = 2

    opcion_ram = input("Selecciona la capacidad de tu memoria RAM: 1 (1 GB), 2 (4 GB), 3 (8 GB), 4 (16 GB): \n")
    if opcion_ram not in config.MODELOS_POR_RAM:
        opcion_ram = "2"
    ram_seleccionada = config.MODELOS_POR_RAM.get(opcion_ram)

    modelos_a_mostrar = config.MODELOS_DISPONIBLES.get(ram_seleccionada, [])
    if modelos_a_mostrar:
        logging.info(f"Modelos disponibles para RAM de {ram_seleccionada} seleccionada:")
        for idx, modelo in enumerate(modelos_a_mostrar, 1):
            logging.info(f"{idx}. {modelo}")

    seleccion_numero = input("\nSelecciona el número del modelo: ")
    if seleccion_numero.isdigit() and 1 <= int(seleccion_numero) <= len(modelos_a_mostrar):
        seleccion_modelo = modelos_a_mostrar[int(seleccion_numero) - 1]
    else:
        seleccion_modelo = modelos_a_mostrar[0]

    if seleccion_modelo:
        try:
            inicio_carga = time.time()  # Iniciar el contador de tiempo
            print("inicializando...")
            model = GPT4All(seleccion_modelo, config.MODEL_PATH)
            fin_carga = time.time()  # Finalizar el contador de tiempo
            tiempo_carga = fin_carga - inicio_carga  # Calcular la duración de la carga
            logging.info(f"Modelo inicializado con éxito en {tiempo_carga:.2f} segundos.")
        except ValueError as e:
            logging.error(f"Error al inicializar el modelo: {e}")
            model = None

        if model:
            i = 2
            seg = 5
            with model.chat_session(config.SYSTEM_TEMPLATE):
                while True:
                    await TelegramChatArchiver.main()
                    chat_history, user_info, ultimo_rol = cargar_chat_history(config.CHAT_HISTORY_PATH)
                    logging.info(f"Último mensaje en la conversación: rol '{ultimo_rol}'")
                    if ultimo_rol == "user":     
                        seg = 5
                        await send_a()
                        await procesar_respuesta(chat_history, user_id_str, model, i, user_info, seleccion_modelo, config.TELEGRAM_TOKEN)
                    else:
                        #limpiar_pantalla()
                        logging.info("Esperando consulta desde Telegram")
                        for seg_temp in range(seg, 0, -1):
                            print(f"Continuando en {seg_temp} segundos...", end="\r")
                            time.sleep(1)
                        if seg < 6:
                            seg += 1

                        await TelegramChatArchiver.main()

        else:
            logging.warning("No se pudo inicializar el modelo.")
    else:
        logging.warning("No se ha inicializado ningún modelo.")

if __name__ == '__main__':
    asyncio.run(main())
