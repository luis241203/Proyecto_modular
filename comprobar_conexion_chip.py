import spidev
import time

# Configura SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 500000  # Velocidad reducida para mayor estabilidad
spi.mode = 0b00  # Modo SPI estándar

def read_register(reg):
    try:
        response = spi.xfer2([reg & 0x7F, 0x00])
        return response[1]
    except Exception as e:
        print(f"Error SPI: {e}")
        return 0x00

# Lee múltiples registros clave
registers = {
    "REG_VERSION": 0x42,
    "REG_OP_MODE": 0x01,
    "REG_FRF_MSB": 0x06
}

for name, reg in registers.items():
    value = read_register(reg)
    print(f"{name}: {hex(value)}")

spi.close()