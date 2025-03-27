import time
import RPi.GPIO as GPIO
from lora import LoRa

# Configura los pines para SPI
GPIO.setmode(GPIO.BCM)
lora = LoRa(spi_bus=0, spi_device=0, gpio_cs=8, gpio_rst=25, gpio_dio0=17)

# Configura el LoRa en modo transmisión
lora.set_mode(LoRa.MODE_TX)

# El mensaje que se va a enviar
message = "Hello, LoRa! Esperando respuesta..."

# Enviar el mensaje
print("Enviando:", message)
lora.send(message)

# Ahora el transmisor espera la respuesta
lora.set_mode(LoRa.MODE_RX)
print("Esperando respuesta...")
while True:
    if lora.received():
        response = lora.receive()
        print("Respuesta recibida:", response)
        break  # Sale del loop cuando recibe una respuesta
    time.sleep(1)  # Espera un segundo antes de volver a comprobar
