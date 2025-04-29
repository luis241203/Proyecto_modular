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

# Registros SX1278
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
REG_FIFO_RX_CURRENT_ADDR = 0x10
REG_RX_NB_BYTES = 0x13
REG_PKT_SNR_VALUE = 0x19
REG_PKT_RSSI_VALUE = 0x1A
REG_FIFO_RX_BASE_ADDR = 0x0F  # <- importante

def read_register(register):
    return spi.xfer2([register & 0x7F, 0x00])[1]

def write_register(register, value):
    spi.xfer2([register | 0x80, value])

def init_lora():
    GPIO.setup(RESET_PIN, GPIO.OUT)
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.01)
    
    write_register(REG_OP_MODE, 0x80)  # Sleep + LoRa
    time.sleep(0.1)
    
    if read_register(REG_VERSION) != 0x12:
        print("Error: Chip no reconocido")
        return False
    
    write_register(REG_FRF_MSB, 0x6C)
    write_register(REG_FRF_MID, 0x40)
    write_register(REG_FRF_LSB, 0x00)
    
    write_register(REG_MODEM_CONFIG1, 0x72)
    write_register(REG_MODEM_CONFIG2, 0x74)
    
    write_register(REG_PA_CONFIG, 0x8F)
    
    write_register(REG_FIFO_TX_BASE_ADDR, 0x80)
    write_register(REG_FIFO_RX_BASE_ADDR, 0x00)  # <- importante para recepción correcta

    write_register(REG_OP_MODE, 0x81)  # Standby
    time.sleep(0.1)
    
    print("LoRa listo para transmitir y recibir")
    return True

def send_data(data):
    write_register(REG_OP_MODE, 0x81)  # standby
    time.sleep(0.05)
    
    write_register(REG_FIFO_ADDR_PTR, 0x80)
    
    for byte in data:
        write_register(REG_FIFO, byte)
    
    write_register(REG_PAYLOAD_LENGTH, len(data))
    write_register(REG_OP_MODE, 0x83)  # modo transmisión
    
    timeout = time.time() + 5
    while (read_register(REG_IRQ_FLAGS) & 0x08) == 0:
        if time.time() > timeout:
            print("Error: Timeout en transmisión")
            break
        time.sleep(0.05)
    
    write_register(REG_IRQ_FLAGS, 0x08)  # limpiar TxDone
    write_register(REG_OP_MODE, 0x81)  # standby
    
    print(f"Datos enviados: {data}")

def receive_data(timeout_s=5):
    write_register(REG_OP_MODE, 0x85)  # Modo recepción continua
    start_time = time.time()
    
    while True:
        irq_flags = read_register(REG_IRQ_FLAGS)
        
        if irq_flags & 0x40:  # RxDone
            length = read_register(REG_RX_NB_BYTES)
            current_addr = read_register(REG_FIFO_RX_CURRENT_ADDR)
            write_register(REG_FIFO_ADDR_PTR, current_addr)
            
            data = []
            for _ in range(length):
                data.append(read_register(REG_FIFO))
            
            text_data = bytes(data).decode('ascii', errors='replace')
            
            rssi = read_register(REG_PKT_RSSI_VALUE) - 164
            snr = read_register(REG_PKT_SNR_VALUE) * 0.25
            
            write_register(REG_IRQ_FLAGS, 0xFF)  # limpiar todos los flags
            
            print(f"Datos recibidos: {text_data} | RSSI: {rssi} dBm | SNR: {snr} dB")
            return text_data
        
        if time.time() - start_time > timeout_s:
            print("Timeout esperando respuesta")
            write_register(REG_IRQ_FLAGS, 0xFF)  # limpiar flags
            break
        
        time.sleep(0.05)
    
    return None

if __name__ == "__main__":
    try:
        if init_lora():
            while True:
                # Enviar una sola 'a'
                payload = [ord('a')]  # <- CAMBIO
                send_data(payload)
                
                # Esperar la respuesta
                respuesta = receive_data(timeout_s=5)
                
                if respuesta:
                    print(f"Respuesta recibida: {respuesta}")
                else:
                    print("No se recibió respuesta")
                
                time.sleep(5)  # Esperar antes de volver a enviar
    except KeyboardInterrupt:
        print("Programa detenido manualmente")
    finally:
        spi.close()
        GPIO.cleanup()
