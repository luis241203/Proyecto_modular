import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD

# Inicializa la Raspberry Pi y el LoRa
BOARD.setup()

# Clase LoRa para manejar el envío de mensajes
class LoRaRaspberry(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRaspberry, self).__init__(verbose)

    def on_rx_done(self):
        print("Mensaje recibido:", self.read_payload(nocheck=True))
        self.clear_irq_flags(RxDone=1)

# Configuración de LoRa
lora = LoRaRaspberry(verbose=True)
lora.set_mode(LoRa.MODE.SLEEP)  # Modo de reposo inicial
lora.set_mode(LoRa.MODE.TX)  # Modo de transmisión

while True:
    message = "Hello LoRa!"
    print("Enviando:", message)
    lora.write_payload([ord(c) for c in message])  # Convierte el mensaje a bytes
    lora.set_mode(LoRa.MODE.TX)  # Enviar el mensaje
    time.sleep(2)  # Esperar antes de enviar el siguiente mensaje
