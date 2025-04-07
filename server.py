from flask import Flask, request, jsonify, render_template_string
import json
import subprocess

app = Flask(__name__)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BUSCAR PERSONA OFFLINE</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            max-width: 100%;
            margin: auto;
        }
        h2 {
            color: #333;
        }
        form {
            display: flex;
            gap: 7%;
        }
        input, button {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        #mensaje {
            margin-top: 10px;
            color: green;
            font-weight: bold;
            display: none;
        }
    </style>
    <script>
        function enviarDatos() {
            let apellidos_raw = document.getElementById("apellidos_raw").value;
            let nombre_raw = document.getElementById("nombre_raw").value;
            let cedula = document.getElementById("cedula").value;
            let fechaNacimiento_raw = document.getElementById("fechaNacimiento_raw").value;

            // Convertir fecha a formato DD/MM/YYYY
            if (fechaNacimiento_raw) {
                let partes = fechaNacimiento_raw.split("-");
                fechaNacimiento_raw = `${partes[2]}/${partes[1]}/${partes[0]}`;
            }

            fetch('/guardar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ apellidos_raw, nombre_raw, cedula, fechaNacimiento_raw })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "ok") {
                    alert("Búsqueda terminada");
                }
            })
            .catch(error => {
                console.error("Error al enviar datos:", error);
                alert("Error al intentar buscar datos.");
            });
        }

        function actualizarTabla() {
            fetch('/datos')
                .then(response => response.json())
                .then(data => {
                    let tabla = document.getElementById("tabla-datos");
                    tabla.innerHTML = "";
                    if (data.length === 0) {
                        let tr = document.createElement("tr");
                        tr.innerHTML = "<td colspan='4'>No hay datos disponibles / CARGANDO...</td>";
                        tabla.appendChild(tr);
                    } else {
                        data.forEach(fila => {
                            let tr = document.createElement("tr");
                            tr.innerHTML = `<td>${fila.apellidos_raw}</td><td>${fila.nombre_raw}</td><td>${fila.cedula}</td><td>${fila.fechaNacimiento_raw}</td><td>${fila.nroActa}</td><td>${fila.seccionJudicial}</td>`;
                            tabla.appendChild(tr);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error al obtener datos:", error);
                });
        } 

        // Actualizar la tabla cada 1 segundo
        setInterval(actualizarTabla, 1000);
    </script>
</head>
<body>
    <div class="container">
        <h2>BUSCAR PERSONA</h2>
        <form onsubmit="event.preventDefault(); enviarDatos();">
            <input type="text" placeholder="Apellidos" id="apellidos_raw">
            <input type="text" placeholder="Nombres" id="nombre_raw">
            <input type="text" placeholder="Cédula" id="cedula">
            <input type="date" placeholder="Fecha de Nacimiento" id="fechaNacimiento_raw">
            <button type="submit">BUSCAR</button>
        </form>
        <p id="mensaje"></p>
    </div>
    <div class="container">
        <h2>Resultados</h2>
        <table>
            <thead>
                <tr>
                    <th>Apellidos</th>
                    <th>Nombres</th>
                    <th>Cédula</th>
                    <th>Fecha de Nacimiento</th>
                    <th>Número de Acta</th>
                    <th>Sección Judicial</th>
                </tr>
            </thead>
            <tbody id="tabla-datos"></tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.get_json()

    try:
        with open("aapellido.txt", "w", encoding="utf-8") as f:
            f.write(datos.get("apellidos_raw", ""))
        with open("anombre.txt", "w", encoding="utf-8") as f:
            f.write(datos.get("nombre_raw", ""))
        with open("aci.txt", "w", encoding="utf-8") as f:
            f.write(datos.get("cedula", ""))
        with open("afecha.txt", "w", encoding="utf-8") as f:
            f.write(datos.get("fechaNacimiento_raw", ""))

        # Ejecutar el script externo
        subprocess.run(["python", "buscador.py"], check=True)

        return jsonify({"status": "ok"})
    except Exception as e:
        print("Error en /guardar:", e)
        return jsonify({"status": "error", "mensaje": str(e)}), 500

@app.route('/datos', methods=['GET'])
def obtener_datos():
    try:
        with open("aresultado.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        return jsonify(datos)
    except Exception as e:
        print("Error al leer el archivo de resultados:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
