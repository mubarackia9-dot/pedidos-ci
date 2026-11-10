"""Cálculo del total de un pedido con descuentos y validación de existencias.

Parte mínima del sistema de gestión de pedidos y despachos. Implementa las reglas
de docs/especificacion.md.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


class PedidoError(Exception):
    """Error base de validación de pedidos."""


class DescuentoInvalido(PedidoError):
    pass


class ExistenciasInsuficientes(PedidoError):
    pass


class ProductoNoEncontrado(PedidoError):
    pass


class CantidadInvalida(PedidoError):
    pass


@dataclass(frozen=True)
class LineaPedido:
    codigo: str
    cantidad: int
    precio_unitario: int


class Inventario:
    """Inventario en memoria: {codigo: {"precio": int, "existencias": int}}."""

    def __init__(self, productos):
        self._productos = {codigo: dict(datos) for codigo, datos in productos.items()}

    def producto(self, codigo):
        if codigo not in self._productos:
            raise ProductoNoEncontrado(f"El producto {codigo} no existe")
        return self._productos[codigo]

    def existencias(self, codigo):
        return self.producto(codigo)["existencias"]

    def descontar(self, codigo, cantidad):
        self._productos[codigo]["existencias"] -= cantidad


def calcular_subtotal(lineas):
    """R1: suma de cantidad x precio unitario."""
    return sum(linea.cantidad * linea.precio_unitario for linea in lineas)


def calcular_total(subtotal, descuento_porcentaje):
    """R2-R6: aplica un descuento porcentual (0 a 100) y redondea al peso."""
    if not 0 <= descuento_porcentaje <= 100:
        raise DescuentoInvalido(
            f"El descuento debe estar entre 0 y 100; se recibió {descuento_porcentaje}"
        )
    factor = (Decimal(100) - Decimal(str(descuento_porcentaje))) / Decimal(100)
    total = Decimal(subtotal) * factor
    return int(total.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def procesar_pedido(inventario, items, descuento):
    """R7-R11: valida todas las líneas antes de tocar el inventario.

    items: lista de tuplas (codigo, cantidad).
    Devuelve el total a cobrar.
    """
    lineas = []
    for codigo, cantidad in items:
        if cantidad <= 0:
            raise CantidadInvalida(f"La cantidad de {codigo} debe ser mayor que cero")
        producto = inventario.producto(codigo)
        if producto["existencias"] < cantidad:
            raise ExistenciasInsuficientes(
                f"{codigo}: se pidieron {cantidad}, hay {producto['existencias']}"
            )
        lineas.append(LineaPedido(codigo, cantidad, producto["precio"]))

    total = calcular_total(calcular_subtotal(lineas), descuento)

    for linea in lineas:
        inventario.descontar(linea.codigo, linea.cantidad)
    return total
