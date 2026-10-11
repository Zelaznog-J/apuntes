# Lectura y escritura de datos geográficos

!!! question "Pregunta guía"
    ¿En qué formato guardo y comparto mis datos, y cómo leo solo la parte que necesito de un archivo enorme?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Leer y escribir capas vectoriales en GeoPackage, GeoJSON, Shapefile y GeoParquet.
2. Leer y escribir rásteres en GeoTIFF y Cloud Optimized GeoTIFF (COG).
3. Filtrar al leer: por extensión, por atributos y por columnas.
4. Consultar GeoParquet remoto con DuckDB.
5. Elegir formato según tamaño, interoperabilidad y uso.

## Esquema del capítulo

**1. Formatos vectoriales**

- GeoPackage como formato por defecto; limitaciones del Shapefile.
- GeoParquet para datos grandes.

**2. Formatos ráster**

- GeoTIFF, compresión y `nodata`.
- COG: lectura parcial por HTTP.

**3. Leer solo lo necesario**

- `bbox`, `mask`, `where` y `columns` en `read_file`.
- Ventanas en Rasterio.

**4. DuckDB espacial**

- Consultar GeoParquet en S3 y exportar resultados.

**5. Errores frecuentes**

- Nombres de campo truncados en Shapefile.
- Archivos `.prj` ausentes.

## Ejemplo agronómico previsto

Descargar los límites comunales de una región desde Overture Maps con DuckDB y guardarlos en GeoPackage y GeoParquet para comparar tamaño y velocidad de lectura.

!!! example "Caso aplicado"
    [Límites administrativos de Chile con Overture Maps](https://zelaznog-j.github.io/proyectos/overture/)

## Material base

- Proyecto del portafolio: límites administrativos con Overture Maps.
- Sección 5.7 del [capítulo 1](01-panorama.md) y sección 6.7 de [GDAL y Python](09-curvas-de-nivel/gdal-y-python.md).

## Referencias

1. Lovelace, R., Nowosad, J. y Muenchow, J. *Geocomputation with Python*. Libro abierto: [py.geocompx.org](https://py.geocompx.org/). Capítulo 8.
2. [pyogrio](https://pyogrio.readthedocs.io/).
3. [DuckDB: extensión spatial](https://duckdb.org/docs/extensions/spatial/overview.html).
4. [GeoParquet](https://geoparquet.org/).
