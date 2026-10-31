import base64
import csv
import io
from pathlib import Path

from flask import Flask, render_template, request

from main import (
    escribir_resumen_csv,
    ingreso_promedio_por_unidad,
    leer_ventas,
    mas_vendido,
    mayor_ingreso,
    porcentaje_ingresos_por_producto,
    procesar_ventas_csv,
    productos_con_mayor_ingreso,
    resumir_productos,
)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


def preparar_resultado(ventas, nombre_archivo):
    resumen = resumir_productos(ventas)
    porcentajes = porcentaje_ingresos_por_producto(resumen)
    total_unidades = sum(datos["unidades"] for datos in resumen.values())
    total_importe = sum(datos["importe"] for datos in resumen.values())
    filas = [
        {
            "producto": producto,
            "unidades": resumen[producto]["unidades"],
            "importe": f"{resumen[producto]['importe']:.2f}",
            "porcentaje": f"{porcentajes[producto]:.2f}",
            "barra": round(porcentajes[producto], 2),
        }
        for producto in sorted(resumen)
    ]

    archivo_salida = io.StringIO(newline="")
    escribir_resumen_csv(resumen, archivo_salida)
    descarga = base64.b64encode(archivo_salida.getvalue().encode("utf-8-sig")).decode("ascii")

    return {
        "nombre_archivo": nombre_archivo,
        "productos": len(resumen),
        "total_unidades": total_unidades,
        "total_importe": f"{total_importe:.2f}",
        "promedio": f"{ingreso_promedio_por_unidad(resumen):.2f}",
        "mas_vendido": mas_vendido(resumen),
        "mayor_ingreso": mayor_ingreso(resumen),
        "ranking": [(producto, f"{importe:.2f}") for producto, importe in productos_con_mayor_ingreso(resumen)],
        "filas": filas,
        "descarga_url": f"data:text/csv;base64,{descarga}",
    }


@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "GET":
        return render_template("index.html")

    archivo = request.files.get("archivo")
    if archivo is None or not archivo.filename:
        return render_template("index.html", error="Elegí un archivo CSV para continuar."), 400

    try:
        with io.TextIOWrapper(archivo.stream, encoding="utf-8-sig", newline="") as entrada:
            ventas = procesar_ventas_csv(entrada)
    except (UnicodeError, ValueError, csv.Error) as error:
        return render_template("index.html", error=f"No pude leer el CSV: {error}"), 400

    return render_template("index.html", resultado=preparar_resultado(ventas, archivo.filename))


@app.get("/ejemplo")
def ejemplo():
    try:
        ventas = leer_ventas(Path(__file__).with_name("ventas.csv"))
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        return render_template("index.html", error=f"No pude abrir el ejemplo: {error}"), 400
    return render_template("index.html", resultado=preparar_resultado(ventas, "ventas.csv · ejemplo"))


@app.errorhandler(413)
def archivo_demasiado_grande(_error):
    return render_template("index.html", error="El archivo supera el límite de 1 MB."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
