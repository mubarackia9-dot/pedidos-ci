# Imagen del módulo de pedidos: construye la aplicación y corre las pruebas.
FROM python:3.12-slim

WORKDIR /app

# Dependencias primero, para aprovechar la caché de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código y pruebas.
COPY pedidos/ ./pedidos/
COPY tests/ ./tests/
COPY pytest.ini .

# Valor por defecto; cada ambiente lo cambia con -e APP_ENV=...
ENV APP_ENV=desarrollo

# Al iniciar el contenedor se ejecutan todas las pruebas con un solo comando.
CMD ["pytest", "-v"]
