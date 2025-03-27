import spidev

# Configuración SPI sin GPIO para CS (usando CS hardware)
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0 (CS hardware)
spi.max_speed_hz = 500000

def read_register(reg):
    return spi.xfer2([reg & 0x7F, 0x00])[1]

version = read_register(0x42)
print(f"Versión del chip: {hex(version)}")