import time
from gpt4all import GPT4All
import logging

def obtener_opciones_usuario(config):
    print("Elige el modo de respuesta del bot:")
    print("1. Respuesta rápida (ventana de contexto limitada a la última pregunta)")
    print("2. Respuesta detallada (ventana de contexto ampliada a todo el historial)")
    modo_respuesta = input("Selecciona una opción (1 o 2): ")
    if modo_respuesta not in ["1", "2"]:
        print("Selección inválida. Usando modo de respuesta rápida por defecto.")
        modo_respuesta = "1"

    respuesta_rapida = modo_respuesta == "1"

    opcion_ram = input("Selecciona la capacidad de tu memoria RAM: 1 (1 GB), 2 (4 GB), 3 (8 GB), 4 (16 GB): \n")
    if opcion_ram not in config['ram_options']:
        opcion_ram = "2"
    ram_seleccionada = config['ram_options'].get(opcion_ram)

    return respuesta_rapida, ram_seleccionada

def inicializar_modelo_ia(config, seleccion_modelo):
    try:
        inicio_carga = time.time()  # Iniciar el contador de tiempo
        print("Inicializando modelo de IA...")
        model = GPT4All(seleccion_modelo, config['model_path'])
        fin_carga = time.time()  # Finalizar el contador de tiempo
        tiempo_carga = fin_carga - inicio_carga  # Calcular la duración de la carga
        logging.info(f"Modelo inicializado con éxito en {tiempo_carga:.2f} segundos.")
        return model
    except ValueError as e:
        logging.error(f"Error al inicializar el modelo: {e}")
        return None
    
def seleccionar_modelo(config, ram_seleccionada):
    modelos_a_mostrar = config['models_available'].get(ram_seleccionada, [])
    if modelos_a_mostrar:
        logging.info(f"Modelos disponibles para RAM de {ram_seleccionada} seleccionada:")
        for idx, modelo in enumerate(modelos_a_mostrar, 1):
            logging.info(f"{idx}. {modelo}")
        while True:
            try:
                seleccion_numero = int(input("\nSelecciona el número del modelo: "))
                if 1 <= seleccion_numero <= len(modelos_a_mostrar):
                    return modelos_a_mostrar[seleccion_numero - 1]
                else:
                    print("Selección fuera de rango. Por favor intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número.")
    return None


