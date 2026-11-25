"""Pruebas de la configuración por ambiente (variables de entorno).

La misma imagen se usa en todos los ambientes; solo cambian APP_ENV y DATABASE_URL.
"""

from pedidos import config


def test_c1_sin_variables_el_ambiente_es_desarrollo(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert config.ambiente() == "desarrollo"
    assert config.url_base_de_datos() == ""


def test_c2_el_ambiente_y_la_base_se_leen_de_variables(monkeypatch):
    monkeypatch.setenv("APP_ENV", "pruebas")
    monkeypatch.setenv("DATABASE_URL", "postgresql://usuario@db-pruebas:5432/pedidos")
    assert config.ambiente() == "pruebas"
    assert config.url_base_de_datos() == "postgresql://usuario@db-pruebas:5432/pedidos"
