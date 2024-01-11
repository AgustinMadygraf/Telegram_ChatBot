import asyncio
import json
import logging
from bot.utils import limpiar_pantalla, guardar_chat_history
from bot.bot import send, send_a
import config
import time
import os

async def procesar_respuesta(chat_history, user_id, model, i, user_info, seleccion_modelo, chat_id, respuesta_rapida):
    user_id_str = str(user_id)
    user_messages = chat_history.get(user_id_str, [])
    print("\nrespuesta_rapida: ", respuesta_rapida)

    try:
        if user_messages:
            prompt = user_messages[0]['content'] if respuesta_rapida else user_messages
        else:
            prompt = "Continúa"

        print(f"\nlast prompt: {prompt}")
        print("\nConsultado a la IA local, CPU está trabajando. Espere por favor. \n\n---------------------")

        inicio_generacion = time.time()
        tokens = []
        print(f"\nInvocando a **{seleccion_modelo}**\n ")
        for token in model.generate(prompt, temp=0, streaming=True):
            tokens.append(token)
            print(token, end='', flush=True)
        fin_generacion = time.time()
        tiempo_generacion = fin_generacion - inicio_generacion
        print(f"\n\nGracias por esperar. El tiempo de generación de respuesta fue de {tiempo_generacion:.2f} segundos")

        n = len(model.current_chat_session) - 1
        if n >= 0 and len(model.current_chat_session) > n:
            print(f"\nmodel.current_chat_session[n]['content']: {model.current_chat_session[n]['content']}\n")
            reply_content = "**" + seleccion_modelo + "** : " + model.current_chat_session[n]['content']
            print(f"\nreply_content: {reply_content}")
            guardar_chat_history(chat_history, user_info, config.CHAT_HISTORY_PATH, chat_id, reply_content, seleccion_modelo)
            print("\nguardado con éxito. ")
            chat_id = 593052206
            print("\nchat_id: ",chat_id)
            print("")
            await send(reply_content, chat_id)
        else:
            print("No hay mensajes en la sesión de chat actual.")
        i = i + 1
    except Exception as e:
        logging.error(f"Error al procesar la respuesta con el modelo IA: {e}")
        await send("Lo siento, ocurrió un error al procesar tu solicitud.", chat_id)

def cargar_chat_history(file_path):
    logging.info(f"Cargando historial del chat desde {file_path}")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            chat_histories = data.get("chat_histories", {})
            user_info = data.get("user_info", {})

            ultimo_rol = None
            chat_usuario_especifico = chat_histories.get("593052206", [])

            # Ordenar los mensajes por unixtime para asegurar que el más reciente es primero
            chat_usuario_especifico.sort(key=lambda x: x['unixtime'], reverse=True)

            if chat_usuario_especifico:
                primer_mensaje = chat_usuario_especifico[0]
                ultimo_rol = primer_mensaje.get("role")
                logging.info(f"Último mensaje del usuario 593052206 con rol {ultimo_rol}")

            return chat_histories, user_info, ultimo_rol

    except FileNotFoundError:
        logging.error(f"No se encontró el archivo: {file_path}. Por favor verifica la ruta.")
        return {}, {}, None
    except json.JSONDecodeError:
        logging.error(f"Error al leer el archivo: {file_path}. Formato de archivo inválido.")
        return {}, {}, None
    except Exception as e:
        logging.error(f"Error inesperado al leer el archivo {file_path}: {e}")
        return {}, {}, None

    except FileNotFoundError:
        print(f"No se encontró el archivo: {file_path}. Por favor verifica la ruta.")
        return {}, {}, None
    except json.JSONDecodeError:
        print(f"Error al leer el archivo: {file_path}. Formato de archivo inválido.")
        return {}, {}, None
