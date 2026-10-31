Sales Report Automator

Script en Python que lee ventas desde un CSV y genera un reporte agrupado por producto. Muestra unidades vendidas, importe, participación en los ingresos, productos destacados e ingreso promedio por unidad.

## Datos de entrada

El archivo CSV debe tener estas columnas:

```csv
producto,cantidad,precio
Cuaderno,2,1500
Lapicera,3,500
```

`cantidad` debe ser un número entero no negativo y `precio` un número no negativo. Cada fila representa una venta de un producto. El script indica la fila cuando encuentra un dato inválido.

## Ejecutar

Necesitás Python 3. No hay dependencias externas.

```powershell
python main.py
```

Presioná **Enter** en las dos preguntas para usar `ventas.csv` como entrada y `reporte_ventas.csv` como salida. También podés escribir otros nombres o rutas. Las rutas relativas se buscan en la carpeta del proyecto.

El reporte contiene las columnas `producto`, `unidades`, `importe` y `porcentaje`, más una fila `TOTAL`. Los porcentajes están en escala de 0 a 100. Al volver a usar el mismo nombre de salida, el reporte anterior se reemplaza; el programa impide usar el archivo de entrada como salida.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```
