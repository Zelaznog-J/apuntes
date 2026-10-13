# 4. Operaciones geométricas

La pregunta central de este capítulo es: **¿cómo puedo transformar la geometría o estructura espacial de mis datos?**

## De consultar a modificar geometrías

**Las operaciones geométricas modifican directamente la forma o representación espacial de los datos.** Ya no solo consultan relaciones: generan nuevas geometrías.

## Simplificación

**La simplificación reduce la cantidad de vértices de líneas y polígonos.** `.simplify()` permite generalizar geometrías y disminuir el tamaño de los datos.

**Simplificar puede afectar la topología.** Si polígonos vecinos se simplifican independientemente pueden aparecer huecos o solapamientos; los métodos topológicamente conscientes ayudan a evitarlo.

## Centroides y buffers

**El centroide representa el centro geométrico de una entidad.** `.centroid` resulta útil para etiquetado, representación simplificada o cálculo aproximado de distancias.

**El centroide no siempre queda dentro del polígono.** `.representative_point()` genera un punto garantizado dentro de la geometría y puede ser preferible para etiquetar polígonos irregulares.

**Los buffers representan zonas de influencia.** `.buffer(distancia)` genera polígonos alrededor de puntos, líneas o polígonos utilizando las unidades del CRS.

## Transformaciones y operaciones entre geometrías

**Las transformaciones afines permiten trasladar, escalar y rotar geometrías.** GeoPandas proporciona métodos como `.translate()`, `.scale()` y `.rotate()`.

**Las operaciones binarias generan geometrías nuevas a partir de dos entradas.** Entre ellas están `.intersection()`, `.difference()`, `.union()` y `.symmetric_difference()`.

**Subsetting y clipping no son equivalentes.** El primero selecciona entidades completas; el segundo puede cortar y modificar sus geometrías según otra geometría.

## Tipos de geometría y estructura ráster

**También es posible cambiar el tipo de geometría y transformar la estructura de los rásteres.** Las operaciones incluyen conversiones entre tipos vectoriales, cambios de extensión, resolución, agregación, desagregación y remuestreo.

!!! note "Idea clave del capítulo"
    La pregunta central es **"¿cómo puedo transformar la geometría o estructura espacial de mis datos?"**
