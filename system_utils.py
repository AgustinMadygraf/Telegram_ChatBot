import json
from dotenv import load_dotenv



load_dotenv()  

def load_system_template():
    try:
        with open("setup.json", "r") as file:
            templates = json.load(file)
            for idx, template in enumerate(templates, start=1):
                print(f"{idx}. {template['modo']}")
            seleccion = input("Elige el modo (por número): ")
            try:
                seleccion_index = int(seleccion) - 1
                if 0 <= seleccion_index < len(templates):
                    return templates[seleccion_index]['system_template']
            except ValueError:
                pass
            print("Selección inválida. Usando configuración por defecto.")
            return templates[0]['system_template']  # Configuración por defecto en caso de selección inválida
    except FileNotFoundError:
        print("Archivo 'setup.json' no encontrado. Usando configuración por defecto.")
        return '### System:\nConfiguración por defecto.'

SYSTEM_TEMPLATE = load_system_template()