# Cumplimiento de requisitos del proyecto

## Principios SOLID

- **Single Responsibility Principle (SRP):** Cada clase tiene una única responsabilidad.
  - `Empleado` define la interfaz base.
  - `EmpleadoAsalariado`, `EmpleadoPorHoras`, `EmpleadoPorComision`, y `EmpleadoTemporal` implementan sus reglas de cálculo específicas.
  - `Nomina` se encarga únicamente de agrupar empleados y generar reportes.
  - `NominaApp` se encarga de la interfaz gráfica.

- **Open/Closed Principle (OCP):** El sistema está abierto para extensión y cerrado para modificación.
  - Se pueden agregar nuevos tipos de empleados creando nuevas subclases de `Empleado` sin modificar las clases existentes.

- **Liskov Substitution Principle (LSP):** Todas las subclases de `Empleado` pueden ser usadas donde se espera un `Empleado`.
  - `Nomina` trabaja con instancias de `Empleado` de forma genérica.

- **Interface Segregation Principle (ISP):** No existe una interfaz demasiado amplia.
  - Cada empleado implementa solo los métodos necesarios para su cálculo de salario.

- **Dependency Inversion Principle (DIP):** `Nomina` depende de la abstracción `Empleado`, no de implementaciones concretas.

## Código limpio y buenas prácticas

- Nombres descriptivos para variables, métodos y clases.
- Separación clara entre la lógica de negocio y la interfaz de usuario.
- Estructura modular con clases y funciones cortas.
- Manejo de excepciones específico mediante `EmpleadoError`.
- Validaciones explícitas de entrada para evitar valores inválidos.

## Refactorización

- Se extrajo la lógica de cálculo de nómina en clases separadas.
- Se reutilizan propiedades como `salario_bruto`, `bonos`, `beneficios_adicionales` y `deducciones`.
- La aplicación gráfica está desacoplada de los cálculos.

## Comentarios de código

- El código contiene comentarios explicativos en puntos clave, como las tasas de deducción y la estructura de clases.
- Las funciones y clases tienen nombres autoexplicativos, lo que facilita la lectura sin necesidad de comentarios excesivos.

## Pruebas unitarias

- Se agregó el archivo `tests/test_empleados.py` con casos de prueba para:
  - Cálculo de salario bruto y neto según el tipo de empleado.
  - Aplicación de bonos y beneficios.
  - Validaciones de datos inválidos.
  - Generación de reporte.

## Metodología de desarrollo de software

1. **Análisis de requisitos:** Se identificaron las reglas de negocio y las validaciones obligatorias.
2. **Diseño orientado a objetos:** Se definieron las clases base y las subclases especializadas.
3. **Implementación incremental:** Primero se construyó la lógica de negocio y luego se añadió la interfaz gráfica.
4. **Pruebas:** Se añadieron pruebas unitarias para validar el comportamiento de cada tipo de empleado.
5. **Generación del ejecutable:** Se utilizó PyInstaller para crear el archivo `dist/empleados.exe`.

## Conclusión

El sistema cumple con los requisitos de uso de POO, reglas de negocio, validaciones, interfaz gráfica ejecutable y pruebas unitarias. Además, la estructura se diseñó según principios SOLID y buenas prácticas de código.
