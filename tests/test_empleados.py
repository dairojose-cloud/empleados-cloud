import unittest

from empleados import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoPorComision,
    EmpleadoTemporal,
    EmpleadoError,
    Nomina,
)


class TestNominaSistema(unittest.TestCase):
    def test_empleado_asalariado_bono_antiguedad(self):
        empleado = EmpleadoAsalariado(
            nombre="Juan",
            cedula="123",
            años_servicio=6,
            salario_fijo=2_000_000,
        )
        self.assertEqual(empleado.salario_bruto, 2_000_000)
        self.assertEqual(empleado.bonos, 200_000)
        self.assertGreater(empleado.salario_neto, 0)

    def test_empleado_asalariado_sin_bono(self):
        empleado = EmpleadoAsalariado(
            nombre="Ana",
            cedula="124",
            años_servicio=4,
            salario_fijo=2_000_000,
        )
        self.assertEqual(empleado.bonos, 0.0)

    def test_empleado_por_horas_con_horas_extra_y_fondo(self):
        empleado = EmpleadoPorHoras(
            nombre="Luis",
            cedula="125",
            años_servicio=2,
            tarifa_hora=25_000,
            horas_trabajadas=45,
            acepta_fondo_ahorro=True,
        )
        self.assertEqual(empleado.salario_bruto, 40 * 25_000 + 5 * 37_500)
        self.assertGreater(empleado.beneficios_adicionales, 0)
        self.assertGreater(empleado.salario_neto, 0)

    def test_empleado_por_comision_gana_bono_por_ventas(self):
        empleado = EmpleadoPorComision(
            nombre="Carla",
            cedula="126",
            años_servicio=3,
            salario_base=1_000_000,
            porcentaje_comision=0.10,
            ventas=25_000_000,
        )
        self.assertEqual(empleado.comision, 2_500_000)
        self.assertEqual(empleado.bonos, 750_000)
        self.assertGreater(empleado.salario_neto, 0)

    def test_empleado_temporal_sin_bonos(self):
        empleado = EmpleadoTemporal(
            nombre="María",
            cedula="127",
            años_servicio=1,
            salario_fijo=1_500_000,
            duracion_meses=3,
        )
        self.assertEqual(empleado.salario_bruto, 1_500_000)
        self.assertEqual(empleado.bonos, 0.0)
        self.assertEqual(empleado.beneficios_adicionales, 0.0)

    def test_validacion_horas_negativas(self):
        with self.assertRaises(EmpleadoError):
            EmpleadoPorHoras(
                nombre="Pablo",
                cedula="128",
                años_servicio=1,
                tarifa_hora=20_000,
                horas_trabajadas=-5,
            )

    def test_validacion_ventas_negativas(self):
        with self.assertRaises(EmpleadoError):
            EmpleadoPorComision(
                nombre="Marta",
                cedula="129",
                años_servicio=1,
                salario_base=1_000_000,
                porcentaje_comision=0.10,
                ventas=-10_000,
            )

    def test_nomina_total(self):
        empleados = [
            EmpleadoAsalariado(
                nombre="Ana",
                cedula="130",
                años_servicio=6,
                salario_fijo=3_000_000,
            ),
            EmpleadoPorHoras(
                nombre="Luis",
                cedula="131",
                años_servicio=2,
                tarifa_hora=30_000,
                horas_trabajadas=42,
                acepta_fondo_ahorro=False,
            ),
        ]
        nomina = Nomina(empleados)
        total = sum(e.salario_neto for e in empleados)
        self.assertAlmostEqual(nomina.total_nomina(), total)

    def test_reporte_contiene_nombre(self):
        empleados = [
            EmpleadoAsalariado(
                nombre="Lucía",
                cedula="132",
                años_servicio=7,
                salario_fijo=4_000_000,
            )
        ]
        nomina = Nomina(empleados)
        reporte = nomina.reporte()
        self.assertIn("Lucía", reporte)
        self.assertIn("Salario bruto", reporte)


if __name__ == "__main__":
    unittest.main()
