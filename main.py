import tkinter as tk
import selector as select

def regresar_ajustes():
    ventana_monitor.destroy()
    select.create_select()

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
    labels = {}
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


    # Actualizar un label después de un tiempo
    ventana_monitor.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")

    ventana_monitor.mainloop()

def escape():
    ventana_monitor.attributes('-fullscreen', False)
#crear_ventana_monitor()