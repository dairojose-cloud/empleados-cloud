from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from tkinter import messagebox, simpledialog, ttk
from typing import List

ARL_RATE = 0.01  # Asumido como 1% del salario bruto si no se especifica otra tasa
BONO_ALIMENTACION = 1_000_000


class EmpleadoError(ValueError):
    pass


class DialogCancel(Exception):
    pass


@dataclass
class Empleado(ABC):
    nombre: str
    cedula: str
    años_servicio: int

    @property
    @abstractmethod
    def salario_bruto(self) -> float:
        raise NotImplementedError

    @property
    def deducciones(self) -> float:
        base = self.salario_bruto
        seguridad_pension = 0.04 * base
        arl = ARL_RATE * base
        return seguridad_pension + arl

    @property
    def beneficios_adicionales(self) -> float:
        return 0.0

    @property
    def bonos(self) -> float:
        return 0.0

    @property
    def salario_neto(self) -> float:
        neto = self.salario_bruto + self.bonos + self.beneficios_adicionales - self.deducciones
        if neto < 0:
            raise EmpleadoError(f"El salario neto de {self.nombre} no puede ser negativo.")
        return neto

    def resumen_nomina(self) -> str:
        return (
            f"Empleado: {self.nombre} ({self.cedula})\n"
            f"Tipo: {self.__class__.__name__}\n"
            f"Salario bruto: ${self.salario_bruto:,.2f}\n"
            f"Bonos: ${self.bonos:,.2f}\n"
            f"Beneficios adicionales: ${self.beneficios_adicionales:,.2f}\n"
            f"Deducciones: ${self.deducciones:,.2f}\n"
            f"Salario neto: ${self.salario_neto:,.2f}\n"
        )


@dataclass
class EmpleadoAsalariado(Empleado):
    salario_fijo: float

    def __post_init__(self) -> None:
        if self.salario_fijo < 0:
            raise EmpleadoError("El salario fijo no puede ser negativo.")
        if self.años_servicio < 0:
            raise EmpleadoError("Los años de servicio no pueden ser negativos.")

    @property
    def salario_bruto(self) -> float:
        return self.salario_fijo

    @property
    def bonos(self) -> float:
        if self.años_servicio > 5:
            return 0.10 * self.salario_fijo
        return 0.0

    @property
    def beneficios_adicionales(self) -> float:
        return BONO_ALIMENTACION


@dataclass
class EmpleadoPorHoras(Empleado):
    tarifa_hora: float
    horas_trabajadas: float
    acepta_fondo_ahorro: bool = field(default=False)

    def __post_init__(self) -> None:
        if self.tarifa_hora < 0:
            raise EmpleadoError("La tarifa por hora no puede ser negativa.")
        if self.horas_trabajadas < 0:
            raise EmpleadoError("Las horas trabajadas no pueden ser negativas.")
        if self.años_servicio < 0:
            raise EmpleadoError("Los años de servicio no pueden ser negativos.")

    @property
    def salario_bruto(self) -> float:
        horas_normales = min(self.horas_trabajadas, 40)
        horas_extras = max(self.horas_trabajadas - 40, 0)
        return horas_normales * self.tarifa_hora + horas_extras * self.tarifa_hora * 1.5

    @property
    def beneficios_adicionales(self) -> float:
        if self.años_servicio > 1 and self.acepta_fondo_ahorro:
            return 0.02 * self.salario_bruto
        return 0.0


@dataclass
class EmpleadoPorComision(Empleado):
    salario_base: float
    porcentaje_comision: float
    ventas: float

    def __post_init__(self) -> None:
        if self.salario_base < 0:
            raise EmpleadoError("El salario base no puede ser negativo.")
        if self.porcentaje_comision < 0:
            raise EmpleadoError("El porcentaje de comisión no puede ser negativo.")
        if self.ventas < 0:
            raise EmpleadoError("Las ventas no pueden ser menores a $0.")
        if self.años_servicio < 0:
            raise EmpleadoError("Los años de servicio no pueden ser negativos.")

    @property
    def salario_bruto(self) -> float:
        return self.salario_base + self.comision

    @property
    def comision(self) -> float:
        return self.ventas * self.porcentaje_comision

    @property
    def bonos(self) -> float:
        if self.ventas > 20_000_000:
            return 0.03 * self.ventas
        return 0.0

    @property
    def beneficios_adicionales(self) -> float:
        return BONO_ALIMENTACION


