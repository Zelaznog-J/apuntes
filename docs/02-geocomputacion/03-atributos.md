# Operaciones con datos de atributos

!!! question "Pregunta guía"
    ¿Cómo filtro, resumo y uno información tabular de mis cuarteles sin perder su geometría?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Seleccionar filas y columnas de un `GeoDataFrame` con condiciones sobre sus atributos.
2. Agregar atributos por grupo (`groupby`, `dissolve`) y distinguir cuándo se conserva la geometría.
3. Unir tablas no espaciales (análisis de suelo, rendimientos) a una capa vectorial con `merge`.
4. Crear atributos nuevos y quitar la geometría cuando ya no se necesita.
5. Seleccionar subconjuntos de un ráster por posición y resumir sus valores.

## Esquema del capítulo

**1. Atributos en datos vectoriales**

- Subconjuntos: `loc`, `iloc`, máscaras booleanas, `query`.
- Agregación: `groupby` frente a `dissolve`.
- Uniones por atributo: `merge` y claves que no coinciden.
- Crear columnas y eliminar la geometría (`drop(columns='geometry')`).

**2. Atributos en datos ráster**

- Subconjuntos por fila y columna sobre el array.
- Resúmenes: estadísticos globales, histogramas, frecuencias de clases.

**3. Errores frecuentes**

- Claves con espacios o tildes distintas; tipos de dato incompatibles en la unión.
- Perder el CRS al convertir a `DataFrame`.

## Ejemplo agronómico previsto

Unir una planilla de análisis de suelo (pH, MO, P Olsen) a la capa de cuarteles, calcular la superficie por cultivo y marcar los cuarteles bajo un umbral de fósforo.

## Material base

- PDF del curso: *2. Operaciones con datos de atributos* (secciones 2.2 y 2.3).
- Sección 5.7 (disolver y exportar) del [capítulo 1](01-panorama.md).

## Referencias

1. Lovelace, R., Nowosad, J. y Muenchow, J. *Geocomputation with Python*. Libro abierto: [py.geocompx.org](https://py.geocompx.org/). Capítulo 3.
2. [GeoPandas: guía de usuario](https://geopandas.org/en/stable/docs/user_guide.html).
3. [pandas: merge, join y concat](https://pandas.pydata.org/docs/user_guide/merging.html).
