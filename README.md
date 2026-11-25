# Módulo de pedidos — Integración continua

Parte mínima del sistema de gestión de pedidos y despachos: calcula el total de un
pedido con descuentos y valida existencias. Sirve como base para demostrar control
de versiones, pruebas automatizadas y un entorno reproducible con Docker.

## Estructura

```
pedidos-ci/
├── docs/especificacion.md   Comportamiento esperado (escrito antes del código)
├── tests/                   14 pruebas automáticas (R1–R11, C1–C2)
├── pedidos/pedido.py        Lógica del pedido
├── pedidos/config.py        Configuración por ambiente (variables de entorno)
├── Dockerfile               Imagen que corre las pruebas
├── Jenkinsfile              Pipeline de integración continua
├── jenkins/                 Servidor Jenkins en Docker (Dockerfile, compose, plugins)
├── requirements.txt         Dependencias (pytest, pytest-cov)
├── .env.example             Plantilla de variables; el .env real no se sube
└── .gitignore
```

## Ejecutar las pruebas

Con Python instalado:

```bash
pip install -r requirements.txt
pytest -v
```

Con Docker (no requiere Python en el equipo):

```bash
docker build -t pedidos-ci .
docker run --rm pedidos-ci
```

Misma imagen, otro ambiente: solo cambian las variables.

```bash
docker run --rm -e APP_ENV=pruebas pedidos-ci
```

## Integración continua con Jenkins

El archivo `Jenkinsfile` define el pipeline. Jenkins corre en Docker y usa el
motor de Docker del equipo para construir la imagen y ejecutar las pruebas.

```bash
cd jenkins
docker compose up -d --build      # levanta Jenkins en http://localhost:8080
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Etapas del pipeline, en cada rama:

1. **Código**: identifica la rama y el commit.
2. **Construir imagen**: `docker build -t pedidos-ci:<commit> .`
3. **Pruebas en contenedor**: `pytest` con reporte JUnit y cobertura.
4. **Publicar imagen** (solo `main`): etiqueta la imagen aprobada como `latest`.

Ramas: `main` (producción), `develop` (integración), `feature/*` (funcionalidades),
`hotfix/*` (correcciones urgentes). Las versiones se marcan con etiquetas (`v1.0`).

---

# Guía para la entrega

Sigue los pasos en orden. Antes de cada comando que sea evidencia, ejecuta `date`
para que la fecha quede visible en la captura (Windows PowerShell: `Get-Date`).

## Paso 1 — Crear el repositorio y el primer commit (especificación)

1. En GitHub crea un repositorio nuevo llamado `pedidos-ci`, privado, sin README.
2. Agrega al tutor como colaborador (Settings → Collaborators), o hazlo público.
3. En tu equipo, dentro de esta carpeta:

```bash
git init
git config user.name "Tu Nombre"
git config user.email "tu-correo@ejemplo.com"
git add docs/especificacion.md .gitignore README.md
git commit -m "Especificación del comportamiento esperado (R1-R11)"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/pedidos-ci.git
git push -u origin main
```

## Paso 2 — Pruebas antes del código

Este commit demuestra que las pruebas se escribieron primero.

```bash
git add tests/ requirements.txt pytest.ini
git commit -m "Pruebas automáticas antes de la implementación"
```

Opcional pero recomendado: corre `pytest -v` en este punto y guarda la captura.
Fallarán porque todavía no hay código; esa falla es la evidencia de TDD.

## Paso 3 — Implementación en una rama

```bash
git checkout -b feature/calculo-pedido
git add pedidos/
git commit -m "Implementa cálculo del total y validación de existencias"
pytest -v
git checkout main
git merge feature/calculo-pedido
git push origin main
```

Captura: `pytest -v` con las 12 pruebas aprobadas.

## Paso 4 — Docker

```bash
git add Dockerfile .dockerignore .env.example
git commit -m "Dockerfile para construir la imagen y correr las pruebas"
git push

date
docker build -t pedidos-ci .
docker images pedidos-ci
docker run --name pedidos-pruebas -e APP_ENV=pruebas pedidos-ci
docker ps -a --filter name=pedidos-pruebas
```

Capturas: la construcción, la imagen listada, las pruebas pasando dentro del
contenedor y el contenedor en `docker ps -a`.

Si algo falla (Docker no inicia, error de construcción), guarda la captura del
error y de cómo lo corregiste: la rúbrica lo cuenta como evidencia.

## Paso 5 — Recuperar una versión anterior

```bash
date
git log --oneline
# Copia el id del commit de "Pruebas automáticas antes de la implementación"
git show --stat <ID_COMMIT>
git checkout <ID_COMMIT> -- tests/test_pedido.py
git status
git checkout HEAD -- tests/test_pedido.py   # vuelve a la versión actual
```

Variante más ilustrativa: cambia algo a propósito en `pedidos/pedido.py`, haz
commit, y luego recupéralo con `git checkout <ID_ANTERIOR> -- pedidos/pedido.py`
mostrando con `pytest` que vuelve a funcionar.

## Paso 6 — Clonar en otro directorio y correr las pruebas

```bash
cd ..
date
git clone https://github.com/TU_USUARIO/pedidos-ci.git pedidos-ci-clon
cd pedidos-ci-clon
pip install -r requirements.txt
pytest -v
```

## Paso 7 — Revisión de seguridad

```bash
git log -p | grep -iE "password|clave|secret|token" || echo "Sin secretos"
```

Revisa también que ninguna captura muestre contraseñas, tokens o datos reales.
