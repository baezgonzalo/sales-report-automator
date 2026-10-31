import base64
import io
import unittest

from web import app


class WebTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def test_carga_y_descarga(self):
        respuesta = self.cliente.post(
            "/",
            data={"archivo": (io.BytesIO(b"producto,cantidad,precio\nCuaderno,2,1500\n"), "ventas.csv")},
        )
        self.assertEqual(respuesta.status_code, 200)
        pagina = respuesta.get_data(as_text=True)
        self.assertIn("Cuaderno", pagina)
        self.assertIn("3000.00", pagina)
        marcador = "data:text/csv;base64,"
        self.assertIn(marcador, pagina)
        contenido = pagina.split(marcador, 1)[1].split('"', 1)[0]
        reporte = base64.b64decode(contenido).decode("utf-8-sig")
        self.assertIn("Cuaderno,2,3000.00,100.00", reporte)

    def test_csv_invalido_muestra_error(self):
        respuesta = self.cliente.post(
            "/",
            data={"archivo": (io.BytesIO(b"producto,cantidad,precio\nCuaderno,dos,1500\n"), "ventas.csv")},
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("Fila 2", respuesta.get_data(as_text=True))

    def test_ejemplo(self):
        respuesta = self.cliente.get("/ejemplo")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("23802.00", respuesta.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
