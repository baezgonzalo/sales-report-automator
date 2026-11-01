Sales Report Automator

Script en Python que lee ventas desde un CSV y genera un reporte agrupado por producto. Muestra unidades vendidas, importe, participación en los ingresos, productos destacados e ingreso promedio por unidad.

## Datos de entrada

El archivo CSV debe tener estas columnas:

```csv
producto,cantidad,precio
```

`cantidad` debe ser un número entero no negativo y `precio` un número no negativo. Cada fila representa una venta de un producto. El script indica la fila cuando encuentra un dato inválido.

## Ejecutar

Necesitás Python 3. No hay dependencias externas.

```powershell
python main.py
```

Presioná **Enter** en las dos preguntas para usar `ventas.csv` como entrada y `reporte_ventas.csv` como salida. También podés escribir otros nombres o rutas. Las rutas relativas se buscan en la carpeta del proyecto.

El reporte contiene las columnas `producto`, `unidades`, `importe` y `porcentaje`, más una fila `TOTAL`. Los porcentajes están en escala de 0 a 100. Al volver a usar el mismo nombre de salida, el reporte anterior se reemplaza; el programa impide usar el archivo de entrada como salida.

## Usar la página web local

Instalá Flask una sola vez:

```powershell
python -m pip install -r requirements.txt
```

Después iniciá la página:

```powershell
python web.py
```

Abrí `http://127.0.0.1:5000` en el navegador. Elegí un archivo CSV: la página lo procesa automáticamente y muestra las métricas, la tabla y un botón para descargar el reporte. El botón **Generar resumen** permite enviar el archivo manualmente si el navegador no ejecuta JavaScript. El archivo cargado se procesa en memoria y no se guarda en el proyecto. También podés probar **Ver datos de ejemplo** con `ventas.csv`.

La página funciona en tu computadora. Para compartirla por internet haría falta elegir dónde publicarla.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```
