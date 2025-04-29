import tkinter as tk
import selector as select
import spidev
import time
import RPi.GPIO as GPIO
import threading
from queue import Queue

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
DIO0_PIN = 17  # Pin para interrupción RxDone (opcional pero recomendado)
RESET_PIN = 22  # Pin de reset
labels = {}

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

def cerrar_app():
    print("Cerrando aplicación...")

    # Cerrar SPI
    spi.close()

    # Limpiar GPIO
    GPIO.cleanup()

    # Cerrar ventana
    ventana_monitor.destroy()

def read_register(register):
    return spi.xfer2([register & 0x7F, 0x00])[1]

def write_register(register, value):
    spi.xfer2([register | 0x80, value])

def regresar_ajustes():
    ventana_monitor.destroy()
    select.create_select()

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
    
    #print(f"Datos enviados: {data}")

def receive_data(queue,timeout_s=5):
    write_register(REG_OP_MODE, 0x85)  # Modo recepción continua
    start_time = time.time()
    while True:
         
        # Verificar si hay datos recibidos
        irq_flags = read_register(REG_IRQ_FLAGS)
        
        if irq_flags & 0x40:  # RxDone
            # Obtener longitud del paquete
            length = read_register(REG_RX_NB_BYTES)
            
            # Leer datos del FIFO
            current_addr = read_register(REG_FIFO_RX_CURRENT_ADDR)
            write_register(0x0D, current_addr)  # FIFO_ADDR_PTR
            
            data = []
            for _ in range(length):
                data.append(read_register(REG_FIFO))
            
            try:
                text_data = bytes(data).decode('ascii')
                valores_separados = text_data.split(',')
            except:
                pass

            temp_agua, temp_amb, humedad, ldr, tur, ultrasonico, caudal = valores_separados

            # Mostramos los valores
            # Leer RSSI y SNR
            rssi = read_register(REG_PKT_RSSI_VALUE) - 164  # Ajuste para 433MHz
            snr = read_register(REG_PKT_SNR_VALUE) * 0.25
            
            # Limpiar flags
            write_register(REG_IRQ_FLAGS, 0xFF)
            
            #print(f"Datos recibidos: {data} | RSSI: {rssi} dBm | SNR: {snr} dB")
            print(f"Datos recibidos: {text_data} | RSSI: {rssi} dBm | SNR: {snr} dB")

            #print(f"Temperatura Agua: {temp_agua}")
            #print(f"Temperatura Ambiente: {temp_amb}")
            #print(f"Humedad: {humedad}")
            #print(f"LDR: {ldr}")
            #print(f"Tur: {tur}")
           # print(f"Ultrasonico: {ultrasonico}")
            queue.put((temp_agua,temp_amb,humedad,ldr,tur,ultrasonico, caudal))
        if time.time() - start_time > timeout_s:
            print("Timeout esperando respuesta")
            write_register(REG_IRQ_FLAGS, 0xFF)  # limpiar flags
            break
        time.sleep(0.05)

def bilateral():
    while True:
        # Enviar una sola 'a'
        payload = [ord('a')]  # <- CAMBIO
        send_data(payload)
        
        # Esperar la respuesta
        respuesta = receive_data(timeout_s=5)
        
        if respuesta:
            print("Recibido")
        else:
            print("No se recibió respuesta")
        
        time.sleep(5)  # Esperar antes de volver a enviar

def poner_valores_lora(queue):
    try:
        temp_agua, temp_amb, humedad, ldr, tur, ultrasonico, caudal = queue.get_nowait()
        actualizar_label(labels,"label_temp_agua_data",temp_agua)
        actualizar_label(labels,"label_temp_amb_data",temp_amb)
        actualizar_label(labels,"label_turb_data",tur)
        actualizar_label(labels,"label_lum_data",ldr)
        actualizar_label(labels,"label_hum_data",humedad)
        actualizar_label(labels,"label_nivel_data",ultrasonico)
        actualizar_label(labels,"label_caudal_data",caudal)
    except:
        pass
    ventana_monitor.after(100, poner_valores_lora, queue)

