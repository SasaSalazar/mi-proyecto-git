from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla
with conectar() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT,
            carrera TEXT,
            materia TEXT
        )
    """)

# ---- RUTAS CRUD ----
@app.route('/insertar', methods=['POST'])
def insertar():
    data = request.json
    campos = ['nombre', 'correo', 'telefono', 'carrera', 'materia']
    if not data.get('nombre') or not data.get('correo'):
        return jsonify({'error': 'Nombre y correo son obligatorios.'}), 400
    with conectar() as conn:
        conn.execute("""INSERT INTO usuarios (nombre, correo, telefono, carrera, materia)
                        VALUES (?, ?, ?, ?, ?)""",
                        tuple(data.get(campo, '') for campo in campos))
    return jsonify({'mensaje': 'Usuario agregado correctamente.'}), 201

@app.route('/usuarios', methods=['GET'])
def listar():
    with conectar() as conn:
        cur = conn.execute("SELECT * FROM usuarios")
        datos = [dict(row) for row in cur.fetchall()]
    return jsonify(datos)

@app.route('/actualizar', methods=['PUT'])
def actualizar():
    data = request.json
    codigo = data.get('codigo')
    if not codigo:
        return jsonify({'error': 'Código requerido.'}), 400
    with conectar() as conn:
        cur = conn.execute("""UPDATE usuarios
                              SET nombre=?, correo=?, telefono=?, carrera=?, materia=?
                              WHERE codigo=?""",
                              (data['nombre'], data['correo'], data['telefono'],
                               data['carrera'], data['materia'], codigo))
        if cur.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado.'}), 404
    return jsonify({'mensaje': 'Usuario actualizado correctamente.'})

@app.route('/eliminar/<int:codigo>', methods=['DELETE'])
def eliminar(codigo):
    with conectar() as conn:
        cur = conn.execute("DELETE FROM usuarios WHERE codigo=?", (codigo,))
        if cur.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado.'}), 404
    return jsonify({'mensaje': 'Usuario eliminado correctamente.'})

if __name__ == '__main__':
    app.run(debug=True)

