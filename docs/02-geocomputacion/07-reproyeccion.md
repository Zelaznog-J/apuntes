# Reproyección y sistemas de referencia en la práctica

!!! question "Pregunta guía"
    ¿Qué CRS uso para medir en Chile y qué le pasa a mis datos cuando los reproyecto?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Distinguir CRS geográficos y proyectados, y elegir uno adecuado para medir áreas y distancias.
2. Diferenciar asignar un CRS (`set_crs`) de transformar coordenadas (`to_crs`).
3. Reproyectar capas vectoriales y rásteres, eligiendo el método de remuestreo.
4. Reconocer los CRS de uso habitual en Chile (WGS 84, UTM 18S y 19S, SIRGAS-Chile).
5. Detectar errores de CRS antes de que lleguen a un resultado.

## Esquema del capítulo

**1. Conceptos**

- Datum, elipsoide y proyección.
- Códigos EPSG y WKT; `pyproj.CRS`.

**2. Reproyectar vectores**

- `to_crs` y sus límites (geometrías que cruzan el antimeridiano).

**3. Reproyectar rásteres**

- `rasterio.warp.reproject` y `calculate_default_transform`.
- Remuestreo continuo frente a categórico.

**4. CRS en Chile**

- UTM 18S y 19S, el meridiano 72° O como frontera y qué hacer con regiones que cruzan dos husos.

**5. Errores frecuentes**

- Áreas en grados cuadrados.
- `set_crs` donde correspondía `to_crs`.

## Ejemplo agronómico previsto

Calcular la superficie de los predios de una comuna que cruza dos husos UTM y comparar el resultado con una proyección de áreas iguales.

## Material base

- Sección 1.4 del PDF *1. Datos geográficos en Python*.
- Secciones 2, 5.4 y 10 del [capítulo 1](01-panorama.md).

## Referencias

1. Lovelace, R., Nowosad, J. y Muenchow, J. *Geocomputation with Python*. Libro abierto: [py.geocompx.org](https://py.geocompx.org/). Capítulo 7.
2. [GeoPandas: proyecciones](https://geopandas.org/en/stable/docs/user_guide/projections.html).
3. [EPSG.io](https://epsg.io/).
