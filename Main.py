import spidev
import time
import RPi.GPIO as GPIO

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
RESET_PIN = 22  # Pin opcional de reset

# Configuración SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 500000
spi.mode = 0b00

# Registros SX1278 (solo los necesarios para TX)
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_PA_CONFIG = 0x09
REG_MODEM_CONFIG1 = 0x1D
REG_MODEM_CONFIG2 = 0x1E
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_TX_BASE_ADDR = 0x0E
REG_FIFO = 0x00
REG_PAYLOAD_LENGTH = 0x22
REG_IRQ_FLAGS = 0x12
REG_VERSION = 0x42

def read_register(register):
    return spi.xfer2([register & 0x7F, 0x00])[1]

def write_register(register, value):
    spi.xfer2([register | 0x80, value])

def init_lora():
    # Resetear módulo
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.01)
    
    # Modo LoRa + Sleep
    write_register(REG_OP_MODE, 0x80)
    time.sleep(0.1)
    
    # Verificar versión del chip
    if read_register(REG_VERSION) != 0x12:
        print("Error: Chip no reconocido")
        return False
    
    # Frecuencia 433 MHz
    write_register(REG_FRF_MSB, 0x6C)
    write_register(REG_FRF_MID, 0x40)
    write_register(REG_FRF_LSB, 0x00)
    
    # Configuración modem
    write_register(REG_MODEM_CONFIG1, 0x72)  # BW=125kHz, CR=4/5
    write_register(REG_MODEM_CONFIG2, 0x74)  # SF=7
    
    # Configurar potencia (20dBm)
    write_register(REG_PA_CONFIG, 0x8F)
    
    # Configurar FIFO TX
    write_register(REG_FIFO_TX_BASE_ADDR, 0x80)
    
    # Modo standby
    write_register(REG_OP_MODE, 0x81)
    time.sleep(0.1)
    
    print("LoRa listo para transmitir")
    return True

def send_data(data):
    # Poner en modo standby
    write_register(REG_OP_MODE, 0x81)
    time.sleep(0.05)
    
    # Configurar puntero FIFO
    write_register(REG_FIFO_ADDR_PTR, 0x80)
    
    # Escribir datos
    for byte in data:
        write_register(REG_FIFO, byte)
    
    # Longitud del payload
    write_register(REG_PAYLOAD_LENGTH, len(data))
    
    # Iniciar transmisión
    write_register(REG_OP_MODE, 0x83)
    
    # Esperar fin de transmisión (máximo 5 segundos)
    timeout = time.time() + 10
    while (read_register(REG_IRQ_FLAGS) & 0x08) == 0:
        if time.time() > timeout:
            print("Error: Timeout en transmisión")
            break
        time.sleep(0.1)
    
    # Limpiar flag
    write_register(REG_IRQ_FLAGS, 0x08)
    
    # Volver a standby
    write_register(REG_OP_MODE, 0x81)
    
    print(f"Datos enviados: {data}")

if __name__ == "__main__":
    try:
        if init_lora():
            counter = 0
            while True:
                # Enviar datos de prueba (puedes modificar esto)
                payload = [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 33, 33, counter%250]
                send_data(payload)
                
                counter += 1
                time.sleep(10)  # Espera 5 segundos entre transmisiones
                
    except KeyboardInterrupt:
        print("Transmisión detenida")
    finally:
        spi.close()
        GPIO.cleanup()