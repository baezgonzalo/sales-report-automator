import csv

def precio_total(venta):
    return venta["precio"] * venta["cantidad"]

def total_ventas(ventas):
    total = 0
    for venta in ventas:
        total += precio_total(venta)
    return total

def total_producto(ventas, producto):
    total = 0
    for item in ventas:
        if item["producto"] == producto:
            total += item["precio"] * item["cantidad"]
    return total

def resumir_productos(ventas):
    resumen = {}
    for item in ventas:
        if item["producto"] not in resumen:
            resumen[item["producto"]] = {"unidades": 0, "importe": 0}
        resumen[item["producto"]]["unidades"] += item["cantidad"]
        resumen[item["producto"]]["importe"] += item["precio"] * item["cantidad"]
    return resumen

def mostrar_resumen(resumen):
    for producto in sorted(resumen):
        unidades = resumen[producto]["unidades"]
        importe = resumen[producto]["importe"]
        print(producto, unidades, importe)

def exportar_resumen(resumen, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["producto", "unidades", "importe"])
        total_unidades = 0
        total_importe = 0
        for producto in sorted(resumen):
            total_unidades += resumen[producto]["unidades"]
            total_importe += resumen[producto]["importe"]

            escritor.writerow([
            producto,
            resumen[producto]["unidades"],
            resumen[producto]["importe"]
            ])
        escritor.writerow(["TOTAL", total_unidades, total_importe])

def leer_ventas(ruta):
    ventas = []
    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila["precio"] = float(fila["precio"])
            fila["cantidad"] = int(fila["cantidad"])
            ventas.append(fila)
    return ventas

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
    mayor_producto = None
    mayor_importe = 0
    for producto in resumen:
        ingreso = resumen[producto]["importe"]
        if mayor_producto is None or ingreso > mayor_importe:
            mayor_producto = producto
            mayor_importe = ingreso
    if mayor_producto is None:
        return "Aún no tienes productos vendidos."
    return f"{mayor_producto}: ${mayor_importe}"


ruta_entrada = input("Nombre del archivo de ventas: ").strip()
try:
    ventas = leer_ventas(ruta_entrada)
except FileNotFoundError:
    print(f"No encontré el archivo: {ruta_entrada}")
    raise SystemExit(1)
resumen = resumir_productos(ventas)
ruta_salida = input("Nombre del archivo de reporte: ")
if ruta_salida == ruta_entrada:
    print("El reporte debe tener un nombre distinto al archivo de ventas.")
else:
    exportar_resumen(resumen, ruta_salida)
    
print(mayor_ingreso(resumen))
