import asyncio
import json
import logging
from bot.utils import limpiar_pantalla, guardar_chat_history
from bot.bot import send, send_a
import config
import time
import os
from config_manager import ConfigManager

config_manager = ConfigManager()

async def procesar_respuesta(chat_history, user_id, model, i, user_info, seleccion_modelo, chat_id, respuesta_rapida):
    user_id_str = str(user_id)
    user_messages = chat_history.get(user_id_str, [])
    logging.info(f"Respuesta rápida: {respuesta_rapida}")

    try:
        if user_messages:
            prompt = user_messages[0]['content'] if respuesta_rapida else user_messages
        else:
            prompt = "Continúa"

        logging.info(f"Último prompt: {prompt}")
        logging.info(f"Consultando a la IA local, CPU trabajando...")

        inicio_generacion = time.time()
        tokens = []
        logging.info(f"Invocando a **{seleccion_modelo}**")
        print(f"\nInvocando a **{seleccion_modelo}**\n ")
        for token in model.generate(prompt, temp=0, streaming=True):
            tokens.append(token)
            print(token, end='', flush=True)
        fin_generacion = time.time()
        tiempo_generacion = fin_generacion - inicio_generacion
        logging.info(f"Tiempo de generación de respuesta: {tiempo_generacion:.2f} segundos")

        n = len(model.current_chat_session) - 1
        if n >= 0 and len(model.current_chat_session) > n:
            reply_content = "**" + seleccion_modelo + "** : " + model.current_chat_session[n]['content']
            logging.info(f"Contenido de respuesta: {reply_content}")
            guardar_chat_history(chat_history, user_info, config_manager.config_data['chat_history_path'], chat_id, reply_content, seleccion_modelo)
            logging.info("Guardado con éxito en el historial del chat.")
            await send(reply_content, chat_id)
        else:
            logging.info("No hay mensajes en la sesión de chat actual.")
        i += 1
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
