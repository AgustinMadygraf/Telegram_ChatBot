# bot/processing.py
import asyncio
import json
from bot.utils import limpiar_pantalla, guardar_chat_history  
from bot.bot import send, send_a

chat_history_path = "context_window_telegram.json"

async def procesar_respuesta(chat_history, user_id, model, i, user_info, seleccion_modelo,chat_id):
    user_id_str = str(user_id)
    user_messages = chat_history.get(user_id_str, [])
    
    # Seleccionar el último mensaje si hay mensajes disponibles
    if user_messages:
        prompt = user_messages[0]['content']
        #prompt = user_messages
    else:
        prompt = "Continúa"

    print(f"last prompt: {prompt}")
    print("\nConsultado a la IA local, CPU está trabajando. Espere por favor. ")
    model.generate(prompt, temp=0)
    print("Gracias por esperar")

    # Obtener el índice del último mensaje en la sesión de chat
    n = len(model.current_chat_session) - 1

    # Asegurarte de que el índice n sea válido
    if n >= 0 and len(model.current_chat_session) > n:
        print(f"\nmodel.current_chat_session[n]['content']: {model.current_chat_session[n]['content']}\n")
        reply_content = "**" + seleccion_modelo + "** : " + model.current_chat_session[n]['content']
        guardar_chat_history(chat_history, user_info, chat_history_path, chat_id, reply_content,seleccion_modelo)
        print("guardado con éxito. ")
        #print("espere 5 sgundos, verifique el archivo JSON.")
        #time.sleep(5)
        #input("presione enter para continuar")

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

            # Identificar el último rol en la conversación del usuario 593052206
            ultimo_rol = None
            chat_usuario_especifico = chat_histories.get("593052206", [])
            if chat_usuario_especifico:
                primer_mensaje = chat_usuario_especifico[0]  # Obtener el último mensaje
                ultimo_rol = primer_mensaje.get("role")

            return chat_histories, user_info, ultimo_rol

    except FileNotFoundError:
        print(f"No se encontró el archivo: {file_path}. Por favor verifica la ruta.")
        return {}, {}, None
    except json.JSONDecodeError:
        print(f"Error al leer el archivo: {file_path}. Formato de archivo inválido.")
        return {}, {}, None

