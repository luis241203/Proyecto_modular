import tkinter as tk

root = tk.Tk()
root.title("Prueba Tkinter")
root.geometry("400x300")

label = tk.Label(root, text="¡Hola desde Tkinter!")
label.pack(pady=20)

root.mainloop()
