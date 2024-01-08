# bot/processing.py
import asyncio
import json
from bot.utils import limpiar_pantalla, guardar_chat_history  
from bot.bot import send, send_a
import config 
import time
import os

async def procesar_respuesta(chat_history, user_id, model, i, user_info, seleccion_modelo, chat_id):
    user_id_str = str(user_id)
    user_messages = chat_history.get(user_id_str, [])
    
    if user_messages:
        prompt = user_messages[0]['content']
    else:
        prompt = "Continúa"

    print(f"last prompt: {prompt}")
    print("\nConsultado a la IA local, CPU está trabajando. Espere por favor. \n\n")

    inicio_generacion = time.time()
    tokens = []
    print(f"\nIncovando a **{seleccion_modelo}**\n ")
    for token in model.generate(prompt, temp=0, streaming=True):
        # Agregar el token a la lista
        tokens.append(token)
        # Imprimir la respuesta hasta el momento
        print(token, end='', flush=True)
    fin_generacion = time.time()
    tiempo_generacion = fin_generacion - inicio_generacion
    print(f"\nGracias por esperar. El tiempo de generación de respuesta fue de {tiempo_generacion:.2f} segundos")


    n = len(model.current_chat_session) - 1

    if n >= 0 and len(model.current_chat_session) > n:
        print(f"\nmodel.current_chat_session[n]['content']: {model.current_chat_session[n]['content']}\n")
        reply_content = "**" + seleccion_modelo + "** : " + model.current_chat_session[n]['content']
        # Utiliza la ruta del archivo desde config.py
        guardar_chat_history(chat_history, user_info, config.CHAT_HISTORY_PATH, chat_id, reply_content,seleccion_modelo)
        print("guardado con éxito. ")

        await send(reply_content,chat_id)
        
    else:
        print("No hay mensajes en la sesión de chat actual.")
    i = i + 1

def cargar_chat_history(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            chat_histories = data.get("chat_histories", {})
            user_info = data.get("user_info", {})

            ultimo_rol = None
            chat_usuario_especifico = chat_histories.get("593052206", [])
            if chat_usuario_especifico:
                primer_mensaje = chat_usuario_especifico[0]
                ultimo_rol = primer_mensaje.get("role")

            return chat_histories, user_info, ultimo_rol

    except FileNotFoundError:
        print(f"No se encontró el archivo: {file_path}. Por favor verifica la ruta.")
        return {}, {}, None
    except json.JSONDecodeError:
        print(f"Error al leer el archivo: {file_path}. Formato de archivo inválido.")
        return {}, {}, None
