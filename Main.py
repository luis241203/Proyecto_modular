import time
from LoRa import LoRa
from LoRa import ModemConfig

# Configuración del LoRa
lora = LoRa(verbose=True)
lora.set_mode(LoRa.MODE.SLEEP)  # Establecer en modo SLEEP al inicio
lora.set_mode(LoRa.MODE.TX)  # Establecer en modo de transmisión

while True:
    message = "Hello LoRa!"
    print("Enviando:", message)
    lora.write_payload([ord(c) for c in message])  # Convertir el mensaje a bytes
    lora.set_mode(LoRa.MODE.TX)  # Enviar el mensaje
    time.sleep(2)  # Espera antes de enviar el siguiente mensaje
