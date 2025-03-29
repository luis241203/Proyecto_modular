import spidev
import time
import RPi.GPIO as GPIO

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
DIO0_PIN = 17  # Pin para interrupción RxDone
RESET_PIN = 22  # Pin de reset

# Configuración SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 500000
spi.mode = 0b00

# Registros SX1278
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_FIFO = 0x00
REG_FIFO_RX_CURRENT_ADDR = 0x10
REG_IRQ_FLAGS = 0x12
REG_RX_NB_BYTES = 0x13
REG_MODEM_CONFIG1 = 0x1D
REG_MODEM_CONFIG2 = 0x1E
REG_PKT_SNR_VALUE = 0x19
REG_PKT_RSSI_VALUE = 0x1A
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_RX_BASE_ADDR = 0x0F
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
    
    # Frecuencia 433 MHz (Registros FRF)
    write_register(REG_FRF_MSB, 0x6C)  # 433 MHz: 0x6C4000
    write_register(REG_FRF_MID, 0x40)
    write_register(REG_FRF_LSB, 0x00)
    
    # Configuración modem
    write_register(REG_MODEM_CONFIG1, 0x72)  # BW=125kHz, CR=4/5, Explicit Header
    write_register(REG_MODEM_CONFIG2, 0x74)  # SF=7, CRC enabled
    
    # Config FIFO RX
    write_register(REG_FIFO_RX_BASE_ADDR, 0x00)
    write_register(REG_FIFO_ADDR_PTR, 0x00)
    
    # Configurar LNA (opcional para mejor recepción)
    write_register(0x0C, 0x23)  # REG_LNA: LNA máxima ganancia
    
    # Modo RX continuo
    write_register(REG_OP_MODE, 0x85)
    time.sleep(0.1)
    
    print("LoRa listo para recibir en 433 MHz")
    return True

def receive_data():
    # Verificar si hay datos recibidos
    irq_flags = read_register(REG_IRQ_FLAGS)
    if irq_flags & 0x40:  # RxDone
        #write_register(REG_IRQ_FLAGS, irq_flags)
        # Obtener longitud del paquete
        length = read_register(REG_RX_NB_BYTES)
        
        write_register(REG_OP_MODE, 0x81)
        # Leer datos del FIFO
        current_addr = read_register(REG_FIFO_RX_CURRENT_ADDR)
        write_register(REG_FIFO_ADDR_PTR, current_addr)

        data = []
        for _ in range(length):
            data.append(read_register(REG_FIFO))
        
        # Leer RSSI (ajuste para 433 MHz)
        rssi = read_register(REG_PKT_RSSI_VALUE) - 164  # Ajuste específico para 433 MHz
        snr = read_register(REG_PKT_SNR_VALUE) * 0.25
                    
        print(f"Datos recibidos: {data} | RSSI: {rssi} dBm | SNR: {snr} dB")
        #write_register(REG_FIFO_RX_BASE_ADDR, 0x00)
        #write_register(REG_FIFO_ADDR_PTR, 0x00)
        #write_register(REG_OP_MODE, 0x85)
        return data
    time.sleep(0.1)
    return None

if __name__ == "__main__":
    try:
        # Configuración inicial
        GPIO.setup(DIO0_PIN, GPIO.IN)
        
        if not init_lora():
            raise RuntimeError("Fallo al inicializar LoRa")

        print("Esperando datos en 433 MHz (Ctrl+C para salir)...")
        data = receive_data()  # Recibe datos RAW sin conversión
        if data:
            print(f"Paquete recibido: {data} | RSSI: {read_register(REG_PKT_RSSI_VALUE)-164} dBm")
        else:
            print("no hay datos")
        time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nInterrupción por usuario")
    finally:
        # Liberación segura de recursos
        spi.close()
        GPIO.cleanup()
        print("SPI y GPIO liberados correctamente")