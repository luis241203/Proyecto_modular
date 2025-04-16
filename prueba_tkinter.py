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

root.mainloop()
