import tkinter as tk
from tkinter import ttk
import selector as select

def crear_label(ventana_ajustes, texto, nombre, labels_dict, border, color, letra_color, size_letra):
    # Crear un nuevo Label y agregarlo al diccionario
    label = tk.Label(ventana_ajustes, text=texto, font=("Arial", size_letra, "bold"), bd=border, relief="solid", bg = color, fg = letra_color)
    label.pack(padx=10, pady=7, fill="x")
    labels_dict[nombre] = label  # Guardar la referencia en el diccionario

def actualizar_label(labels_dict, nombre, nuevo_texto):
    # Actualizar el texto de un Label existente
    if nombre in labels_dict:
        labels_dict[nombre].config(text=nuevo_texto)
def regresar_ajustes():
    ventana_ajustes.destroy()
    select.create_select()

def crear_ventana_ajustes():
    global ventana_ajustes
    ventana_ajustes = tk.Tk()
    ventana_ajustes.geometry("1024x600")
    ventana_ajustes.config(bg="AntiqueWhite")
    ventana_ajustes.attributes('-fullscreen', True)
    ventana_ajustes.bind('<Escape>', lambda e: ventana_ajustes.attributes('-fullscreen', False))

    # Diccionario para almacenar los labels
    labels = {}
    # LABEL DE BIENVENIDA
    crear_label(ventana_ajustes, "ACUAPONIC SETTINGS", "label_Welcome", labels, 0, "#F0E68C", "black", 25)

##################APARTADO DE TEMPERATURA DEL AGUA#######################

    #Creacion de contenedores
    temp_agua_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    temp_agua_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TEMPERATURA AGUA
    crear_label(temp_agua_conteiner, "TEMPERATURA DESEADA DEL AGUA :", "label_temp_agua", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_temp_agua"].pack(side="left", expand=True)
    labels["label_temp_agua"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    text_temp_agua_min = tk.StringVar()
    text_temp_agua_max = tk.StringVar()
    textbox_agua_min = ttk.Entry(temp_agua_conteiner, textvariable=text_temp_agua_min, width=10)
    textbox_agua_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_agua_min.config(font=("Arial", 20, "bold"))

    textbox_agua_max = ttk.Entry(temp_agua_conteiner, textvariable=text_temp_agua_max, width=10)
    textbox_agua_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox_agua_max.config(font=("Arial", 20, "bold"))
#############################################################################  

##################APARTADO DE TEMPERATURA DEL AMBIENTE#######################

    #Creacion de contenedores
    temp_amb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    temp_amb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TEMPERATURA AMBIENTE
    crear_label(temp_amb_conteiner, "TEMPERATURA DESEADA DEL AMBIENTE :", "label_temp_amb", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_temp_amb"].pack(side="left", expand=True)
    labels["label_temp_amb"].config(anchor = "w")

    #OBTENCION DE PARAMETROS
    text_temp_amb_min = tk.StringVar()
    text_temp_amb_max = tk.StringVar()
    textbox_amb_min = ttk.Entry(temp_amb_conteiner, textvariable=text_temp_amb_min, width=10)
    textbox_amb_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_amb_min.config(font=("Arial", 20, "bold"))

    textbox2_amb_max = ttk.Entry(temp_amb_conteiner, textvariable=text_temp_amb_max, width=10)
    textbox2_amb_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_amb_max.config(font=("Arial", 20, "bold"))
    #temp = textbox.get
#############################################################################   

##################APARTADO DE TURBIDEZ#######################

    #Creacion de contenedores
    turb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    turb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TURBIDEZ
    crear_label(turb_conteiner, "TURBIDEZ :", "label_turb", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_turb"].pack(side="left", expand=True)
    labels["label_turb"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    text_turb_min = tk.StringVar()
    text_turb_max = tk.StringVar()
    textbox_turb_min = ttk.Entry(turb_conteiner, textvariable=text_turb_min, width=10)
    textbox_turb_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_turb_min.config(font=("Arial", 20, "bold"))

    textbox2_turb_max = ttk.Entry(turb_conteiner, textvariable=text_turb_max, width=10)
    textbox2_turb_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_turb_max.config(font=("Arial", 20, "bold"))
#############################################################

##################APARTADO DE LUMINOSIDAD#######################

    #Creacion de contenedores
    lum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    lum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL LUMINOSIDAD
    crear_label(lum_conteiner, "LUMINOSIDAD  MINIMA :", "label_lum", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_lum"].pack(side="left", expand=True)
    labels["label_lum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    text_lum_min = tk.StringVar()
    text_lum_max = tk.StringVar()
    textbox_lum_min = ttk.Entry(lum_conteiner, textvariable=text_lum_min, width=10)
    textbox_lum_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_lum_min.config(font=("Arial", 20, "bold"))

    textbox2_lum_max = ttk.Entry(lum_conteiner, textvariable=text_lum_max, width=10)
    textbox2_lum_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_lum_max.config(font=("Arial", 20, "bold"))
################################################################

##################APARTADO DE HUMEDAD#######################

    #Creacion de contenedores
    hum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    hum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL HUMEDAD
    crear_label(hum_conteiner, "HUMEDAD DESEADA :", "label_hum", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_hum"].pack(side="left", expand=True)
    labels["label_hum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    text_hum_min = tk.StringVar()
    text_hum_max = tk.StringVar()
    textbox_hum_min = ttk.Entry(hum_conteiner, textvariable=text_hum_min, width=10)
    textbox_hum_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_hum_min.config(font=("Arial", 20, "bold"))

    textbox2_hum_max = ttk.Entry(hum_conteiner, textvariable=text_hum_max, width=10)
    textbox2_hum_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_hum_max.config(font=("Arial", 20, "bold"))
################################################################


##################APARTADO DE CAUDAL################################

    #Creacion de contenedores
    caudal_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    caudal_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL CAUDAL
    crear_label(caudal_conteiner, "CAUDAL REQUERIDO:", "label_caudal", labels, 0, "AntiqueWhite", "black", 20)
    labels["label_caudal"].pack(side="left", expand=True)
    labels["label_caudal"].config(anchor = "w")    
    #OBTENCION DE PARAMETROS
    text_caudal_min = tk.StringVar()
    textbox_caudal_min = ttk.Entry(caudal_conteiner, textvariable=text_caudal_min, width=22)
    textbox_caudal_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_caudal_min.config(font=("Arial", 20, "bold"))  
####################################################################
    #BOTON DE REGRESAR
    boton_regresar_ajustes = tk.Button(ventana_ajustes, text="REGRESAR", font=("Arial", 25, "bold"), command=regresar_ajustes,bg="white")
    boton_regresar_ajustes.pack(fill='x', padx=25, pady=25, side="top", expand=True)

    #BOTON DE ESCAPE
    boton3 = tk.Button(ventana_ajustes, text="ESC", font=("Arial", 16, "bold"), command=escape,bg="white")
    boton3.pack(fill='x', padx=25, pady=25, side="top", expand=True)

    # Actualizar un label después de un tiempo
    ventana_ajustes.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")

    ventana_ajustes.mainloop()

def escape():
    ventana_ajustes.attributes('-fullscreen', False)
#crear_ventana_ajustes()