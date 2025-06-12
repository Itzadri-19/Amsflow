from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests

app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)

# Conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="amsflow"
    )

# DeepSeek AI
deepseek_api_key = "sk-19b02618d173451a83b33d6c208d4a51"
TEXT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
deepseek_headers = {
    "Authorization": f"Bearer {deepseek_api_key}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contraseña = data.get("contrasegna")

    if not correo or not contraseña:
        return jsonify({"success": False, "error": "Faltan datos"}), 400

    try:
        conexion = get_connection()  # <-- Línea faltante
        cursor = conexion.cursor(buffered=True)
        cursor.execute("SELECT NombreApellidos FROM usuarios WHERE correo=%s AND contrasegna=%s", (correo, contraseña))
        resultado = cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()

    if resultado:
        nombre_usuario = resultado[0]
        return jsonify({"success": True, "nombre": nombre_usuario})
    else:
        return jsonify({"success": False, "error": "Credenciales incorrectas"}), 401

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400

    try:
        response = requests.post(
            TEXT_ENDPOINT,
            headers=deepseek_headers,
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Responde siempre en español. Te llamas AmsMind. Si te preguntan tu nombre o identidad, di que eres AmsMind."},
                    {"role": "user", "content": message}
                ]
            }
        )

        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": f"Error generando respuesta de texto: {response.status_code} - {response.text}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error generando respuesta de texto: {str(e)}"}), 500

@app.route("/api/finanzas", methods=["GET"])
def obtener_finanzas():
    conexion = get_connection()
    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT SUM(total) FROM ventas")
        ingresos = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(p.precio_coste * dv.cantidad)
            FROM detalles_venta dv
            JOIN productos p ON dv.id_producto = p.id_producto
        """)
        gastos = cursor.fetchone()[0] or 0

        beneficio = ingresos - gastos
        margen_beneficio = (beneficio / ingresos * 100) if ingresos > 0 else 0

        cursor.close()
        conexion.close()

        return jsonify({
            "ingresos": round(ingresos, 2),
            "gastos": round(gastos, 2),
            "beneficio": round(beneficio, 2),
            "margen_beneficio": round(margen_beneficio, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tabla_productos", methods=["GET"])
def obtener_tabla_productos():
    conexion = get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        id_categoria = request.args.get("categoria")

        if id_categoria:
            cursor.execute("""
                SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, c.nombre AS categoria
                FROM productos p
                JOIN categorias_productos c ON p.id_categoria = c.id_categoria
                WHERE p.id_categoria = %s
            """, (id_categoria,))
        else:
            cursor.execute("""
                SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, c.nombre AS categoria
                FROM productos p
                JOIN categorias_productos c ON p.id_categoria = c.id_categoria
            """)

        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(productos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ventas', methods=['GET'])
def obtener_ventas():
    conexion = get_connection()
    try:
        cur = conexion.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                v.id_venta,
                v.fecha,
                c.nombre AS cliente,
                e.nombre AS empleado,
                SUM(dv.cantidad * dv.precio_unitario) AS total
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN empleados e ON v.id_empleado = e.id_empleado
            JOIN detalles_venta dv ON v.id_venta = dv.id_venta
            GROUP BY v.id_venta
            ORDER BY v.fecha DESC
        """)
        ventas = cur.fetchall()
        cur.close()
        conexion.close()
        return jsonify(ventas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ventas/detalles', methods=['GET'])
def obtener_detalles_venta():
    id_venta = request.args.get('id')
    conexion = get_connection()
    try:
        cur = conexion.cursor(dictionary=True)
        cur.execute("""
            SELECT 
                p.nombre AS producto,
                dv.cantidad,
                dv.precio_unitario,
                (dv.cantidad * dv.precio_unitario) AS subtotal
            FROM detalles_venta dv
            JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = %s
        """, (id_venta,))
        detalles = cur.fetchall()
        cur.close()
        conexion.close()
        return jsonify(detalles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from datetime import datetime

@app.route('/api/comprar', methods=['POST'])
def comprar_producto():
    data = request.get_json()
    id_producto = data.get("id_producto")
    cantidad = data.get("cantidad")
    id_cliente = data.get("id_cliente", 1)     # Por defecto cliente 1
    id_empleado = data.get("id_empleado", 1)   # Por defecto empleado 1

    if not id_producto or not cantidad:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        cantidad = int(cantidad)
    except ValueError:
        return jsonify({"error": "Cantidad no válida"}), 400

    conexion = get_connection()
    try:
        cursor = conexion.cursor()

        # Verificar stock disponible
        cursor.execute("SELECT stock, precio FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        stock_actual, precio_unitario = producto
        if cantidad > stock_actual:
            return jsonify({"error": "Stock insuficiente"}), 400

        # Crear la venta
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total = cantidad * precio_unitario
        cursor.execute("""
            INSERT INTO ventas (fecha, total, id_cliente, id_empleado)
            VALUES (%s, %s, %s, %s)
        """, (fecha, total, id_cliente, id_empleado))
        id_venta = cursor.lastrowid

        # Insertar el detalle de la venta
        cursor.execute("""
            INSERT INTO detalles_venta (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_venta, id_producto, cantidad, precio_unitario))

        # Actualizar el stock
        cursor.execute("""
            UPDATE productos SET stock = stock - %s WHERE id_producto = %s
        """, (cantidad, id_producto))

        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({"success": True, "mensaje": "Compra realizada correctamente", "id_venta": id_venta})

    except Exception as e:
        conexion.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/compras")
def compras():
    return render_template("compras.html")


@app.route("/api/clientes", methods=["GET"])
def obtener_clientes():
    conexion = get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_cliente, nombre FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/datos_formulario", methods=["GET"])
def obtener_empleados():
    conexion = get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_empleado, nombre FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(empleados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
