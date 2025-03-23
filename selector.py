import tkinter as tk
import main as main
def create_monitoring():
    root.destroy()
    main.crear_ventana_monitor()

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
root.title("ACUAPONIAC SYSTEM")
labels = {}

# LABEL DE BIENVENIDA
crear_label(root, "ACUAPONIC MENU", "label_Welcome", labels, 0, "gray", "black", 25)

# LABEL DE SELECCION
crear_label(root, "SELECCIONA UNA DE LAS SIGUIENTES OPCIONES:", "label_Welcome", labels, 0, "beige", "black", 25)

# CREACION DE CONTENEDOR PARA BOTONES
botones = tk.Frame(root,bg="gray")
botones.pack(padx=10, pady=10, fill='x',side="bottom")

# BOTON DE MONITOREO
boton1 = tk.Button(botones, text="MONITOREO", font=("Arial", 16, "bold"), command=create_monitoring)
boton1.pack(fill='x', padx=5, pady=5, side="right", expand=True)

#BOTON DE AJUSTE
boton2 = tk.Button(botones, text="AJUSTES", font=("Arial", 16, "bold"))
boton2.pack(fill='x', padx=5, pady=5, side="left", expand=True)


root.mainloop()