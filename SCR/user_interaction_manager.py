import time
from gpt4all import GPT4All
import logging

def obtener_opciones_usuario(config):
    """
    Obtiene las opciones del usuario para la configuración del chatbot.

    Esta función interactúa con el usuario para determinar el modo de respuesta del bot y la capacidad de memoria RAM deseada. 
    Asegura que las opciones seleccionadas sean válidas según la configuración proporcionada.

    Parámetros:
    config (dict): Un diccionario que contiene la configuración del bot, incluyendo opciones de RAM.

    Retorna:
    tuple: Un tuple que contiene un booleano para indicar si se usa respuesta rápida y la memoria RAM seleccionada.
    """
    modo_respuesta = obtener_modo_respuesta()
    ram_seleccionada = seleccionar_memoria_ram(config)
    return modo_respuesta, ram_seleccionada

def obtener_modo_respuesta():
    """
    Solicita al usuario elegir el modo de respuesta del bot.

    Permite al usuario elegir entre una respuesta rápida o una respuesta detallada. Valida la entrada del usuario y 
    usa el modo de respuesta rápida por defecto en caso de una selección inválida.

    Retorna:
    bool: Verdadero para respuesta rápida, Falso para respuesta detallada.
    """
    print("Elige el modo de respuesta del bot:")
    print("1. Respuesta rápida (ventana de contexto limitada a la última pregunta)")
    print("2. Respuesta detallada (ventana de contexto ampliada a todo el historial)")
    modo_respuesta = input("Selecciona una opción (1 o 2): ")
    return modo_respuesta == "1" or modo_respuesta not in ["1", "2"]

def seleccionar_memoria_ram(config):
    """
    Solicita al usuario seleccionar la capacidad de memoria RAM.

    Permite al usuario elegir entre diferentes opciones de RAM disponibles en la configuración. 
    Valida la entrada del usuario y selecciona una opción predeterminada en caso de una selección inválida.

    Parámetros:
    config (dict): Un diccionario que contiene las opciones de RAM disponibles.

    Retorna:
    str: La capacidad de memoria RAM seleccionada.
    """
    print("Selecciona la capacidad de tu memoria RAM: 1 (1 GB), 2 (4 GB), 3 (8 GB), 4 (16 GB): \n")
    opcion_ram = input("Elige una opción: ")
    return config['ram_options'].get(opcion_ram, "2")

def seleccionar_modelo(config, ram_seleccionada):
    """
    Permite al usuario seleccionar un modelo de IA basado en la capacidad de RAM seleccionada.

    Presenta al usuario una lista de modelos disponibles según la capacidad de RAM y permite seleccionar uno. 
    Asegura que la selección sea válida y maneja las entradas inválidas adecuadamente.

    Parámetros:
    config (dict): Un diccionario que contiene la configuración del bot, incluyendo los modelos disponibles.
    ram_seleccionada (str): La capacidad de RAM seleccionada por el usuario.

    Retorna:
    str: El modelo seleccionado o None si no se selecciona un modelo válido.
    """
    modelos_a_mostrar = config['models_available'].get(ram_seleccionada, [])
    mostrar_opciones_modelo(modelos_a_mostrar)
    return obtener_seleccion_modelo(modelos_a_mostrar)

def mostrar_opciones_modelo(modelos):
    """
    Muestra los modelos de IA disponibles al usuario.

    Parámetros:
    modelos (list): Una lista de modelos de IA disponibles.
    """
    if modelos:
        logging.info("Modelos disponibles:")
        for idx, modelo in enumerate(modelos, 1):
            logging.info(f"{idx}. {modelo}")

def obtener_seleccion_modelo(modelos):
    """
    Obtiene la selección del usuario de entre los modelos disponibles.

    Parámetros:
    modelos (list): Una lista de modelos de IA disponibles.

    Retorna:
    str: El modelo seleccionado o None si la selección es inválida.
    """
    while True:
        try:
            seleccion_numero = int(input("\nSelecciona el número del modelo: "))
            if 1 <= seleccion_numero <= len(modelos):
                return modelos[seleccion_numero - 1]
            else:
                print("Selección fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor ingresa un número.")

def inicializar_modelo_ia(config, seleccion_modelo):
    """
    Inicializa el modelo de inteligencia artificial seleccionado.

    Esta función se encarga de cargar e inicializar el modelo de IA basado en la selección del usuario y la configuración proporcionada. 
    Mide el tiempo que toma cargar el modelo y registra esta información. Maneja las excepciones en caso de errores durante la inicialización.

    Parámetros:
    config (dict): Un diccionario que contiene la configuración del bot, incluyendo la ruta del modelo.
    seleccion_modelo (str): El nombre del modelo de IA seleccionado por el usuario.

    Retorna:
    GPT4All: Una instancia del modelo de IA inicializado, o None si la inicialización falla.
    """
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




