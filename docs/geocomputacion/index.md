# GeoComputación con Python

El libro *Geocomputation with Python* (Dorman, Graser, Nowosad y Lovelace, 2025; Chapman & Hall/CRC, serie The Python Series) enseña a analizar datos geográficos con Python de forma reproducible y con software de código abierto. Se inspira en el movimiento FOSS4G (software libre para geoespacial). Más que un manual de una librería, recorre el flujo de trabajo con datos espaciales. Parte de cómo se representan, pasa por manipularlos, analizarlos y transformarlos, y termina en cómo leerlos, escribirlos y visualizarlos.

## El contenido del libro

1. **Datos geográficos en Python:** modelos vectorial y ráster, y el papel del CRS.
2. **Operaciones con atributos:** filtrar, agregar y unir tablas con geometría.
3. **Operaciones espaciales:** relaciones entre geometrías, uniones espaciales y álgebra de mapas.
4. **Operaciones geométricas:** simplificar, centroides, buffers, transformaciones y recortes.
5. **Interacciones ráster-vector:** enmascarar, recortar, extraer valores y convertir entre ambos modelos.
6. **Reproyección:** sistemas de referencia, transformación de coordenadas y remuestreo de rásteres.
7. **E/S de datos:** lectura y escritura de datos geográficos.
8. **Mapas con Python:** visualización cartográfica.

Libro original: [py.geocompx.org](https://py.geocompx.org/)

## Esquema general

![Esquema del flujo de trabajo con datos espaciales en Python](img/esquema-geocomputacion.webp)

El esquema resume cómo se conectan los temas del libro. Todo parte de los **datos espaciales**, que se representan como **vector** (puntos, líneas y polígonos, con GeoPandas y Shapely) o como **ráster** (celdas, con Rasterio y NumPy). Sobre ellos se hace el **análisis espacial**, que se divide en tres frentes: los **atributos** (filtros, `groupby`, `dissolve`, `merge`), las **relaciones espaciales** (`intersects`, `within`, `contains`, `sjoin`) y la **geometría** (`buffer`, `centroid`, `simplify`, `intersection`, `clip`). A continuación vienen el **álgebra ráster** (operaciones locales, focales, zonales y globales) y la **interacción ráster-vector** (máscara y recorte, extracción, rasterización y vectorización). Todo el flujo se apoya en el **CRS y la reproyección**, que definen las unidades, las distancias y las áreas, y garantizan que las capas estén alineadas.

En esta sección encontrarás apuntes y resúmenes de lo que he aprendido con el libro.