def crear_label(ventana_monitor, texto, nombre, labels_dict, border, color, letra_color, size_letra):
    # Crear un nuevo Label y agregarlo al diccionario
    label = tk.Label(ventana_monitor, text=texto, font=("Arial", size_letra, "bold"), bd=border, relief="solid", bg = color, fg = letra_color)
    label.pack(padx=10, pady=7, fill="x")
    labels_dict[nombre] = label  # Guardar la referencia en el diccionario

def actualizar_label(labels_dict, nombre, nuevo_texto):
    # Actualizar el texto de un Label existente
    if nombre in labels_dict:
        labels_dict[nombre].config(text=nuevo_texto)
def crear_ventana_monitor():
    global ventana_monitor
    ventana_monitor = tk.Tk()
    ventana_monitor.geometry("1024x600")
    ventana_monitor.config(bg="AntiqueWhite")
    ventana_monitor.attributes('-fullscreen', True)
    ventana_monitor.bind('<Escape>', lambda e: ventana_monitor.attributes('-fullscreen', False))

    # Diccionario para almacenar los labels
    # LABEL DE BIENVENIDA
    crear_label(ventana_monitor, "ACUAPONIC MONITOR", "label_Welcome", labels, 0, "#F0E68C", "black", 25)

##################APARTADO DE TEMPERATURA DEL AGUA#######################

    #Creacion de contenedores
    temp_agua_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    temp_agua_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TEMPERATURA AGUA
    crear_label(temp_agua_conteiner, "TEMPERATURA AGUA (°C):", "label_temp_agua", labels, 0, "Wheat", "black", 14)
    labels["label_temp_agua"].pack(side="left", expand=True)
    labels["label_temp_agua"].config(anchor = "w")
    crear_label(temp_agua_conteiner, "35.6", "label_temp_agua_data", labels, 0, "Wheat", "green", 14)
    labels["label_temp_agua_data"].pack(side="right", expand=True, padx = 100)
    labels["label_temp_agua_data"].config(anchor = "e")
#############################################################################  

##################APARTADO DE TEMPERATURA DEL AMBIENTE#######################

    #Creacion de contenedores
    temp_amb_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    temp_amb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TEMPERATURA AMBIENTE
    crear_label(temp_amb_conteiner, "TEMPERATURA AMBIENTE (°C):", "label_temp_amb", labels, 0, "Wheat", "black", 14)
    labels["label_temp_amb"].pack(side="left", expand=True)
    labels["label_temp_amb"].config(anchor = "w")
    crear_label(temp_amb_conteiner, "40.1", "label_temp_amb_data", labels, 0, "Wheat", "green", 14)
    labels["label_temp_amb_data"].pack(side="right", expand=True, padx = 100)
    labels["label_temp_amb_data"].config(anchor = "e")
#############################################################################   

##################APARTADO DE TURBIDEZ#######################

    #Creacion de contenedores
    turb_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    turb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TURBIDEZ
    crear_label(turb_conteiner, "TURBIDEZ (NTU):", "label_turb", labels, 0, "Wheat", "black", 14)
    labels["label_turb"].pack(side="left", expand=True)
    labels["label_turb"].config(anchor = "w")
    crear_label(turb_conteiner, "70%", "label_turb_data", labels, 0, "Wheat", "green", 14)
    labels["label_turb_data"].pack(side="right", expand=True, padx = 100)
    labels["label_turb_data"].config(anchor = "e")
#############################################################

