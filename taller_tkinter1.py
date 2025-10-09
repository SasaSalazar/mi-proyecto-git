import sqlite3
import tkinter as tk
from tkinter import messagebox

# Conexión con la base de datos
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    telefono TEXT,
    carrera TEXT,
    materia TEXT
)
""")
conn.commit()

# --- Funciones CRUD ---
def insertar():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()
    carrera = entry_carrera.get()
    materia = entry_materia.get()
    if nombre and correo:
        cursor.execute("INSERT INTO usuarios (nombre, correo, telefono, carrera, materia) VALUES (?, ?, ?, ?, ?)",
                       (nombre, correo, telefono, carrera, materia))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        limpiar()
    else:
        messagebox.showwarning("Error", "Los campos nombre y correo son obligatorios.")

def listar():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    lista.delete(0, tk.END)
    for u in usuarios:
        lista.insert(tk.END, f"{u[0]} - {u[1]} - {u[2]} - {u[3]} - {u[4]} - {u[5]}")

def eliminar():
    codigo = entry_codigo.get()
    if codigo:
        cursor.execute("DELETE FROM usuarios WHERE codigo=?", (codigo,))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        limpiar()
    else:
        messagebox.showwarning("Error", "Debe ingresar un código válido.")

def actualizar():
    codigo = entry_codigo.get()
    if codigo:
        cursor.execute("""UPDATE usuarios
                          SET nombre=?, correo=?, telefono=?, carrera=?, materia=?
                          WHERE codigo=?""",
                       (entry_nombre.get(), entry_correo.get(), entry_telefono.get(),
                        entry_carrera.get(), entry_materia.get(), codigo))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        limpiar()
    else:
        messagebox.showwarning("Error", "Debe ingresar un código válido.")

def limpiar():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_carrera.delete(0, tk.END)
    entry_materia.delete(0, tk.END)

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Gestión de Usuarios")

tk.Label(root, text="Código").grid(row=0, column=0)
tk.Label(root, text="Nombre").grid(row=1, column=0)
tk.Label(root, text="Correo").grid(row=2, column=0)
tk.Label(root, text="Teléfono").grid(row=3, column=0)
tk.Label(root, text="Carrera").grid(row=4, column=0)
tk.Label(root, text="Materia").grid(row=5, column=0)

entry_codigo = tk.Entry(root)
entry_nombre = tk.Entry(root)
entry_correo = tk.Entry(root)
entry_telefono = tk.Entry(root)
entry_carrera = tk.Entry(root)
entry_materia = tk.Entry(root)

entry_codigo.grid(row=0, column=1)
entry_nombre.grid(row=1, column=1)
entry_correo.grid(row=2, column=1)
entry_telefono.grid(row=3, column=1)
entry_carrera.grid(row=4, column=1)
entry_materia.grid(row=5, column=1)

tk.Button(root, text="Agregar", command=insertar).grid(row=6, column=0)
tk.Button(root, text="Listar", command=listar).grid(row=6, column=1)
tk.Button(root, text="Actualizar", command=actualizar).grid(row=7, column=0)
tk.Button(root, text="Eliminar", command=eliminar).grid(row=7, column=1)
tk.Button(root, text="Limpiar", command=limpiar).grid(row=8, column=0)

lista = tk.Listbox(root, width=80)
lista.grid(row=9, column=0, columnspan=2)

root.mainloop()
conn.close()
