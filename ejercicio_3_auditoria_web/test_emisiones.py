import unittest
from emisiones import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    def test_valor_nominal_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250, 0.5), 125.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_decimales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)


class TestMetricas(unittest.TestCase):
    def test_total_y_planta_mayor(self):
        datos = [
            {"planta": "Norte", "consumo_kwh": 100},
            {"planta": "Sur", "consumo_kwh": 300},
        ]
        r = obtener_metricas_consumo(datos)
        self.assertAlmostEqual(r["total_emisiones"], 160.0)
        self.assertEqual(r["planta_mayor_consumo"], "Sur")


if __name__ == "__main__":
    unittest.main()
