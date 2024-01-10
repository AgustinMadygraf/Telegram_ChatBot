# Chatbot de Telegram para GPT-4All

Este proyecto es un chatbot de Telegram que utiliza modelos avanzados de inteligencia artificial para interactuar con los usuarios. Está construido en Python y puede ser personalizado para diferentes usos.

## Características

- Interacción en tiempo real con usuarios a través de Telegram.
- Utiliza modelos de IA como GPT-4All para generar respuestas.
- Configurable para diferentes capacidades de memoria RAM.

## Configuración

### Prerrequisitos

- Python 3.12 o superior.
- Una cuenta de bot de Telegram y su token correspondiente.

### Instalación

Clona este repositorio usando:

```bash
git clone [URL del repositorio]
```

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

```env
TELEGRAM_TOKEN=tu_token_de_telegram_aquí
```

> ⚠️ **Nota de Seguridad**: Nunca subas tu archivo `.env` a repositorios públicos, ya que contiene información sensible.

### Ejecución

Para iniciar el chatbot, ejecuta:

```bash
python main.py
```

## Documentación Adicional

- `config.py`: Gestiona la configuración del chatbot.
- `main.py`: Archivo principal que inicia el bot.
- `TelegramChatArchiver.py`: Archiva el historial de chats de Telegram.

## Contribuir

Si deseas contribuir al proyecto, considera realizar un 'fork' del repositorio y enviar tus 'pull requests'. Para más detalles, consulta `CONTRIBUTING.md`.

## Licencia

Este proyecto está licenciado bajo [Licencia MIT](LICENSE).
