from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests

app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="amsflow"
)

# DeepSeek
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
        cursor = conexion.cursor(buffered=True)
        cursor.execute("SELECT NombreApellidos FROM usuarios WHERE correo=%s AND contrasegna=%s", (correo, contraseña))
        resultado = cursor.fetchone()
    finally:
        cursor.close()

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

# ==============================================
#              RUTAS DE API AJUSTADAS
# ==============================================

@app.route("/api/finanzas")
def api_finanzas():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            MONTH(v.fecha) AS mes,
            SUM(dv.cantidad * dv.precio_unitario) AS ingresos,
            SUM(p.precio_coste * dv.cantidad) AS gastos
        FROM ventas v
        JOIN detalles_venta dv ON v.id_venta = dv.id_venta
        JOIN productos p ON dv.id_producto = p.id_producto
        GROUP BY mes
        ORDER BY mes
    """)
    resultados = cursor.fetchall()
    cursor.close()

    meses = []
    ingresos = []
    gastos = []
    beneficio_neto = []
    margen_beneficio = []

    for mes, ingreso, gasto in resultados:
        beneficio = ingreso - gasto
        margen = round((beneficio / ingreso) * 100, 2) if ingreso > 0 else 0

        meses.append(f"Mes {mes}")
        ingresos.append(round(ingreso, 2))
        gastos.append(round(gasto, 2))
        beneficio_neto.append(round(beneficio, 2))
        margen_beneficio.append(margen)

    return jsonify({
        "meses": meses,
        "ingresos": ingresos,
        "gastos": gastos,
        "beneficio_neto": beneficio_neto,
        "margen_beneficio": margen_beneficio
    })

@app.route("/api/productos")
def api_productos():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.nombre, SUM(dv.cantidad) AS total
        FROM detalles_venta dv
        JOIN productos p ON dv.id_producto = p.id_producto
        GROUP BY p.id_producto
        ORDER BY total DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()

    labels = [r[0] for r in resultados]
    valores = [int(r[1]) for r in resultados]

    return jsonify({
        "labels": labels,
        "valores": valores
    })

@app.route("/api/clientes")
def api_clientes():
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            MONTH(fecha) AS mes, 
            COUNT(DISTINCT id_cliente) AS nuevos 
        FROM ventas 
        GROUP BY mes 
        ORDER BY mes
    """)
    nuevos_mes = cursor.fetchall()

    cursor.execute("""
        SELECT 
            MONTH(v.fecha) AS mes, 
            COUNT(DISTINCT v.id_cliente) AS recurrentes,
            AVG(dv.cantidad * dv.precio_unitario) AS ticket_medio
        FROM ventas v
        JOIN detalles_venta dv ON v.id_venta = dv.id_venta
        GROUP BY mes
        ORDER BY mes
    """)
    datos_extra = cursor.fetchall()
    cursor.close()

    meses = [f"Mes {m[0]}" for m in nuevos_mes]
    nuevos = [m[1] for m in nuevos_mes]
    recurrentes = [d[1] for d in datos_extra]
    ticket_medio = [round(d[2], 2) if d[2] else 0 for d in datos_extra]

    return jsonify({
        "meses": meses,
        "nuevos": nuevos,
        "recurrentes": recurrentes,
        "ticket_medio": ticket_medio
    })

@app.route("/api/ventas")
def api_ventas():
    cursor = conexion.cursor()

    # Categoría más vendida
    cursor.execute("""
        SELECT c.nombre, SUM(dv.cantidad) AS total 
        FROM detalles_venta dv
        JOIN productos p ON dv.id_producto = p.id_producto
        JOIN categorias_productos c ON p.id_categoria = c.id
        GROUP BY c.id 
        ORDER BY total DESC 
        LIMIT 4
    """)
    categorias = cursor.fetchall()
    nombres_categoria = [c[0] for c in categorias]
    cantidades_categoria = [c[1] for c in categorias]

    # Producto más vendido
    cursor.execute("""
        SELECT p.nombre, MONTH(v.fecha) AS mes, SUM(dv.cantidad) AS total
        FROM detalles_venta dv
        JOIN productos p ON dv.id_producto = p.id_producto
        JOIN ventas v ON dv.id_venta = v.id_venta
        GROUP BY p.id_producto, mes
        ORDER BY total DESC
        LIMIT 1
    """)
    producto, _, _ = cursor.fetchone()

    # Estacionalidad del producto más vendido
    cursor.execute("""
        SELECT MONTH(v.fecha) AS mes, SUM(dv.cantidad) AS total
        FROM detalles_venta dv
        JOIN productos p ON dv.id_producto = p.id_producto
        JOIN ventas v ON dv.id_venta = v.id_venta
        WHERE p.nombre = %s
        GROUP BY mes
        ORDER BY mes
    """, (producto,))
    estacionalidad = cursor.fetchall()
    cursor.close()

    meses = [f"Mes {m[0]}" for m in estacionalidad]
    demanda = [m[1] for m in estacionalidad]

    return jsonify({
        "categorias": nombres_categoria,
        "valores": cantidades_categoria,
        "producto": producto,
        "meses": meses,
        "demanda": demanda
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
