import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class ReporteVentasTests(unittest.TestCase):
    def test_resumen_reporte_y_promedio(self):
        ventas = [
            {"producto": "A", "cantidad": 2, "precio": 10.0},
            {"producto": "B", "cantidad": 1, "precio": 20.0},
            {"producto": "A", "cantidad": 1, "precio": 20.0},
        ]
        resumen = main.resumir_productos(ventas)
        self.assertEqual(resumen["A"], {"unidades": 3, "importe": 40.0})
        self.assertEqual(main.ingreso_promedio_por_unidad(resumen), 15.0)
        self.assertEqual(main.productos_con_mayor_ingreso(resumen), [("A", 40.0), ("B", 20.0)])

        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            salida = Path(carpeta) / "reporte.csv"
            main.exportar_resumen(resumen, salida)
            with salida.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
        self.assertEqual(filas[0], {"producto": "A", "unidades": "3", "importe": "40.00", "porcentaje": "66.67"})
        self.assertEqual(filas[-1], {"producto": "TOTAL", "unidades": "4", "importe": "60.00", "porcentaje": "100.00"})

    def test_csv_invalido_indica_fila(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            entrada = Path(carpeta) / "ventas.csv"
            entrada.write_text("producto,cantidad,precio\nCuaderno,dos,10\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Fila 2"):
                main.leer_ventas(entrada)

    def test_no_sobrescribe_entrada_con_ruta_equivalente(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            entrada = Path(carpeta) / "ventas.csv"
            contenido = "producto,cantidad,precio\nCuaderno,1,10\n"
            entrada.write_text(contenido, encoding="utf-8")
            ruta_equivalente = str(Path(carpeta)) + r"\.\ventas.csv"
            self.assertNotEqual(str(entrada), ruta_equivalente)
            with patch("builtins.input", side_effect=[str(entrada), ruta_equivalente]):
                with redirect_stdout(io.StringIO()):
                    resultado = main.main()
            self.assertEqual(resultado, 1)
            self.assertEqual(entrada.read_text(encoding="utf-8"), contenido)

    def test_sin_ventas(self):
        self.assertEqual(main.ingreso_promedio_por_unidad({}), 0)
        self.assertEqual(main.productos_con_mayor_ingreso({}), [])
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as carpeta:
            salida = Path(carpeta) / "reporte.csv"
            main.exportar_resumen({}, salida)
            with salida.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
        self.assertEqual(filas, [{"producto": "TOTAL", "unidades": "0", "importe": "0.00", "porcentaje": "0.00"}])


if __name__ == "__main__":
    unittest.main()
