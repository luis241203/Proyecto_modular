import spidev
import time
import RPi.GPIO as GPIO

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
CS_PIN = 8
DIO0_PIN = 17
RESET_PIN = 22  # Pin opcional de reset

# Configuración SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 1000000  # 1MHz es suficiente para LoRa
spi.mode = 0b00

# Registros SX1278
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_PA_CONFIG = 0x09
REG_LNA = 0x0C
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_TX_BASE_ADDR = 0x0E
REG_FIFO_RX_BASE_ADDR = 0x0F
REG_IRQ_FLAGS = 0x12
REG_RX_NB_BYTES = 0x13
REG_PKT_SNR_VALUE = 0x19
REG_PKT_RSSI_VALUE = 0x1A
REG_MODEM_CONFIG1 = 0x1D
REG_MODEM_CONFIG2 = 0x1E
REG_SYMB_TIMEOUT_LSB = 0x1F
REG_PREAMBLE_MSB = 0x20
REG_PREAMBLE_LSB = 0x21
REG_PAYLOAD_LENGTH = 0x22
REG_DIO_MAPPING1 = 0x40
REG_VERSION = 0x42

def cs_enable():
    GPIO.output(CS_PIN, GPIO.LOW)

def cs_disable():
    GPIO.output(CS_PIN, GPIO.HIGH)

def read_register(register):
    cs_enable()
    response = spi.xfer2([register & 0x7F, 0x00])
    cs_disable()
    return response[1]

def write_register(register, value):
    cs_enable()
    spi.xfer2([register | 0x80, value])
    cs_disable()

def init_lora():
    # Configuración básica del módulo LoRa
    write_register(REG_OP_MODE, 0x80)  # Modo LoRa + Sleep
    time.sleep(0.1)
    
    # Verificar versión del chip
    version = read_register(REG_VERSION)
    if version != 0x12:
        print(f"Error: Versión del chip no reconocida: {version}")
        return False
    
    # Configurar frecuencia (915 MHz)
    write_register(REG_FRF_MSB, 0xE4)
    write_register(REG_FRF_MID, 0xC0)
    write_register(REG_FRF_LSB, 0x00)
    
    # Configuración del modem
    write_register(REG_MODEM_CONFIG1, 0x72)  # BW=125kHz, CR=4/5, Implicit header
    write_register(REG_MODEM_CONFIG2, 0x74)  # SF=7, CRC enabled
    
    # Configuración de potencia
    write_register(REG_PA_CONFIG, 0x8F)  # PA_BOOST, 20dBm
    
    # Configurar FIFO
    write_register(REG_FIFO_TX_BASE_ADDR, 0x80)
    write_register(REG_FIFO_RX_BASE_ADDR, 0x00)
    
    # Cambiar a modo standby
    write_register(REG_OP_MODE, 0x81)
    time.sleep(0.1)
    
    print("LoRa inicializado correctamente")
    return True

def send_data(data):
    # Cambiar a modo standby
    write_register(REG_OP_MODE, 0x81)
    
    # Configurar puntero FIFO
    write_register(REG_FIFO_ADDR_PTR, 0x80)
    
    # Escribir datos en FIFO
    for byte in data:
        write_register(REG_FIFO, byte)
    
    # Configurar longitud del payload
    write_register(REG_PAYLOAD_LENGTH, len(data))
    
    # Cambiar a modo TX
    write_register(REG_OP_MODE, 0x83)
    
    # Esperar hasta que se complete la transmisión
    while (read_register(REG_IRQ_FLAGS) & 0x08) == 0:
        time.sleep(0.1)
    
    # Limpiar flag de TX
    write_register(REG_IRQ_FLAGS, 0x08)
    
    # Volver a modo standby
    write_register(REG_OP_MODE, 0x81)
    
    print(f"Datos enviados: {data}")

def receive_data():
    # Cambiar a modo RX continuo
    write_register(REG_OP_MODE, 0x85)
    
    # Esperar hasta que llegue un paquete
    while (read_register(REG_IRQ_FLAGS) & 0x40) == 0:
        time.sleep(0.1)
    
    # Leer datos recibidos
    rx_nb_bytes = read_register(REG_RX_NB_BYTES)
    write_register(REG_FIFO_ADDR_PTR, read_register(REG_FIFO_RX_CURRENT_ADDR))
    
    data = []
    for i in range(rx_nb_bytes):
        data.append(read_register(REG_FIFO))
    
    # Limpiar flag de RX
    write_register(REG_IRQ_FLAGS, 0x40)
    
    # Leer RSSI y SNR
    rssi = read_register(REG_PKT_RSSI_VALUE)
    snr = read_register(REG_PKT_SNR_VALUE)
    
    print(f"Datos recibidos: {data}, RSSI: {rssi}, SNR: {snr}")
    return data

if __name__ == "__main__":
    try:
        # Inicializar GPIO
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.setup(DIO0_PIN, GPIO.IN)
        GPIO.setup(RESET_PIN, GPIO.OUT)
        
        # Resetear módulo
        GPIO.output(RESET_PIN, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(RESET_PIN, GPIO.HIGH)
        time.sleep(0.1)
        
        if init_lora():
            counter = 0
            while True:
                # Enviar datos
                send_data([0x01, 0x02, 0x03, counter % 256])
                
                # Recibir datos
                receive_data()
                
                counter += 1
                time.sleep(5)
                
    except KeyboardInterrupt:
        print("Programa terminado")
    finally:
        spi.close()
        GPIO.cleanup()