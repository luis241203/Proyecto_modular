import tkinter as tk
from tkinter import ttk
import main as main
import ajustes as adj

root = tk.Tk()
root.geometry("1024x600")
root.config(bg="#6A9BAE")
root.title("ACUAPONIAC SYSTEM")
root.attributes('-fullscreen', True)
root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))


def crear_label(root, texto, nombre, labels_dict, border, color, letra_color, size_letra):
    # Crear un nuevo Label y agregarlo al diccionario
    label = tk.Label(root, text=texto, font=("Arial", size_letra, "bold"), bd=border, relief="solid", bg = color, fg = letra_color)
    label.pack(padx=10, pady=7, fill="x")
    labels_dict[nombre] = label  # Guardar la referencia en el diccionario

def actualizar_label(labels_dict, nombre, nuevo_texto):
    # Actualizar el texto de un Label existente
    if nombre in labels_dict:
        labels_dict[nombre].config(text=nuevo_texto)


def create_select():
    labels = {}
    image = tk.PhotoImage(file="sources\logo_ambiente.png")
    resized_img = image.subsample(10, 10)
    # LABEL DE BIENVENIDA

    label_conteiner = tk.Frame(root, bg="#A3C1D1", bd=2, relief="ridge")
    label_conteiner.place(relx=0.5, rely=0.5, anchor="center")
    crear_label(label_conteiner, "ACUAPONIC MENU", "label_Welcome", labels, 0, "#A3C1D1", "White", 35)
    labels["label_Welcome"].config(anchor = "center")
    labels["label_Welcome"].pack(padx = 50)

    # IMAGEN
    label_image = ttk.Label(label_conteiner,image=resized_img, background="#A3C1D1")
    label_image.pack()

    # LABEL DE SELECCION
    crear_label(label_conteiner, "SELECCIONA UNA DE LAS SIGUIENTES OPCIONES:", "label_options", labels, 0, "#A3C1D1", "black", 20)
    labels["label_options"].pack(padx=25, pady=25)

    # BOTON DE MONITOREO
    boton1 = tk.Button(label_conteiner, text="MONITOREO", font=("Arial", 16, "bold"), command=create_monitoring,bg="white")
    boton1.pack(fill='x', padx=25, pady=25, side="top", expand=True)

    #BOTON DE AJUSTE
    boton2 = tk.Button(label_conteiner, text="AJUSTES", font=("Arial", 16, "bold"), command=create_adjusting,bg="white")
    boton2.pack(fill='x', padx=25, pady=25, side="top", expand=True)


    root.mainloop()

def create_monitoring():
    root.destroy()
    main.crear_ventana_monitor()

def create_adjusting():
    root.destroy()
    adj.crear_ventana_ajustes()

create_select()