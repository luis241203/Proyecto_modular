import spidev
import time

# Configuración de la conexión SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Usar el bus SPI 0 y el chip select 0
spi.max_speed_hz = 5000000  # Ajustar la velocidad de transmisión (5 MHz en este caso)
spi.mode = 0b00  # Modo SPI (Polarity = 0, Phase = 0)

# Pin Chip Select (CS)
CS_PIN = 8  # GPIO pin para CS (Chip Select)
DIO0_PIN = 17  # GPIO pin para DIO0 (interrupciones)

# Definir algunos registros importantes del SX1278
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_DIO_MAPPING1 = 0x40
REG_IRQ_FLAGS = 0x12
REG_PKT_SNR_VALUE = 0x19
REG_MODEM_CONFIG = 0x1D

# Comando para leer un registro
def read_register(register):
    response = spi.xfer2([register & 0x7F, 0x00])  # Leer valor del registro
    return response[1]

# Comando para escribir en un registro
def write_register(register, value):
    spi.xfer2([register | 0x80, value])

# Inicialización del LoRa
def init_lora():
    # Configurar el modo de operación (modo LoRa, transmisor o receptor)
    write_register(REG_OP_MODE, 0x80)  # Modo LoRa, modo de recepción

    # Configuración de frecuencia (Ejemplo: 915 MHz, que corresponde a 0xD9, 0x06, 0x00)
    write_register(REG_FRF_MSB, 0xD9)
    write_register(REG_FRF_MID, 0x06)
    write_register(REG_FRF_LSB, 0x00)

    # Configurar otros registros según sea necesario (como la potencia de transmisión)
    write_register(REG_MODEM_CONFIG, 0x72)  # Ejemplo de configuración de modem (ajustar según necesidades)

    # Configuración de interrupciones (DIO0)
    write_register(REG_DIO_MAPPING1, 0x00)  # Mapear DIO0 a IRQ

    print("LoRa inicializado")

# Enviar datos a través de LoRa
def send_data(data):
    # Asegurarse de que el FIFO esté vacío antes de escribir datos
    write_register(REG_OP_MODE, 0x81)  # Modo LoRa, modo de transmisión

    # Colocar datos en el FIFO para enviarlos
    for byte in data:
        write_register(REG_FIFO, byte)

    print(f"Datos enviados: {data}")

# Leer datos recibidos
def receive_data():
    # Cambiar a modo recepción
    write_register(REG_OP_MODE, 0x85)  # Modo LoRa, modo de recepción

    # Leer el valor de la señal recibida
    snr = read_register(REG_PKT_SNR_VALUE)  # Leer la relación señal/ruido

    print(f"Señal recibida con SNR: {snr}")
    # Aquí puedes leer más registros, como el FIFO, para obtener los datos recibidos.

# Main loop
if __name__ == "__main__":
    init_lora()  # Inicializar LoRa

    while True:
        send_data([0x01, 0x02, 0x03])  # Enviar datos de ejemplo
        time.sleep(2)

        receive_data()  # Leer datos si hay algún mensaje recibido
        time.sleep(1)