@dataclass
class EmpleadoTemporal(Empleado):
    salario_fijo: float
    duracion_meses: int

    def __post_init__(self) -> None:
        if self.salario_fijo < 0:
            raise EmpleadoError("El salario fijo no puede ser negativo.")
        if self.duracion_meses <= 0:
            raise EmpleadoError("La duración del contrato debe ser mayor que cero.")
        if self.años_servicio < 0:
            raise EmpleadoError("Los años de servicio no pueden ser negativos.")

    @property
    def salario_bruto(self) -> float:
        return self.salario_fijo


class Nomina:
    def __init__(self, empleados: List[Empleado]) -> None:
        self.empleados = empleados

    def reporte(self) -> str:
        lineas = ["=== Reporte de Nómina ==="]
        for empleado in self.empleados:
            lineas.append(empleado.resumen_nomina())
        return "\n".join(lineas)

    def total_nomina(self) -> float:
        return sum(e.salario_neto for e in self.empleados)


def cargar_ejemplo_empleados() -> List[Empleado]:
    return [
        EmpleadoAsalariado(nombre="Ana Pérez", cedula="1001", años_servicio=6, salario_fijo=5_000_000),
        EmpleadoPorHoras(nombre="Luis Gómez", cedula="1002", años_servicio=2, tarifa_hora=30_000, horas_trabajadas=45, acepta_fondo_ahorro=True),
        EmpleadoPorComision(nombre="Carolina Rojas", cedula="1003", años_servicio=3, salario_base=1_200_000, porcentaje_comision=0.10, ventas=25_000_000),
        EmpleadoTemporal(nombre="Martín Díaz", cedula="1004", años_servicio=1, salario_fijo=2_000_000, duracion_meses=6),
    ]


class NominaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema de Nómina")
        self.geometry("860x620")
        self.resizable(False, False)
        self.empleados: List[Empleado] = []
        self.create_widgets()

    def create_widgets(self) -> None:
        frame_izq = ttk.Frame(self, padding=12)
        frame_izq.grid(row=0, column=0, sticky="nsew")

        frame_der = ttk.Frame(self, padding=12)
        frame_der.grid(row=0, column=1, sticky="nsew")

        ttk.Label(frame_izq, text="Agregar empleado", font=(None, 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Button(frame_izq, text="Asalariado", command=self.agregar_asalariado, width=24).grid(row=1, column=0, pady=4)
        ttk.Button(frame_izq, text="Por Horas", command=self.agregar_por_horas, width=24).grid(row=2, column=0, pady=4)
        ttk.Button(frame_izq, text="Por Comisión", command=self.agregar_por_comision, width=24).grid(row=3, column=0, pady=4)
        ttk.Button(frame_izq, text="Temporal", command=self.agregar_temporal, width=24).grid(row=4, column=0, pady=4)

        ttk.Separator(frame_izq, orient="horizontal").grid(row=5, column=0, sticky="ew", pady=12)
        ttk.Button(frame_izq, text="Cargar ejemplo", command=self.cargar_ejemplo, width=24).grid(row=6, column=0, pady=4)
        ttk.Button(frame_izq, text="Generar reporte", command=self.mostrar_reporte, width=24).grid(row=7, column=0, pady=4)
        ttk.Button(frame_izq, text="Salir", command=self.destroy, width=24).grid(row=8, column=0, pady=4)

        ttk.Label(frame_izq, text="Empleados registrados", font=(None, 12, "bold")).grid(row=9, column=0, pady=(20, 6))
        self.lista_empleados = tk.Listbox(frame_izq, width=35, height=18)
        self.lista_empleados.grid(row=10, column=0, sticky="nsew")

        frame_izq.rowconfigure(10, weight=1)

        ttk.Label(frame_der, text="Reporte de nómina", font=(None, 12, "bold")).grid(row=0, column=0, sticky="w")
        self.texto_reporte = tk.Text(frame_der, wrap="word", width=60, height=32, state="disabled")
        self.texto_reporte.grid(row=1, column=0, sticky="nsew")

        frame_der.rowconfigure(1, weight=1)
        frame_der.columnconfigure(0, weight=1)

    def pedir_texto(self, prompt: str) -> str:
        valor = simpledialog.askstring("Datos del empleado", prompt, parent=self)
        if valor is None:
            raise DialogCancel
        valor = valor.strip()
        if not valor:
            messagebox.showwarning("Entrada inválida", "El valor no puede estar vacío.")
            raise DialogCancel
        return valor

    def pedir_entero(self, prompt: str, minimo: int = 0) -> int:
        valor = simpledialog.askinteger("Datos del empleado", prompt, parent=self, minvalue=minimo)
        if valor is None:
            raise DialogCancel
        return valor

    def pedir_flotante(self, prompt: str, minimo: float = 0.0) -> float:
        valor = simpledialog.askfloat("Datos del empleado", prompt, parent=self, minvalue=minimo)
        if valor is None:
            raise DialogCancel
        return valor

    def agregar_empleado(self, empleado: Empleado) -> None:
        self.empleados.append(empleado)
        self.lista_empleados.insert(tk.END, f"{empleado.nombre} - {empleado.__class__.__name__}")
        messagebox.showinfo("Empleado agregado", "El empleado ha sido agregado correctamente.")

    def agregar_asalariado(self) -> None:
        try:
            empleado = EmpleadoAsalariado(
                nombre=self.pedir_texto("Nombre:"),
                cedula=self.pedir_texto("Cédula:"),
                años_servicio=self.pedir_entero("Años de servicio:", 0),
                salario_fijo=self.pedir_flotante("Salario fijo mensual:", 0.0),
            )
            self.agregar_empleado(empleado)
        except (EmpleadoError, DialogCancel):
            return

    def agregar_por_horas(self) -> None:
        try:
            empleado = EmpleadoPorHoras(
                nombre=self.pedir_texto("Nombre:"),
                cedula=self.pedir_texto("Cédula:"),
                años_servicio=self.pedir_entero("Años de servicio:", 0),
                tarifa_hora=self.pedir_flotante("Tarifa por hora:", 0.0),
                horas_trabajadas=self.pedir_flotante("Horas trabajadas este mes:", 0.0),
                acepta_fondo_ahorro=messagebox.askyesno("Fondo de ahorro", "¿Acepta acceso al fondo de ahorro?"),
            )
            self.agregar_empleado(empleado)
        except (EmpleadoError, DialogCancel):
            return

    def agregar_por_comision(self) -> None:
        try:
            empleado = EmpleadoPorComision(
                nombre=self.pedir_texto("Nombre:"),
                cedula=self.pedir_texto("Cédula:"),
                años_servicio=self.pedir_entero("Años de servicio:", 0),
                salario_base=self.pedir_flotante("Salario base mensual:", 0.0),
                porcentaje_comision=self.pedir_flotante("Porcentaje de comisión (0.10 = 10%):", 0.0),
                ventas=self.pedir_flotante("Ventas del mes:", 0.0),
            )
            self.agregar_empleado(empleado)
        except (EmpleadoError, DialogCancel):
            return

    def agregar_temporal(self) -> None:
        try:
            empleado = EmpleadoTemporal(
                nombre=self.pedir_texto("Nombre:"),
                cedula=self.pedir_texto("Cédula:"),
                años_servicio=self.pedir_entero("Años de servicio:", 0),
                salario_fijo=self.pedir_flotante("Salario fijo mensual:", 0.0),
                duracion_meses=self.pedir_entero("Duración del contrato (meses):", 1),
            )
            self.agregar_empleado(empleado)
        except (EmpleadoError, DialogCancel):
            return

    def cargar_ejemplo(self) -> None:
        self.empleados = cargar_ejemplo_empleados()
        self.lista_empleados.delete(0, tk.END)
        for empleado in self.empleados:
            self.lista_empleados.insert(tk.END, f"{empleado.nombre} - {empleado.__class__.__name__}")
        messagebox.showinfo("Ejemplo cargado", "Se cargaron empleados de ejemplo correctamente.")

    def mostrar_reporte(self) -> None:
        if not self.empleados:
            messagebox.showwarning("Sin empleados", "No hay empleados registrados. Agrega al menos uno.")
            return
        nomina = Nomina(self.empleados)
        contenido = nomina.reporte() + f"\nTotal de nómina (neto): ${nomina.total_nomina():,.2f}\n"
        self.texto_reporte.config(state="normal")
        self.texto_reporte.delete("1.0", tk.END)
        self.texto_reporte.insert(tk.END, contenido)
        self.texto_reporte.config(state="disabled")


if __name__ == "__main__":
    app = NominaApp()
    app.mainloop()
