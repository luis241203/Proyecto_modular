import tkinter as tk

def crear_label(root, texto, nombre, labels_dict, border, color, letra_color, size_letra):
    # Crear un nuevo Label y agregarlo al diccionario
    label = tk.Label(root, text=texto, font=("Arial", size_letra, "bold"), bd=border, relief="solid", bg = color, fg = letra_color)
    label.pack(padx=10, pady=7, fill="x")
    labels_dict[nombre] = label  # Guardar la referencia en el diccionario

def actualizar_label(labels_dict, nombre, nuevo_texto):
    # Actualizar el texto de un Label existente
    if nombre in labels_dict:
        labels_dict[nombre].config(text=nuevo_texto)

root = tk.Tk()
root.geometry("1024x600")
root.config(bg="beige")

# Diccionario para almacenar los labels
labels = {}
# LABEL DE BIENVENIDA
crear_label(root, "ACUAPONIC MONITOR", "label_Welcome", labels, 0, "beige", "black", 25)

# LABEL TEMPERATURA AGUA
crear_label(root, "TEMPERATURA AGUA", "label_temp_agua", labels, 2, "white", "black", 12)
crear_label(root, "35.6", "label_temp_agua_data", labels, 0, "beige", "green", 15)

# LABEL TEMPERATURA AMBIENTE
crear_label(root, "TEMPERATURA AMBIENTE", "label_temp_amb", labels, 2, "white", "black", 12)
crear_label(root, "40.1", "label_temp_amb_data", labels, 0, "beige", "green", 15)

# LABEL TURBIDEZ
crear_label(root, "TURBIDEZ", "label_turb", labels, 2, "white", "black", 12)
crear_label(root, "70%", "label_turb_data", labels, 0, "beige", "green", 15)

# LABEL LUMINOSIDAD
crear_label(root, "LUMINOSIDAD", "label_lum", labels, 2, "white", "black", 12)
crear_label(root, "35%", "label_lum_data", labels, 0, "beige", "green", 15)

# LABEL HUMEDAD
crear_label(root, "HUMEDAD", "label_hum", labels, 2, "white", "black", 12)
crear_label(root, "16%", "label_hum_data", labels, 0, "beige", "green", 15)

# LABEL PH
crear_label(root, "PH DE AGUA", "label_ph", labels, 2, "white", "black", 12)
crear_label(root, "365", "label_ph_data", labels, 0, "beige", "green", 15)

# Actualizar un label después de un tiempo
root.after(2000, actualizar_label, labels, "label1", "Texto actualizado para Label 1")

root.mainloop()
