"""Pruebas del cálculo del total de un pedido y la validación de existencias.

Escritas antes del código a partir de docs/especificacion.md. Cada prueba indica
la regla (R1...R11) que verifica.
"""

import pytest

from pedidos.pedido import (
    CantidadInvalida,
    DescuentoInvalido,
    ExistenciasInsuficientes,
    Inventario,
    LineaPedido,
    ProductoNoEncontrado,
    calcular_subtotal,
    calcular_total,
    procesar_pedido,
)


@pytest.fixture
def inventario():
    return Inventario({
        "ARROZ-500": {"precio": 5_000, "existencias": 10},
        "ACEITE-1L": {"precio": 12_000, "existencias": 3},
    })


# --- Cálculo del total -------------------------------------------------------

def test_r1_subtotal_suma_cantidad_por_precio():
    lineas = [LineaPedido("ARROZ-500", 2, 5_000), LineaPedido("ACEITE-1L", 1, 12_000)]
    assert calcular_subtotal(lineas) == 22_000


def test_r2_sin_descuento_total_igual_a_subtotal():
    assert calcular_total(22_000, 0) == 22_000


def test_r3_descuento_porcentual_se_resta_del_subtotal():
    assert calcular_total(100_000, 10) == 90_000


def test_r4_error_del_caso_descuento_del_10_no_se_multiplica_mal():
    """Reproduce el error que llegó a los clientes.

    Un 10 % mal aplicado puede cobrar solo el descuento (10.000) o dejar el total
    en negativo (100.000 * (1 - 10) = -900.000). El total correcto es 90.000.
    """
    total = calcular_total(100_000, 10)
    assert total == 90_000
    assert total != 10_000
    assert total > 0


def test_r5_total_se_redondea_al_peso_mas_cercano():
    assert calcular_total(9_999, 15) == 8_499


@pytest.mark.parametrize("descuento", [-5, 150])
def test_r6_descuento_fuera_de_rango_se_rechaza(descuento):
    with pytest.raises(DescuentoInvalido):
        calcular_total(100_000, descuento)


# --- Validación de existencias -----------------------------------------------

def test_r7_existencias_insuficientes_rechazan_el_pedido(inventario):
    with pytest.raises(ExistenciasInsuficientes):
        procesar_pedido(inventario, [("ACEITE-1L", 5)], descuento=0)


def test_r8_producto_inexistente_rechaza_el_pedido(inventario):
    with pytest.raises(ProductoNoEncontrado):
        procesar_pedido(inventario, [("X-999", 1)], descuento=0)


def test_r9_cantidad_cero_o_negativa_se_rechaza(inventario):
    with pytest.raises(CantidadInvalida):
        procesar_pedido(inventario, [("ARROZ-500", 0)], descuento=0)


def test_r10_pedido_valido_descuenta_existencias_y_calcula_total(inventario):
    total = procesar_pedido(inventario, [("ARROZ-500", 2)], descuento=10)
    assert total == 9_000
    assert inventario.existencias("ARROZ-500") == 8


def test_r11_si_una_linea_falla_el_inventario_no_cambia(inventario):
    with pytest.raises(ExistenciasInsuficientes):
        procesar_pedido(
            inventario, [("ARROZ-500", 2), ("ACEITE-1L", 5)], descuento=0
        )
    assert inventario.existencias("ARROZ-500") == 10
    assert inventario.existencias("ACEITE-1L") == 3
