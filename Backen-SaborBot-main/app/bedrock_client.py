

# app/bedrock_client.py
import os
import json
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime
import base64 # Necesario para decodificar la imagen
from dotenv import load_dotenv
load_dotenv() 

# --- CONFIGURACIÓN DE AWS ---
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# IDs de Modelos
LITE_TEXT_MODEL_ID = "us.amazon.nova-lite-v1:0"
TITAN_IMAGE_MODEL_ID = "amazon.titan-image-generator-v1" # ID para el modelo de imagen
MY_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
MY_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# Configuración base de Boto3
my_config = Config(
    connect_timeout=10, 
    read_timeout=120, 
    retries={'max_attempts': 1}
)

# La función invoke_bedrock (para texto) se mantiene igual
def invoke_bedrock(prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
    """
    Invoca Amazon Bedrock (Nova Lite) con un contexto de chatbot de cocina.
    """
    try:
        client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
            aws_access_key_id=MY_ACCESS_KEY,
            aws_secret_access_key=MY_SECRET_KEY,
            config=my_config # Usando la configuración definida globalmente
        )
    except ClientError as e:
        print(f"Error al inicializar el cliente de Bedrock: {e}")
        return "Error de conexión con AWS Bedrock. Verifica credenciales y región."
        
    system_list = [
        {"text": "Eres un asistente de cocina amable y experto. Responde a todas las preguntas del usuario relacionadas con recetas, ingredientes, técnicas de cocina y consejos culinarios. Responde de forma concisa y útil."}
    ]
    message_list = [{"role": "user", "content": [{"text": prompt}]}]
    inf_params = {"maxTokens": max_tokens, "topP": 0.9, "topK": 20, "temperature": temperature}

    request_body = {
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params,
    }

    try:
        response = client.invoke_model_with_response_stream(
            modelId=LITE_TEXT_MODEL_ID, # Usar el ID del modelo de texto
            body=json.dumps(request_body)
        )
        stream = response.get("body")
        full_response_text = ""
        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    content_block_delta = chunk_json.get("contentBlockDelta")
                    if content_block_delta:
                        text_chunk = content_block_delta.get("delta").get("text")
                        if text_chunk:
                            full_response_text += text_chunk
            return full_response_text.strip()
        else:
            return "No se recibió respuesta del modelo de texto."
            
    except ClientError as e:
        error_message = f"Error al invocar el modelo de Bedrock (texto): {e}"
        print(error_message)
        return error_message

# --- NUEVA FUNCIÓN PARA GENERAR IMÁGENES ---
def generate_image_with_titan(
    prompt: str, 
    seed: int = 0, 
    cfg_scale: float = 7.0, 
    quality: str = "standard", 
    width: int = 1024, 
    height: int = 1024,
    output_image_path: str = None # Path para guardar la imagen # type: ignore
) -> str:
    """
    Genera una imagen usando Amazon Titan Image Generator G1.

    :param prompt: El prompt de texto para la imagen.
    :param seed: Semilla para la generación (0 para aleatorio, o un número fijo para reproducibilidad).
    :param cfg_scale: Escala de la guía del clasificador (controla la adherencia al prompt).
    :param quality: Calidad de la imagen ("standard" o "premium").
    :param width: Ancho de la imagen.
    :param height: Alto de la imagen.
    :param output_image_path: Ruta del archivo donde guardar la imagen (e.g., "imagen_generada.png").
                               Si es None, devuelve la imagen en Base64.
    :return: Si output_image_path es None, devuelve la imagen codificada en Base64.
             Si se proporciona output_image_path, devuelve la ruta del archivo.
             En caso de error, devuelve un mensaje de error.
    """
    try:
        client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=MY_ACCESS_KEY,
            aws_secret_access_key=MY_SECRET_KEY,
            region_name=AWS_REGION,
            config=my_config # Usando la configuración definida globalmente
        )
    except ClientError as e:
        print(f"Error al inicializar el cliente de Bedrock para imagen: {e}")
        return "Error de conexión con AWS Bedrock para imagen. Verifica credenciales y región."

    # Estructura del body para Titan Image Generator G1
    request_body = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1, # Solo generamos una imagen por solicitud para este ejemplo
            "quality": quality,
            "cfgScale": cfg_scale,
            "seed": seed,
            "width": width,
            "height": height
        }
    }

    try:
        response = client.invoke_model(
            modelId=TITAN_IMAGE_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )

        response_body = json.loads(response.get("body").read())
        
        # Las imágenes vienen en una lista, incluso si solo pedimos una
        base64_image_data = response_body["images"][0] 
        
        if output_image_path:
            # Decodifica y guarda la imagen si se proporciona una ruta
            with open(output_image_path, "wb") as f:
                f.write(base64.b64decode(base64_image_data))
            return output_image_path
        else:
            # Si no se da una ruta, devuelve los datos Base64
            return base64_image_data

    except ClientError as e:
        error_message = f"Error al invocar el modelo de Bedrock (imagen): {e}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error inesperado al generar la imagen: {e}"
        print(error_message)
        return error_message