##################APARTADO DE LUMINOSIDAD#######################

    #Creacion de contenedores
    lum_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    lum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL LUMINOSIDAD
    crear_label(lum_conteiner, "LUMINOSIDAD (%):", "label_lum", labels, 0, "Wheat", "black", 14)
    labels["label_lum"].pack(side="left", expand=True)
    labels["label_lum"].config(anchor = "w")
    crear_label(lum_conteiner, "35%", "label_lum_data", labels, 0, "Wheat", "green", 14)
    labels["label_lum_data"].pack(side="right", expand=True, padx = 100)
    labels["label_lum_data"].config(anchor = "e")
################################################################

##################APARTADO DE HUMEDAD#######################

    #Creacion de contenedores
    hum_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    hum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL HUMEDAD
    crear_label(hum_conteiner, "HUMEDAD (%HR):", "label_hum", labels, 0, "Wheat", "black", 14)
    labels["label_hum"].pack(side="left", expand=True)
    labels["label_hum"].config(anchor = "w")
    crear_label(hum_conteiner, "16%", "label_hum_data", labels, 0, "Wheat", "green", 14)
    labels["label_hum_data"].pack(side="right", expand=True, padx = 100)
    labels["label_hum_data"].config(anchor = "e")
################################################################


##################APARTADO DE CAUDAL################################

    #Creacion de contenedores
    caudal_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    caudal_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL CAUDAL
    crear_label(caudal_conteiner, "CAUDAL (L/min):", "label_caudal", labels, 0, "Wheat", "black", 14)
    labels["label_caudal"].pack(side="left", expand=True)
    labels["label_caudal"].config(anchor = "w")    
    crear_label(caudal_conteiner, "20%", "label_caudal_data", labels, 0, "Wheat", "green", 14)
    labels["label_caudal_data"].pack(side="right", expand=True, padx = 100)
    labels["label_caudal_data"].config(anchor = "e")    
####################################################################


##################APARTADO DE nivel################################

    #Creacion de contenedores
    nivel_conteiner = tk.Frame(ventana_monitor,bg="Wheat")
    nivel_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL NIVEL
    crear_label(nivel_conteiner, "NIVEL (%):", "label_nivel", labels, 0, "Wheat", "black", 14)
    labels["label_nivel"].pack(side="left", expand=True)
    labels["label_nivel"].config(anchor = "w")    
    crear_label(nivel_conteiner, "20%", "label_nivel_data", labels, 0, "Wheat", "green", 14)
    labels["label_nivel_data"].pack(side="right", expand=True, padx = 100)
    labels["label_nivel_data"].config(anchor = "e")    
####################################################################


    #FRAME DE BOTONES
    botones_frame = tk.Frame(ventana_monitor, bg="AntiqueWhite")  # Mismo color de fondo
    botones_frame.pack(pady=20, fill='x', padx=25)  # Ajusta el padding según necesites

    # Modifica los botones para que se empaquen DENTRO del frame:
    boton_regresar_ajustes = tk.Button(botones_frame, text="REGRESAR", font=("Arial", 14, "bold"), command=regresar_ajustes, bg="white")
    boton_regresar_ajustes.pack(side="left", expand=True, fill='x', padx=5)  # side="left" para alinearlos horizontalmente

    boton3 = tk.Button(botones_frame, text="ESC", font=("Arial", 14, "bold"), command=escape, bg="white")
    boton3.pack(side="left", expand=True, fill='x', padx=5)  # side="left" para colocarlo junto al anterior

    queue = Queue()
    if (init_lora() != True):
        print("no se inicio bien el modulo LoRa")
        regresar_ajustes()

    thread_lora = threading.Thread(target=bilateral, args=(queue,))
    thread_lora.daemon = True  # Este hilo se cerrará cuando se cierre la aplicación principal
    thread_lora.start()

    # Iniciar la actualización de la interfaz de Tkinter
    poner_valores_lora(queue)


    # Actualizar un label después de un tiempo
    #ventana_monitor.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")
    ventana_monitor.protocol("WM_DELETE_WINDOW", cerrar_app)

    ventana_monitor.mainloop()

def escape():
    ventana_monitor.attributes('-fullscreen', False)
#crear_ventana_monitor()