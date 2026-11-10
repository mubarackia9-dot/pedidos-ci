# Especificación del comportamiento esperado

Este documento se escribe **antes** del código. Cada regla tiene una o más pruebas
automáticas en `tests/` que la verifican.

Los valores monetarios están en pesos colombianos (COP) y se manejan como enteros,
sin centavos. Cuando un cálculo produce fracciones, se redondea al peso más
cercano (0,5 hacia arriba).

## Reglas

| # | Regla | Entrada | Resultado esperado |
|---|-------|---------|--------------------|
| R1 | El subtotal es la suma de cantidad × precio unitario de cada línea. | 2 × 5.000 + 1 × 12.000 | 22.000 |
| R2 | Sin descuento, el total es igual al subtotal. | subtotal 22.000, descuento 0 % | 22.000 |
| R3 | El descuento se expresa en porcentaje (0 a 100) y se resta del subtotal. | subtotal 100.000, descuento 10 % | 90.000 |
| R4 | **Error del caso:** un descuento del 10 % nunca puede cobrarse como si fuera 10 veces el valor ni dejar el total en negativo. | subtotal 100.000, descuento 10 % | 90.000 (no 10.000, no -900.000) |
| R5 | El total se redondea al peso más cercano. | subtotal 9.999, descuento 15 % | 8.499 (8.499,15 → 8.499) |
| R6 | Un descuento menor que 0 % o mayor que 100 % se rechaza. | descuento 150 % | Error `DescuentoInvalido` |
| R7 | Si un producto pedido no tiene existencias suficientes, el pedido se rechaza. | pide 5, hay 3 | Error `ExistenciasInsuficientes` |
| R8 | Si el producto no existe en el inventario, el pedido se rechaza. | producto "X-999" | Error `ProductoNoEncontrado` |
| R9 | Las cantidades deben ser mayores que cero. | cantidad 0 | Error `CantidadInvalida` |
| R10 | Un pedido válido descuenta las existencias del inventario. | pide 2, hay 10 | quedan 8 |
| R11 | Si una línea falla la validación, el inventario no cambia en ninguna línea. | línea 1 válida, línea 2 sin existencias | inventario intacto |

## Configuración por ambiente

La misma imagen Docker se usa en desarrollo, pruebas y producción. Lo único que
cambia entre ambientes son variables de entorno:

| Variable | Propósito | Ejemplo en pruebas |
|----------|-----------|--------------------|
| `APP_ENV` | Nombre del ambiente | `pruebas` |
| `DATABASE_URL` | Conexión a la base de datos de ese ambiente | `postgresql://usuario@db-pruebas:5432/pedidos` |

Las credenciales **nunca** se escriben en el código ni en el repositorio.
