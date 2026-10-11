# GeoComputación con Python

Representar, transformar y combinar datos geográficos con código: desde una geometría en Shapely hasta cubos de datos de 25 años, siempre con preguntas agronómicas de fondo.

El hilo de todos los capítulos es el mismo:

**pregunta agronómica → datos vectoriales y ráster → CRS común → operación espacial → resumen por unidad de manejo → verificación**

## Capítulos

| Capítulo | Pregunta guía | Estado |
| --- | --- | --- |
| 1. [Panorama: de las geometrías al análisis ráster–vector](01-panorama.md) | ¿Cómo respondo con código lo que hoy resuelvo con clics en un SIG? | Disponible |
| 2. [Datos geográficos: vector, ráster y CRS](02-datos-geograficos.ipynb) | ¿Cómo representa Python un cuartel o una imagen, y qué significan sus coordenadas? | En preparación |
| 3. [Operaciones con datos de atributos](03-atributos.md) | ¿Cómo filtro, resumo y uno tablas sin perder la geometría? | En preparación |
| 4. [Operaciones espaciales](04-operaciones-espaciales.md) | ¿Qué muestra cae en qué cuartel y cómo resumo un ráster por vecindario? | En preparación |
| 5. [Operaciones geométricas](05-operaciones-geometricas.md) | ¿Cómo creo franjas de protección o cambio la resolución de un ráster? | En preparación |
| 6. [Interacciones ráster–vector](06-raster-vector.md) | ¿Cómo obtengo el NDVI medio de cada cuartel? | En preparación |
| 7. [Reproyección y CRS en la práctica](07-reproyeccion.md) | ¿Qué CRS uso para medir en Chile? | En preparación |
| 8. [Lectura y escritura de datos](08-lectura-escritura.md) | ¿En qué formato guardo mis datos y cómo leo solo lo que necesito? | En preparación |
| 9. [Curvas de nivel](09-curvas-de-nivel/index.md) · [GDAL y Python](09-curvas-de-nivel/gdal-y-python.md) · [laboratorio](09-curvas-de-nivel/laboratorio.ipynb) | ¿Cómo paso de una grilla de alturas a líneas que se lean en el mapa del predio? | Disponible |
| 10. [Datos a escala: STAC, xarray y Dask](10-datos-a-escala.md) | ¿Cómo paso de un predio a una región y 25 años de datos? | En preparación |

El capítulo 1 es un recorrido completo por las herramientas; los capítulos 2 al 8 profundizan cada tema y siguen la secuencia de *Geocomputation with Python*. El capítulo 9 aplica todo a un problema completo y el 10 lleva los mismos conceptos a grandes volúmenes de datos.

## Entorno de trabajo

```bash
conda create -n geo -c conda-forge python=3.12 geopandas rasterio rasterstats gdal scikit-image matplotlib jupyterlab
conda activate geo
```

Con `pip` también funciona (`pip install geopandas rasterio rasterstats scikit-image matplotlib`), pero en Windows conda resuelve mejor GDAL. La sección 5 de [GDAL y Python](09-curvas-de-nivel/gdal-y-python.md) detalla la configuración en VS Code.

## Datos de ejemplo

- Capítulo 1: el predio y el NDVI se generan con el propio código del capítulo; no requiere descargas.
- Capítulo 9: [`dem_utm.tif`](09-curvas-de-nivel/datos/dem_utm.tif), [`dem_geograficas.tif`](09-curvas-de-nivel/datos/dem_geograficas.tif) y [`sombreado.tif`](09-curvas-de-nivel/datos/sombreado.tif), usados por el laboratorio.

## Convenciones

| Tema | Convención |
|---|---|
| CRS para medir | UTM 18S (`EPSG:32718`) al oeste de 72° O; UTM 19S (`EPSG:32719`) al este |
| CRS para compartir | WGS 84 (`EPSG:4326`), con coordenadas en orden longitud, latitud |
| Formato vectorial | GeoPackage (`.gpkg`) por defecto; GeoParquet para datos grandes |
| Formato ráster | GeoTIFF con `nodata` declarado; COG si se publicará en la web |
| Superficies | Hectáreas con dos decimales |
| Estadísticas zonales | Reportar siempre `count` y `std` junto a la media, y declarar `all_touched` |

!!! example "Casos aplicados"
    [Límites administrativos de Chile con Overture Maps](https://zelaznog-j.github.io/proyectos/overture/) (capítulo 8) · [Precipitación en Chile con ERA5](https://zelaznog-j.github.io/proyectos/precipitacion-era5/) (capítulo 10)
