import tkinter as tk
from tkinter import *
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
    label.pack(padx=10, pady=5, fill="x")
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
    ventana_ajustes.geometry("1024x500")
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
    temp_agua_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL TEMPERATURA AGUA
    crear_label(temp_agua_conteiner, "RANGO DE TEMPERATURA DEL AGUA (°C):", "label_temp_agua", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_temp_agua"].pack(side="left", expand=True)
    labels["label_temp_agua"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_temp_agua_min, text_temp_agua_max 
    text_temp_agua_min = Spinbox(temp_agua_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_temp_agua_min.pack(side="left",padx=10, pady=5, fill="both")
    text_temp_agua_max = Spinbox(temp_agua_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_temp_agua_max.pack(side="left",padx=10, pady=5, fill="both")

#############################################################################  

##################APARTADO DE TEMPERATURA DEL AMBIENTE#######################

    #Creacion de contenedores
    temp_amb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    temp_amb_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL TEMPERATURA AMBIENTE
    crear_label(temp_amb_conteiner, "RANGO DE TEMPERATURA DEL AMBIENTE (°C):", "label_temp_amb", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_temp_amb"].pack(side="left", expand=True)
    labels["label_temp_amb"].config(anchor = "w")

    #OBTENCION DE PARAMETROS
    global text_temp_amb_min, text_temp_amb_max 
    text_temp_amb_min = Spinbox(temp_amb_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_temp_amb_min.pack(side="left",padx=10, pady=5, fill="both")
    text_temp_amb_max = Spinbox(temp_amb_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_temp_amb_max.pack(side="left",padx=10, pady=5, fill="both")

#############################################################################   

##################APARTADO DE TURBIDEZ#######################

    #Creacion de contenedores
    turb_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    turb_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL TURBIDEZ
    crear_label(turb_conteiner, "TURBIDEZ LIMITE (NTU):", "label_turb", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_turb"].pack(side="left", expand=True)
    labels["label_turb"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_turb_max
    text_turb_max = Scale(turb_conteiner, from_=0, to=100, orient=HORIZONTAL,background="#FFB380", width=20, length=500)
    text_turb_max.pack(side="left",padx=10, pady=5, fill="both")
#############################################################

##################APARTADO DE LUMINOSIDAD#######################

    #Creacion de contenedores
    lum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    lum_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL LUMINOSIDAD
    crear_label(lum_conteiner, "LUMINOSIDAD DE BOMBILLA DESEADA (%):", "label_lum", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_lum"].pack(side="left", expand=True)
    labels["label_lum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS
    global text_lum_max
    text_lum_max = Scale(lum_conteiner, from_=0, to=100, orient=HORIZONTAL,background="#FFB380", width=20, length=500)
    text_lum_max.pack(side="left",padx=10, pady=5, fill="both")
################################################################

##################APARTADO DE HUMEDAD#######################

    #Creacion de contenedores
    hum_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    hum_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL HUMEDAD
    crear_label(hum_conteiner, "RANGO DE HUMEDAD (%HR):", "label_hum", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_hum"].pack(side="left", expand=True)
    labels["label_hum"].config(anchor = "w")
    #OBTENCION DE PARAMETROS

    global text_hum_min, text_hum_max 
    text_hum_min = Spinbox(hum_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_hum_min.pack(side="left",padx=10, pady=5, fill="both")
    text_hum_max = Spinbox(hum_conteiner, from_=30, to=50, increment=1, font=("Arial", 14, "bold"))
    text_hum_max.pack(side="left",padx=10, pady=5, fill="both")
################################################################


##################APARTADO DE CAUDAL################################

    #Creacion de contenedores
    caudal_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    caudal_conteiner.pack(padx=10,pady=5,fill="x")

    # LABEL CAUDAL
    crear_label(caudal_conteiner, "CAUDAL REQUERIDO (L/min):", "label_caudal", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_caudal"].pack(side="left", expand=True)
    labels["label_caudal"].config(anchor = "w")    
    #OBTENCION DE PARAMETROS
    global text_caudal_min
    text_caudal_min = Scale(caudal_conteiner, from_=0, to=100, orient=HORIZONTAL,background="#FFB380", width=20, length=500)
    text_caudal_min.pack(side="left",padx=10, fill="both")
####################################################################


##################APARTADO DE NIVEL################################

    #Creacion de contenedores
    nivel_conteiner = tk.Frame(ventana_ajustes,bg="AntiqueWhite")
    nivel_conteiner.pack(padx=10,pady=5,fill="x")

    # NIVEL nivel
    crear_label(nivel_conteiner, "NIVEL MINIMO (%):", "label_nivel", labels, 0, "AntiqueWhite", "black", 14)
    labels["label_nivel"].pack(side="left", expand=True)
    labels["label_nivel"].config(anchor = "w")    
    #OBTENCION DE PARAMETROS
    global text_nivel_min
    text_nivel_min = Scale(nivel_conteiner, from_=0, to=100, orient=HORIZONTAL,background="#FFB380", width=20, length=500)
    text_nivel_min.pack(side="left",padx=10, fill="both") 
####################################################################

    #FRAME DE BOTONES
    botones_frame = tk.Frame(ventana_ajustes, bg="AntiqueWhite")  # Mismo color de fondo
    botones_frame.pack(pady=5, fill='x', padx=25)  # Ajusta el padding según necesites

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
    boton_guardar.pack(fill='x', padx=25, side="left", expand=True)

    # Actualizar un label después de un tiempo
    ventana_ajustes.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")

    ventana_ajustes.mainloop()

def escape():
    ventana_ajustes.attributes('-fullscreen', False)
#crear_ventana_ajustes()