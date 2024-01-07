# -*- coding: utf-8 -*-
#ChatBot_Telegram_LLM.py 
import os
import json
import time
import sys
import telegram
import asyncio
from pathlib import Path
from gpt4all import GPT4All
import TelegramChatArchiver
from bot.utils import limpiar_pantalla, guardar_chat_history
from bot.bot import send, send_a
from bot.processing import cargar_chat_history, procesar_respuesta



async def main():
    limpiar_pantalla()
    print("Versión de Python:")
    print(sys.version)
    print("")
    print("Inicializando...")
    chat_history_path = "context_window_telegram.json"
    print(f"El archivo seleccionado para trabajar es: {chat_history_path}")
    
    user_id_str = str(593052206)
    i = 2
# Agrupando modelos por requisitos de RAM
    modelos_por_ram = {
        "1": "1 GB",
        "2": "4 GB",
        "3": "8 GB",
        "4": "16 GB"
    }

    modelos_disponibles = {
        "1 GB": ["all-MiniLM-L6-v2-f16.gguf"],
        "4 GB": ["replit-code-v1_5-3b-q4_0.gguf"],
        "8 GB": ["mistral-7b-openorca.Q4_0.gguf", "mistral-7b-instruct-v0.1.Q4_0.gguf",
                "gpt4all-falcon-q4_0.gguf", "gpt4all-13b-snoozy-q4_0.gguf", "orca-2-7b.Q4_0.gguf",
                "mpt-7b-chat-merges-q4_0.gguf"],
        "16 GB": ["orca-2-13b.Q4_0.gguf", "wizardlm-13b-v1.2.Q4_0.gguf", "nous-hermes-llama2-13b.Q4_0.gguf","mixtral-8x7b-v0.1.Q4_K_M.gguf"]
    }

    # Preguntar por la capacidad de RAM
    opcion_ram = input("Selecciona la capacidad de tu memoria RAM: 1 (1 GB), 2 (4 GB), 3 (8 GB), 4 (16 GB): \n")
    if opcion_ram not in ["1", "2", "3", "4"]:
        opcion_ram = "2"
    ram_seleccionada = modelos_por_ram.get(opcion_ram)

    # Mostrar modelos disponibles para la RAM seleccionada
    modelos_a_mostrar = modelos_disponibles.get(ram_seleccionada, [])
    if modelos_a_mostrar:
        print(f"Modelos disponibles para RAM de {ram_seleccionada} seleccionada : ")
        for idx, modelo in enumerate(modelos_a_mostrar, 1):
                print(f"{idx}. {modelo}")

    # Solicitar la selección del modelo por número
    seleccion_numero = input("\nSelecciona el número del modelo: ")

    # Verificar si la entrada es válida
    if seleccion_numero.isdigit() and 1 <= int(seleccion_numero) <= len(modelos_a_mostrar):
        seleccion_modelo = modelos_a_mostrar[int(seleccion_numero) - 1]
    else:
        seleccion_modelo = modelos_a_mostrar[0]  # Selecciona el primer modelo por defecto

    if seleccion_modelo:
        print(f"\nSeleccionaste {seleccion_modelo} \n")
        print("Espere, está cargardo los parámetros en la memoria RAM")
    else:
        print("No se ha seleccionado ningún modelo.")

    system_template = '### System:\nResponde siempre en español. Eres un asistente de IA que sigue las instrucciones extremadamente bien. Ayuda tanto como puedas.'

    # Continuar con el proceso si se ha seleccionado un modelo
    if seleccion_modelo:
        model_path = 'E:\Model _Explorer'
        try:
            model = GPT4All(seleccion_modelo, model_path)
            print("Gracias por esperar.")
        except ValueError as e:
            print(f"Error al inicializar el modelo: {e}")
            model = None

        if model:
            print("\nInicializando...\n")
            print("model_path: ", model_path)
            i = 2 
            seg = 5  # Inicializa seg fuera del bucle

            with model.chat_session(system_template):
                while True:
                    await TelegramChatArchiver.main()
                    chat_history, user_info, ultimo_rol = cargar_chat_history(chat_history_path)
                    if ultimo_rol:
                        print(f"El último mensaje en la conversación con el usuario 593052206 fue de un '{ultimo_rol}'.")
                    if ultimo_rol == "user":     
                        seg = 5  # Restablece seg a 5 cuando hay una respuesta del usuario
                        await send_a()
                        await procesar_respuesta(chat_history, user_id_str, model, i, user_info, seleccion_modelo, chat_id)
                    else:
                        limpiar_pantalla()
                        print("Esperando consulta desde Telegram")
                        for seg_temp in range(seg, 0, -1):  # Cuenta regresiva desde seg hasta 1
                            print(f"Continuando en {seg_temp} segundos...", end="\r")
                            time.sleep(1)
                        print("\nContinuando.")
                        if seg < 60:
                            seg += 1  # Incrementa seg, pero no más de 60 segundos

                        await TelegramChatArchiver.main()

        else:
            print("No se pudo inicializar el modelo.")
    else:
        print("No se ha inicializado ningún modelo.")

chat_history_path = "context_window_telegram.json"
chat_id=593052206
if __name__ == '__main__':
    asyncio.run(main())