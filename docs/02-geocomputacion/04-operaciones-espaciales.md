# Operaciones espaciales

!!! question "Pregunta guía"
    ¿Qué muestras caen en qué cuartel, qué tan lejos está cada pozo del canal y cómo resumo un ráster por vecindario?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Usar predicados topológicos (`intersects`, `within`, `touches`) para seleccionar entidades.
2. Hacer uniones y agregaciones espaciales con `sjoin` y `sjoin_nearest`.
3. Calcular distancias entre geometrías en un CRS adecuado.
4. Aplicar álgebra de mapas: operaciones locales, focales, zonales y globales.
5. Combinar rásteres que comparten grilla.

## Esquema del capítulo

**1. Operaciones espaciales con vectores**

- Subconjuntos espaciales y relaciones topológicas.
- Unión espacial (`sjoin`) y unión sin solapamiento (`sjoin_nearest`).
- Agregación espacial y capas incongruentes (interpolación areal).
- Relaciones de distancia.

**2. Operaciones espaciales con rásteres**

- Subconjuntos espaciales.
- Álgebra de mapas: local, focal (ventanas móviles), zonal y global.
- Equivalencias entre álgebra de mapas y operaciones vectoriales.
- Combinar rásteres (mosaico).

**3. Errores frecuentes**

- `sjoin` con `how='inner'` que descarta muestras sin aviso.
- Distancias calculadas en grados.

## Ejemplo agronómico previsto

Asignar cada muestra de suelo a su cuartel, encontrar la estación meteorológica más cercana a cada predio y suavizar un NDVI con una ventana de 3 × 3.

## Material base

- PDF del curso: *3. Operaciones con datos espaciales*.
- Secciones 4.3, 5.5 y 6.7 del [capítulo 1](01-panorama.md).

## Referencias

1. Lovelace, R., Nowosad, J. y Muenchow, J. *Geocomputation with Python*. Libro abierto: [py.geocompx.org](https://py.geocompx.org/). Capítulo 4.
2. [GeoPandas: uniones espaciales](https://geopandas.org/en/stable/docs/user_guide/mergingdata.html).
3. [SciPy: filtros n-dimensionales](https://docs.scipy.org/doc/scipy/reference/ndimage.html).
