import time
from RFM95 import RFM95

# Configuración del LoRa
lora = RFM95(spi_bus=0, spi_device=0, gpio_cs=8, gpio_rst=25, gpio_dio0=17)
lora.set_frequency(915.0)  # Establece la frecuencia (por ejemplo, 915 MHz)

# Enviar mensaje
while True:
    message = "Hello LoRa!"
    print("Enviando:", message)
    lora.send(message.encode())  # Envía el mensaje codificado en bytes
    time.sleep(2)  # Espera antes de enviar el siguiente mensaje
