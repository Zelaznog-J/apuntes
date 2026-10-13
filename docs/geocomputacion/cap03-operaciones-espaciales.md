# 3. Operaciones con datos espaciales

La pregunta central de este capítulo es: **¿dónde están mis objetos y cómo se relacionan entre sí?**

## Relaciones espaciales entre geometrías

**Las operaciones espaciales utilizan la ubicación y la relación entre geometrías.** A diferencia del capítulo anterior, el criterio de selección ya no tiene que provenir de una columna.

**Un subconjunto espacial selecciona entidades según su relación con otra geometría.** El resultado suele construirse mediante una `Series` booleana.

**`.intersects()` es uno de los predicados espaciales más generales.** Devuelve `True` cuando dos geometrías comparten al menos algún punto.

**Existen varias relaciones topológicas.** Entre las más importantes están `.within()`, `.contains()`, `.touches()`, `.crosses()`, `.overlaps()` y `.disjoint()`.

**El orden importa en algunos predicados.** `A.contains(B)` no equivale a `B.contains(A)`, mientras que `intersects` es una relación simétrica.

**La distancia también permite describir relaciones espaciales.** Puede calcularse con `.distance()` y compararse con un umbral para identificar objetos cercanos.

## Uniones y agregación espacial

**La unión espacial (`sjoin`) combina atributos según la posición.** En vez de usar un identificador común, relaciona entidades por criterios como intersección, inclusión o proximidad.

**La agregación espacial combina relaciones espaciales y estadística.** Un flujo típico es: `sjoin()` → `groupby()` → función de resumen → unión del resultado a una capa geográfica.

## Álgebra de mapas y CRS

**En ráster, el álgebra de mapas permite transformar valores espacialmente.** Las operaciones pueden ser locales, focales, zonales o globales según si usan una celda, sus vecinas, zonas o todo el ráster.

**Las capas involucradas en una operación espacial deben usar sistemas de coordenadas compatibles.** Esto es especialmente importante para distancias, buffers y combinaciones entre capas.

!!! note "Idea clave del capítulo"
    La pregunta pasa a ser **"¿dónde están mis objetos y cómo se relacionan entre sí?"**
