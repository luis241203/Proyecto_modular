import spidev
import time
import RPi.GPIO as GPIO

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
DIO0_PIN = 17  # Pin para interrupción RxDone (opcional pero recomendado)
RESET_PIN = 22  # Pin de reset

# Configuración SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 500000
spi.mode = 0b00

# Registros SX1278 (para recepción)
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
# Registros SX1278 (completos para RX)
REG_FIFO_ADDR_PTR = 0x0D
REG_FIFO_RX_BASE_ADDR = 0x0F  # <-- ¡Este faltaba!
IRQ_RX_DONE_MASK = 0x40

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
    if read_register(0x42) != 0x12:  # REG_VERSION
        print("Error: Chip no reconocido")
        return False
    
    write_register(REG_FRF_MSB, 0x6C)  # 433 MHz: 0x6C4000
    write_register(REG_FRF_MID, 0x40)
    write_register(REG_FRF_LSB, 0x00)
    
    # Config modem
    write_register(REG_MODEM_CONFIG1, 0x72)  # BW=125kHz, CR=4/5
    write_register(REG_MODEM_CONFIG2, 0x74)  # SF=7, CRC enabled
    
    # Config FIFO RX
    write_register(REG_FIFO_RX_BASE_ADDR, 0x00)  # Dirección base RX
    write_register(REG_FIFO_ADDR_PTR, 0x00)       # Resetear puntero
    
    # Modo RX continuo
    write_register(REG_OP_MODE, 0x85)
    time.sleep(0.1)
    
    print("LoRa listo para recibir")
    return True

def lora_recibido():
    if (read_register(REG_IRQ_FLAGS) & IRQ_RX_DONE_MASK):
        return True
    else:
        return False

def receive_data():
    # Limpiar flags previos y verificar recepción
    irq_flags = read_register(REG_IRQ_FLAGS)
    
    if not (irq_flags & IRQ_RX_DONE_MASK):
        return None
    
    # Cambiar a modo standby para operación segura
    write_register(REG_OP_MODE, 0x81)
    time.sleep(0.01)  # Pequeña espera para estabilizar
    
    # Obtener datos
    length = read_register(REG_RX_NB_BYTES)
    current_addr = read_register(REG_FIFO_RX_CURRENT_ADDR)
    write_register(REG_FIFO_ADDR_PTR, current_addr)
    
    data = [read_register(REG_FIFO) for _ in range(length)]
    
    # Métricas RF
    rssi = read_register(REG_PKT_RSSI_VALUE) - 164  # Ajuste 433MHz
    snr = read_register(REG_PKT_SNR_VALUE) * 0.25
    
    # Preparar para siguiente recepción
    write_register(REG_FIFO_ADDR_PTR, 0x00)
    write_register(REG_OP_MODE, 0x85)  # Crucial: volver a RX continuo
    write_register(REG_IRQ_FLAGS, 0xFF)  # Limpieza completa
    time.sleep(0.01)
    
    print(f"Paquete: {data} | RSSI: {rssi} dBm | SNR: {snr} dB")
    return data

if __name__ == "__main__":
    try:
        GPIO.setup(DIO0_PIN, GPIO.IN)
        
        if not init_lora():
            raise RuntimeError("Error al inicializar LoRa")
        
        print("Receptor activo en 433 MHz. Ctrl+C para salir...")
        
        # Bucle principal optimizado
        while True:
            data = receive_data()
            if not data:
                # Verificación directa del registro por si falla DIO0
                if (read_register(REG_IRQ_FLAGS) & IRQ_RX_DONE_MASK):
                    continue
                time.sleep(0.05)  # Pausa mínima para reducir CPU usage
                
    except KeyboardInterrupt:
        print("\nRecepción detenida")
    finally:
        spi.close()
        GPIO.cleanup()
        print("Recursos liberados")