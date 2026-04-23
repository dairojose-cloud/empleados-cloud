# Sistema de Nómina - Proyecto de Programación Orientada a Objetos

Este proyecto implementa un sistema de nómina para una empresa que maneja distintos tipos de empleados, cada uno con su propia forma de calcular salario, beneficios y deducciones.

## Funcionalidades

- Tipos de empleados:
  - Empleado Asalariado
  - Empleado por Horas
  - Empleado por Comisión
  - Empleado Temporal
- Cálculo de salario bruto y neto
- Aplicación de bonos y beneficios según reglas de negocio
- Deducciones obligatorias: seguridad social, pensión y ARL
- Interfaz gráfica con `tkinter`
- Generación de reporte en pantalla
- Ejecutable `.exe` generado con PyInstaller

## Requisitos

- Python 3.14
- Entorno virtual preferido
- Paquete: `pyinstaller`

## Uso

1. Abre una terminal en la carpeta `empleados`.
2. Activa el entorno virtual si aplica.
3. Ejecuta el programa con:

```powershell
python empleados.py
```

4. Se abrirá una ventana donde podrás:
  - agregar empleados de cada tipo
  - cargar empleados de ejemplo
  - generar el reporte de nómina

## Ejecutable

El ejecutable generado con PyInstaller se encuentra en:

- `dist/empleados.exe`

Puedes ejecutar ese archivo directamente en Windows.

## Pruebas unitarias

El proyecto incluye pruebas unitarias en `tests/test_empleados.py`.

Para ejecutar las pruebas:

```powershell
python -m unittest discover -s tests
```

## Metodología de desarrollo

1. **Análisis de requisitos**
   - Se revisaron las reglas de negocio.
   - Se definieron los tipos de empleado y validaciones.
2. **Diseño orientado a objetos**
   - Se creó una clase base `Empleado` con subclases para cada tipo de empleado.
   - Se separó la lógica de negocio de la interfaz gráfica.
3. **Implementación**
   - Se desarrolló el cálculo de salario, bonos, beneficios y deducciones.
   - Se añadió la aplicación GUI con `tkinter`.
4. **Pruebas**
   - Se añadieron pruebas unitarias para verificar casos clave.
5. **Generación del ejecutable**
   - Se utilizó `PyInstaller` para crear `dist/empleados.exe`.

## Cumplimiento de buenas prácticas

El proyecto está diseñado para cumplir con:

- Principios SOLID
- Código limpio y legible
- Refactorización de responsabilidades
- Buen manejo de errores y validaciones
- Pruebas unitarias
- Documentación de cumplimiento en `COMPLIANCE.md`

## Estructura del proyecto

- `empleados.py` - Código principal con clases de negocio y GUI.
- `tests/test_empleados.py` - Pruebas unitarias.
- `COMPLIANCE.md` - Documentación de cumplimiento de requisitos.
- `dist/empleados.exe` - Ejecutable generado.
- `build/` - Archivos temporales de PyInstaller.
- `empleados.spec` - Especificación de PyInstaller.

## Nota

Este README complementa el desarrollo ya realizado sin modificar la lógica original del sistema.
