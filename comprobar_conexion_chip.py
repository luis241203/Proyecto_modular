import spidev
import RPi.GPIO as GPIO

# Configuración SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Chip Select 0
spi.max_speed_hz = 500000  # Velocidad recomendada para SX1278

# Configuración GPIO para CS (opcional, si no usas CS hardware)
CS_PIN = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)

def read_register(reg):
    GPIO.output(CS_PIN, GPIO.LOW)
    response = spi.xfer2([reg & 0x7F, 0x00])
    GPIO.output(CS_PIN, GPIO.HIGH)
    return response[1]

def write_register(reg, value):
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.xfer2([reg | 0x80, value])
    GPIO.output(CS_PIN, GPIO.HIGH)

# Ejemplo: Leer la versión del chip (debería devolver 0x12 para SX1278)
version = read_register(0x42)
print(f"Versión del chip: {hex(version)}")