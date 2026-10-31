import csv
import math
from pathlib import Path


def precio_total(venta):
    return venta["precio"] * venta["cantidad"]


def total_ventas(ventas):
    return sum(precio_total(venta) for venta in ventas)


def total_producto(ventas, producto):
    return sum(precio_total(venta) for venta in ventas if venta["producto"] == producto)


def resumir_productos(ventas):
    resumen = {}
    for venta in ventas:
        producto = venta["producto"]
        if producto not in resumen:
            resumen[producto] = {"unidades": 0, "importe": 0}
        resumen[producto]["unidades"] += venta["cantidad"]
        resumen[producto]["importe"] += precio_total(venta)
    return resumen


def porcentaje_ingresos_por_producto(resumen):
    total_importe = sum(datos["importe"] for datos in resumen.values())
    porcentajes = {}
    for producto, datos in resumen.items():
        porcentajes[producto] = datos["importe"] / total_importe * 100 if total_importe else 0
    return porcentajes


def ingreso_promedio_por_unidad(resumen):
    total_unidades = sum(datos["unidades"] for datos in resumen.values())
    total_importe = sum(datos["importe"] for datos in resumen.values())
    return total_importe / total_unidades if total_unidades else 0


def mostrar_resumen(resumen):
    if not resumen:
        print("No hay ventas para resumir.")
        return
    porcentajes = porcentaje_ingresos_por_producto(resumen)
    print("\nProducto | Unidades | Importe | % de ingresos")
    for producto in sorted(resumen):
        datos = resumen[producto]
        print(
            f"{producto} | {datos['unidades']} | "
            f"${datos['importe']:.2f} | {porcentajes[producto]:.2f}%"
        )


def escribir_resumen_csv(resumen, archivo):
    porcentajes = porcentaje_ingresos_por_producto(resumen)
    total_unidades = sum(datos["unidades"] for datos in resumen.values())
    total_importe = sum(datos["importe"] for datos in resumen.values())
    escritor = csv.writer(archivo)
    escritor.writerow(["producto", "unidades", "importe", "porcentaje"])
    for producto in sorted(resumen):
        datos = resumen[producto]
        escritor.writerow(
            [producto, datos["unidades"], f"{datos['importe']:.2f}", f"{porcentajes[producto]:.2f}"]
        )
    escritor.writerow(
        ["TOTAL", total_unidades, f"{total_importe:.2f}", "100.00" if total_importe else "0.00"]
    )


def exportar_resumen(resumen, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escribir_resumen_csv(resumen, archivo)


def procesar_ventas_csv(archivo):
    ventas = []
    lector = csv.DictReader(archivo)
    if lector.fieldnames is None:
        raise ValueError("El archivo CSV está vacío.")
    faltantes = {"producto", "cantidad", "precio"} - set(lector.fieldnames)
    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {', '.join(sorted(faltantes))}.")
    for numero_fila, fila in enumerate(lector, start=2):
        if None in fila:
            raise ValueError(f"Fila {numero_fila}: hay más valores que columnas.")
        producto = (fila["producto"] or "").strip()
        if not producto:
            raise ValueError(f"Fila {numero_fila}: falta el producto.")
        try:
            cantidad = int((fila["cantidad"] or "").strip())
            precio = float((fila["precio"] or "").strip())
        except ValueError as error:
            raise ValueError(f"Fila {numero_fila}: cantidad o precio inválido.") from error
        if cantidad < 0 or precio < 0 or not math.isfinite(precio):
            raise ValueError(f"Fila {numero_fila}: cantidad y precio deben ser números no negativos.")
        ventas.append({"producto": producto, "cantidad": cantidad, "precio": precio})
    return ventas


def leer_ventas(ruta):
    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        return procesar_ventas_csv(archivo)


def mas_vendido(resumen):
    mayor_producto = None
    mayor_unidades = 0
    for producto in resumen:
        unidades = resumen[producto]["unidades"]
        if mayor_producto is None or unidades > mayor_unidades:
            mayor_producto = producto
            mayor_unidades = unidades
    if mayor_producto is None:
        return "Aún no tienes productos vendidos."
    return f"{mayor_producto}: {mayor_unidades} unidades"


def mayor_ingreso(resumen):
    ranking = productos_con_mayor_ingreso(resumen, limite=1)
    if not ranking:
        return "Aún no tienes productos vendidos."
    producto, importe = ranking[0]
    return f"{producto}: ${importe:.2f}"


def productos_con_mayor_ingreso(resumen, limite=3):
    if limite <= 0:
        return []
    ordenados = sorted(resumen, key=lambda producto: (-resumen[producto]["importe"], producto))
    return [(producto, resumen[producto]["importe"]) for producto in ordenados[:limite]]


def ruta_en_proyecto(nombre):
    ruta = Path(nombre)
    return ruta if ruta.is_absolute() else Path(__file__).resolve().parent / ruta


def main():
    nombre_entrada = input("Archivo de ventas [ventas.csv]: ").strip() or "ventas.csv"
    nombre_salida = input("Archivo de reporte [reporte_ventas.csv]: ").strip() or "reporte_ventas.csv"
    ruta_entrada = ruta_en_proyecto(nombre_entrada)
    ruta_salida = ruta_en_proyecto(nombre_salida)
    try:
        if ruta_entrada.resolve() == ruta_salida.resolve():
            raise ValueError("El reporte debe tener un nombre distinto al archivo de ventas.")
        ventas = leer_ventas(ruta_entrada)
        resumen = resumir_productos(ventas)
        exportar_resumen(resumen, ruta_salida)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}")
        return 1
    total_unidades = sum(datos["unidades"] for datos in resumen.values())
    total_importe = sum(datos["importe"] for datos in resumen.values())
    print(f"\nReporte guardado en: {ruta_salida}")
    mostrar_resumen(resumen)
    print(f"\nTotal: {total_unidades} unidades y ${total_importe:.2f}")
    print(f"Ingreso promedio por unidad: ${ingreso_promedio_por_unidad(resumen):.2f}")
    print(f"Más vendido por unidades: {mas_vendido(resumen)}")
    print(f"Mayor ingreso: {mayor_ingreso(resumen)}")
    if resumen:
        print("Productos con mayor ingreso:")
        for posicion, (producto, importe) in enumerate(productos_con_mayor_ingreso(resumen), start=1):
            print(f"  {posicion}. {producto}: ${importe:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
