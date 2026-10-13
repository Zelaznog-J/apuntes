# 1. Datos geográficos en Python

Los datos geográficos se representan de dos formas principales: vectorial y ráster. Este capítulo presenta ambos modelos, las herramientas de Python para trabajar con ellos y el papel del sistema de coordenadas.

## Dos modelos de datos

**Los datos geográficos se representan principalmente de dos formas: vectorial y ráster.** El modelo vectorial representa entidades mediante puntos, líneas y polígonos; el ráster representa el espacio como una cuadrícula de celdas.

## Datos vectoriales

**El vector es adecuado para objetos con límites definidos.** Ejemplos: caminos, predios, ciudades, ríos o estaciones de muestreo. En Python, el trabajo vectorial se apoya principalmente en `geopandas` y `shapely`.

**La estructura vectorial en Python es jerárquica:** `GeoDataFrame` → `GeoSeries` → geometrías `shapely`. El `GeoDataFrame` representa la capa completa, la `GeoSeries` es la columna geométrica y cada elemento individual es una geometría.

**Un `GeoDataFrame` combina geometría y atributos.** Por eso se comporta como un `DataFrame` de pandas, pero además permite operaciones espaciales.

**Las geometrías siguen el estándar Simple Features.** Los tipos principales son `POINT`, `LINESTRING`, `POLYGON` y sus versiones `MULTI`, además de `GEOMETRYCOLLECTION`. WKT es una forma legible de representar esas geometrías como texto.

## Datos ráster

**El ráster representa el espacio mediante píxeles con valores.** Cada celda contiene un valor, que puede representar una variable continua (como elevación o temperatura) o categórica (como suelo o cobertura vegetal).

**En `rasterio`, un ráster se entiende como valores + metadatos.** Los valores se almacenan como un array NumPy y los metadatos contienen información como CRS, resolución, dimensiones, `nodata` y transformación espacial.

**Abrir un ráster no significa cargar todos sus valores.** `rasterio.open()` crea una conexión al archivo; `.meta` permite consultar sus metadatos y `.read()` carga una o varias bandas en memoria.

## Georreferenciación y CRS

**La georreferenciación es lo que convierte una matriz en información geográfica.** El `transform` relaciona filas y columnas con coordenadas reales mediante el origen y la resolución; el CRS indica cómo interpretar esas coordenadas respecto de la Tierra.

**El CRS y sus unidades condicionan todo análisis espacial.** Un CRS geográfico suele trabajar en grados y uno proyectado en unidades lineales como metros. Por eso, áreas, distancias y buffers solo tienen sentido si sabes qué CRS y unidades estás usando.

!!! note "Idea clave del capítulo"
    Antes de analizar datos geográficos hay que comprender **cómo están representados y georreferenciados**.
