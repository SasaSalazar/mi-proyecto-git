import tkinter as tk
from tkinter import messagebox
import requests

URL = "http://127.0.0.1:5000"

def insertar():
    data = {
        "nombre": entry_nombre.get(),
        "correo": entry_correo.get(),
        "telefono": entry_telefono.get(),
        "carrera": entry_carrera.get(),
        "materia": entry_materia.get()
    }
    resp = requests.post(f"{URL}/insertar", json=data)
    if resp.status_code == 201:
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        listar()
        limpiar()
    else:
        messagebox.showerror("Error", resp.json().get("error"))

def listar():
    lista.delete(0, tk.END)
    resp = requests.get(f"{URL}/usuarios")
    if resp.status_code == 200:
        for u in resp.json():
            lista.insert(tk.END, f"{u['codigo']} - {u['nombre']} - {u['correo']} - {u['telefono']} - {u['carrera']} - {u['materia']}")

def eliminar():
    codigo = entry_codigo.get()
    if not codigo.isdigit():
        messagebox.showwarning("Error", "Ingrese un código válido.")
        return
    resp = requests.delete(f"{URL}/eliminar/{codigo}")
    if resp.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        listar()
        limpiar()
    else:
        messagebox.showerror("Error", resp.json().get("error"))

def actualizar():
    codigo = entry_codigo.get()
    if not codigo:
        messagebox.showwarning("Error", "Debe ingresar un código válido.")
        return
    data = {
        "codigo": int(codigo),
        "nombre": entry_nombre.get(),
        "correo": entry_correo.get(),
        "telefono": entry_telefono.get(),
        "carrera": entry_carrera.get(),
        "materia": entry_materia.get()
    }
    resp = requests.put(f"{URL}/actualizar", json=data)
    if resp.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        listar()
        limpiar()
    else:
        messagebox.showerror("Error", resp.json().get("error"))

def limpiar():
    for e in [entry_codigo, entry_nombre, entry_correo, entry_telefono, entry_carrera, entry_materia]:
        e.delete(0, tk.END)

root = tk.Tk()
root.title("Cliente Tkinter + Flask")

labels = ["Código", "Nombre", "Correo", "Teléfono", "Carrera", "Materia"]
entries = []
for i, text in enumerate(labels):
    tk.Label(root, text=text).grid(row=i, column=0, padx=5, pady=5)
    e = tk.Entry(root, width=40)
    e.grid(row=i, column=1, padx=5, pady=5)
    entries.append(e)

(entry_codigo, entry_nombre, entry_correo, entry_telefono, entry_carrera, entry_materia) = entries

tk.Button(root, text="Agregar", command=insertar).grid(row=6, column=0, pady=5)
tk.Button(root, text="Listar", command=listar).grid(row=6, column=1, pady=5)
tk.Button(root, text="Actualizar", command=actualizar).grid(row=7, column=0, pady=5)
tk.Button(root, text="Eliminar", command=eliminar).grid(row=7, column=1, pady=5)
tk.Button(root, text="Limpiar", command=limpiar).grid(row=8, column=0, pady=5)

lista = tk.Listbox(root, width=100)
lista.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
