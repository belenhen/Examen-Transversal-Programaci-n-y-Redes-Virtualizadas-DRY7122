from flask import Flask, request, jsonify
from passlib.hash import sha256_crypt
import sqlite3

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Clave secreta para sesiones

# Configuración de la base de datos SQLite
DATABASE = 'usuarios.db'

def crear_tabla_usuarios():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Crear la tabla de usuarios al iniciar la aplicación
crear_tabla_usuarios()

# Ruta para almacenar usuarios y contraseñas en hash
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data['nombre']
    password = sha256_crypt.encrypt(data['password'])

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, password) VALUES (?, ?)', (nombre, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuario registrado correctamente'})

# Ruta para validar usuarios
@app.route('/validar', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    nombre = data['nombre']
    password_plano = data['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        hash_password = usuario[2]
        if sha256_crypt.verify(password_plano, hash_password):
            return jsonify({'message': 'Acceso concedido'})
    
    return jsonify({'message': 'Acceso denegado'})

# Ruta de prueba para mostrar todos los usuarios en la base de datos
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, password FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()

    return jsonify({'usuarios': usuarios})

# Iniciar la aplicación Flask en el puerto 5800
if __name__ == '__main__':
    app.run(port=5800, debug=True)
