import time
import RPi.GPIO as GPIO
from pyLoRa import LoRa

# Configuración de pines
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Inicializa el objeto LoRa
lora = LoRa(cs_pin=8, reset_pin=17, irq_pin=25)  # Ajusta los pines a tu configuración
lora.set_mode(LoRa.MODE_TX)  # Modo de transmisión

# Configura parámetros
lora.set_frequency(868.0)  # Ajusta la frecuencia en MHz, dependiendo de tu región
lora.set_spreading_factor(7)  # Ajusta el factor de expansión
lora.set_bandwidth(125)  # Ancho de banda en kHz

# Función para enviar un mensaje
def send_lora_message(message):
    lora.begin_packet()
    lora.write_bytes(message.encode())  # Envía el mensaje como bytes
    lora.end_packet()
    print(f"Mensaje enviado: {message}")

# Enviar un mensaje cada 2 segundos
while True:
    send_lora_message("¡Hola desde LoRa!")
    time.sleep(2)
