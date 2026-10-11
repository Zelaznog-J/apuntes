# Teledetección

Teledetección satelital y ciencia de datos aplicada a la agronomía: desde cómo un satélite "ve" un cultivo hasta convertir imágenes en decisiones de manejo dentro del lote.

El hilo de todos los capítulos es el mismo:

**imagen → índice → serie temporal → anomalía o zona → recorrida de campo → decisión → verificación**

## Capítulos

| Capítulo | Pregunta guía |
| --- | --- |
| 1. [Fundamentos de teledetección](01-fundamentos.md) | ¿Qué "ve" un satélite cuando observa un cultivo? |
| 2. [Evolución de la tecnología satelital y apertura de los datos](02-evolucion-datos.md) | ¿Por qué hoy cualquiera accede gratis a lo que antes costaba miles de dólares por imagen? |
| 3. [Índices de vegetación y su interpretación agronómica](03-indices-vegetacion.md) | ¿Cómo convierto reflectancias en información sobre el cultivo? |
| 4. [Introducción a Python para datos geoespaciales](04-python.md) · [notebook guía](04-python-notebook.ipynb) | ¿Por qué programar si puedo ver las imágenes en el navegador? |
| 5. [Acceso a imágenes satelitales con Python](05-acceso-imagenes.md) | ¿Cómo consigo todas las imágenes de mi lote sin descargarlas una por una? |
| 6. [Procesamiento raster y cálculo de índices](06-procesamiento-raster.md) | ¿Cómo convierto una imagen cruda en un mapa confiable del lote? |
| 7. [Series de tiempo y detección de anomalías](07-series-tiempo.md) | ¿Cómo evolucionó mi cultivo y cuándo algo salió de lo esperado? |
| 8. [Machine learning aplicado a la agronomía](08-machine-learning.md) | ¿Puede un algoritmo aprender a reconocer cultivos a partir de imágenes? |
| 9. [Integración y mapas de manejo sitio‑específico](09-integracion.md) | ¿Qué decisión concreta tomo con todo esto? |

Los capítulos 1 a 3 son conceptuales; del 4 al 8 son prácticos, con código en Python. A lo largo de todos se construye un **proyecto integrador** sobre un lote propio, que se cierra en el capítulo 9.

## Datos de ejemplo

- [`lote_reflectancias_v2.csv`](datos/lote_reflectancias_v2.csv): reflectancias medias de un lote de trigo en una campaña (capítulos 4 y 7).
- [`muestras_cultivos_v2.csv`](datos/muestras_cultivos_v2.csv): muestras sintéticas de cuatro coberturas para clasificación (capítulo 8), generadas con [`generador_muestras.py`](datos/generador_muestras.py).

## Convenciones

Se usan igual en todos los capítulos:

| Tema | Convención |
|---|---|
| Producto Sentinel‑2 | Nivel **L2A** (reflectancia de superficie). En Earth Engine: `COPERNICUS/S2_SR_HARMONIZED` |
| Escala | Reflectancia = valor ÷ 10.000. La colección *harmonized* ya corrige el desplazamiento de +1.000 que ESA introdujo el 25‑ene‑2022 |
| Bandas de los índices | NDVI (B8, B4) · NDRE (B8A, B5) · GNDVI (B8, B3) · SAVI (B8, B4; L = 0,5) · EVI (B8, B4, B2) · NDMI = NDWI de Gao (B8A, B11) · NDWI de McFeeters (B3, B8) |
| Orden de bandas exportadas | B2, B3, B4, B5, B8, B8A, B11, SCL; se llaman **por nombre** |
| Máscara de nubes | SCL con clases válidas 4 y 5; descartar la fecha si hay < 80 % de píxeles válidos dentro del lote |
| Rangos de NDVI | Agua < 0 · suelo ~0,1–0,2 · implantación ~0,2–0,4 · intermedio ~0,4–0,6 · pleno desarrollo ~0,6–0,9 (orientativos) |
| Coordenadas | Earth Engine usa [longitud, latitud]. Los buffers en metros requieren CRS proyectado (UTM) |
| Campaña de ejemplo | Septiembre de 2024 a enero de 2025 (trigo, hemisferio sur) |
| Validación en ML | Siempre por lote (`GroupKFold`), nunca por píxel |

!!! example "Caso aplicado"
    [Área quemada y severidad del incendio Penco–Lirquén con Sentinel-2](https://zelaznog-j.github.io/proyectos/incendio-penco/)
