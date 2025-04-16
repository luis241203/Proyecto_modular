import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title("Prueba Tkinter")
root.geometry("400x300")

label = tk.Label(root, text="¡Hola desde Tkinter!")
label.pack(pady=20)
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL)
scale.pack()

# Para obtener el valor:
Button(root, text="Obtener valor", command=lambda: print(scale.get())).pack()

# Spinbox con valores del 0 al 100, incrementos de 1
spinbox = Spinbox(root, from_=90, to=100, increment=1)
spinbox.pack()

root.mainloop()
