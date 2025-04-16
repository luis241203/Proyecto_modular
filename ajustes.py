import tkinter as tk
from tkinter import ttk, messagebox
import selector as select

def guardar_configuracion():
    try:
        # Verificar que todos los campos tengan valores numéricos válidos
        configuracion = {
            'temp_agua_min': float(text_temp_agua_min.get()),
            'temp_agua_max': float(text_temp_agua_max.get()),
            'temp_amb_min': float(text_temp_amb_min.get()),
            'temp_amb_max': float(text_temp_amb_max.get()),
            'turb_max': float(text_turb_max.get()),
            'lum_max': float(text_lum_max.get()),
            'hum_min': float(text_hum_min.get()),
            'hum_max': float(text_hum_max.get()),
            'caudal_min': float(text_caudal_min.get()),
            'nivel_min': float(text_nivel_min.get())
        }
        
        # Verificar que los mínimos sean menores que los máximos
        #for param in ['temp_agua', 'temp_amb', 'turb', 'lum', 'hum']:
        #    min_val = configuracion[f'{param}_min']
        #    max_val = configuracion[f'{param}_max']
        #    if min_val >= max_val:
        #        raise ValueError(f"El mínimo de {param} debe ser menor que el máximo")
        
        # Guardar en archivo
        with open('configuracion_acuaponica.txt', 'w') as archivo:
            for clave, valor in configuracion.items():
                archivo.write(f"{clave}={valor}\n")
        
        messagebox.showinfo("Éxito", "Configuración guardada correctamente")
        
    except ValueError as e:
        messagebox.showerror("Error", f"Datos inválidos: {str(e)}")

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
    crear_label(temp_agua_conteiner, "RANGO DE TEMPERATURA DEL AGUA (°C):", "label_temp_agua", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_temp_agua"].pack(side="left", expand=True)
    labels["label_temp_agua"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_temp_agua_min, text_temp_agua_max 
    text_temp_agua_min = tk.StringVar()
    text_temp_agua_max = tk.StringVar()
    textbox_agua_min = ttk.Entry(temp_agua_conteiner, textvariable=text_temp_agua_min, width=10)
    textbox_agua_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_agua_min.config(font=("Arial", 14, "bold"))

    textbox_agua_max = ttk.Entry(temp_agua_conteiner, textvariable=text_temp_agua_max, width=10)
    textbox_agua_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox_agua_max.config(font=("Arial", 14, "bold"))
#############################################################################  

##################APARTADO DE TEMPERATURA DEL AMBIENTE#######################

    #Creacion de contenedores
    temp_amb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    temp_amb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TEMPERATURA AMBIENTE
    crear_label(temp_amb_conteiner, "RANGO DE TEMPERATURA DEL AMBIENTE (°C):", "label_temp_amb", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_temp_amb"].pack(side="left", expand=True)
    labels["label_temp_amb"].config(anchor = "w")

    #OBTENCION DE PARAMETROS
    global text_temp_amb_min, text_temp_amb_max
    text_temp_amb_min = tk.StringVar()
    text_temp_amb_max = tk.StringVar()
    textbox_amb_min = ttk.Entry(temp_amb_conteiner, textvariable=text_temp_amb_min, width=10)
    textbox_amb_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_amb_min.config(font=("Arial", 14, "bold"))

    textbox2_amb_max = ttk.Entry(temp_amb_conteiner, textvariable=text_temp_amb_max, width=10)
    textbox2_amb_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_amb_max.config(font=("Arial", 14, "bold"))
    #temp = textbox.get
#############################################################################   

##################APARTADO DE TURBIDEZ#######################

    #Creacion de contenedores
    turb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    turb_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL TURBIDEZ
    crear_label(turb_conteiner, "TURBIDEZ LIMITE (NTU):", "label_turb", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_turb"].pack(side="left", expand=True)
    labels["label_turb"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_turb_max
    text_turb_max = tk.StringVar()
    textbox2_turb_max = ttk.Entry(turb_conteiner, textvariable=text_turb_max, width=22)
    textbox2_turb_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_turb_max.config(font=("Arial", 14, "bold"))
#############################################################

##################APARTADO DE LUMINOSIDAD#######################

    #Creacion de contenedores
    lum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    lum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL LUMINOSIDAD
    crear_label(lum_conteiner, "LUMINOSIDAD DE BOMBILLA DESEADA (%):", "label_lum", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_lum"].pack(side="left", expand=True)
    labels["label_lum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_lum_max
    text_lum_max = tk.StringVar()

    textbox2_lum_max = ttk.Entry(lum_conteiner, textvariable=text_lum_max, width=22)
    textbox2_lum_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_lum_max.config(font=("Arial", 14, "bold"))
################################################################

##################APARTADO DE HUMEDAD#######################

    #Creacion de contenedores
    hum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    hum_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL HUMEDAD
    crear_label(hum_conteiner, "RANGO DE HUMEDAD (%HR):", "label_hum", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_hum"].pack(side="left", expand=True)
    labels["label_hum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_hum_min, text_hum_max
    text_hum_min = tk.StringVar()
    text_hum_max = tk.StringVar()
    textbox_hum_min = ttk.Entry(hum_conteiner, textvariable=text_hum_min, width=10)
    textbox_hum_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_hum_min.config(font=("Arial", 14, "bold"))

    textbox2_hum_max = ttk.Entry(hum_conteiner, textvariable=text_hum_max, width=10)
    textbox2_hum_max.pack(side="left",padx=10, pady=7, fill="both")
    textbox2_hum_max.config(font=("Arial", 14, "bold"))
################################################################


##################APARTADO DE CAUDAL################################

    #Creacion de contenedores
    caudal_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    caudal_conteiner.pack(padx=10,pady=10,fill="x")

    # LABEL CAUDAL
    crear_label(caudal_conteiner, "CAUDAL REQUERIDO (L/min):", "label_caudal", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_caudal"].pack(side="left", expand=True)
    labels["label_caudal"].config(anchor = "w")    
    #OBTENCION DE PARAMETROS
    global text_caudal_min
    text_caudal_min = tk.StringVar()
    textbox_caudal_min = ttk.Entry(caudal_conteiner, textvariable=text_caudal_min, width=22)
    textbox_caudal_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_caudal_min.config(font=("Arial", 14, "bold"))  
####################################################################


##################APARTADO DE NIVEL################################

    #Creacion de contenedores
    nivel_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    nivel_conteiner.pack(padx=10,pady=10,fill="x")

    # NIVEL nivel
    crear_label(nivel_conteiner, "NIVEL MINIMO (%):", "label_nivel", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_nivel"].pack(side="left", expand=True)
    labels["label_nivel"].config(anchor = "w")    
    #OBTENCION DE PARAMETROS
    global text_nivel_min
    text_nivel_min = tk.StringVar()
    textbox_nivel_min = ttk.Entry(nivel_conteiner, textvariable=text_nivel_min, width=22)
    textbox_nivel_min.pack(side="left",padx=10, pady=7, fill="both")
    textbox_nivel_min.config(font=("Arial", 14, "bold"))  
####################################################################

    #FRAME DE BOTONES
    botones_frame = tk.Frame(ventana_ajustes, bg="AntiqueWhite")  # Mismo color de fondo
    botones_frame.pack(pady=20, fill='x', padx=25)  # Ajusta el padding según necesites

    # Modifica los botones para que se empaquen DENTRO del frame:
    boton_regresar_ajustes = tk.Button(botones_frame, text="REGRESAR", font=("Arial", 14, "bold"), command=regresar_ajustes, bg="white")
    boton_regresar_ajustes.pack(side="left", expand=True, fill='x', padx=5)  # side="left" para alinearlos horizontalmente

    boton3 = tk.Button(botones_frame, text="ESC", font=("Arial", 14, "bold"), command=escape, bg="white")
    boton3.pack(side="left", expand=True, fill='x', padx=5)  # side="left" para colocarlo junto al anterior

        # BOTON DE GUARDAR CONFIGURACION
    boton_guardar = tk.Button(
        botones_frame, 
        text="GUARDAR CONFIGURACIÓN", 
        font=("Arial", 14, "bold"), 
        command=guardar_configuracion,
        bg="lightgreen"

    )
    boton_guardar.pack(fill='x', padx=25, pady=10, side="left", expand=True)

    # Actualizar un label después de un tiempo
    ventana_ajustes.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")

    ventana_ajustes.mainloop()

def escape():
    ventana_ajustes.attributes('-fullscreen', False)
#crear_ventana_ajustes()