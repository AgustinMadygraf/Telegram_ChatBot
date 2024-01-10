# config.py
import os
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

# Configuración general
CHAT_HISTORY_PATH = "data/context_window_telegram.json"

# Configuraciones específicas del modelo de IA
MODELOS_POR_RAM = {
    "1": "1 GB",
    "2": "4 GB",
    "3": "8 GB",
    "4": "16 GB"
}

MODELOS_DISPONIBLES = {
        "1 GB": ["all-MiniLM-L6-v2-f16.gguf"],
        "4 GB": ["replit-code-v1_5-3b-q4_0.gguf"],
        "8 GB": ["mistral-7b-openorca.Q4_0.gguf", "mistral-7b-instruct-v0.1.Q4_0.gguf",
                "gpt4all-falcon-q4_0.gguf", "gpt4all-13b-snoozy-q4_0.gguf", "orca-2-7b.Q4_0.gguf",
                "mpt-7b-chat-merges-q4_0.gguf"],
        "16 GB": ["orca-2-13b.Q4_0.gguf", "wizardlm-13b-v1.2.Q4_0.gguf", "nous-hermes-llama2-13b.Q4_0.gguf","mixtral-8x7b-v0.1.Q4_K_M.gguf"]
    }

# Variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MODEL_PATH = os.getenv('MODEL_PATH', 'E:\Model _Explorer') 
