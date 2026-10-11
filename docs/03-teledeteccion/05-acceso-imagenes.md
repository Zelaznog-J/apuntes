# Acceso a imágenes satelitales con Python

!!! question "Pregunta guía"
    ¿Cómo consigo todas las imágenes de mi lote sin descargarlas una por una?

> **Cómo leer este capítulo.** Este capítulo conecta tu lote con los datos satelitales. La idea central es simple: en vez de bajar imágenes a tu computador, **le pides a un servidor en la nube solo lo que necesitas**. El script de referencia sirve como plantilla: se cambia el contorno y las fechas y funciona para cualquier lote.
>
!!! warning "Código no ejecutado"
    El código de Earth Engine de este capítulo sigue la API oficial, pero no se ha ejecutado de punta a punta. Pruébalo con tu propio proyecto de Google Cloud.

---

## Objetivos

Al terminar, podrás:

1. **Autenticarte** en Google Earth Engine (GEE).
2. **Filtrar** colecciones por fecha, nubosidad y área de interés (AOI).
3. **Obtener** imágenes Sentinel‑2 recortadas a tu lote, listas para el [capítulo 6](06-procesamiento-raster.md).

---

## 1. Qué es una API y por qué usarla

Una **API** (interfaz de programación) permite pedir datos a un catálogo desde un script, sin navegar un visor ni hacer clic imagen por imagen. La diferencia con los capítulos anteriores: **el procesamiento ocurre en los servidores del proveedor**, no en tu computador. Es la idea de "llevar el código a los datos" del [capítulo 2](02-evolucion-datos.md).

## 2. Fuentes de datos

- **Google Earth Engine (GEE):** catálogo de petabytes con cómputo en servidores de Google. Gratuito para uso no comercial; requiere un proyecto de Google Cloud registrado.
- **Copernicus Data Space Ecosystem:** plataforma oficial europea para datos Sentinel, con APIs propias (STAC, OData, Sentinel Hub).
- **Catálogos STAC** (mención): Microsoft Planetary Computer o Earth Search, alternativas abiertas basadas en el estándar visto en el [capítulo 2](02-evolucion-datos.md).

## 3. El modelo de datos de GEE

Cuatro objetos estructuran cualquier script:

| Objeto | Qué es |
|---|---|
| `Image` | Una escena, con sus bandas |
| `ImageCollection` | Un conjunto de escenas (por ejemplo, todas las de tu zona en una campaña) |
| `Geometry` | Una forma geográfica: punto, línea o polígono |
| `Feature` / `FeatureCollection` | Datos vectoriales, como el contorno de un lote con sus atributos |

**Servidor y cliente.** Los objetos `ee.*` **no contienen datos en tu memoria**: son instrucciones que se ejecutan en los servidores de Google. Por eso un `print()` sobre un objeto de GEE puede no mostrar lo que esperas. Para traer un valor a tu computador se usa `.getInfo()`. Úsalo con moderación: cada llamada es un viaje de ida y vuelta al servidor.

## 4. Colección Sentinel‑2 recomendada

La colección de referencia es **`COPERNICUS/S2_SR_HARMONIZED`** (reflectancia de superficie, nivel L2A).

- **Qué significa "harmonized".** Desde el 25 de enero de 2022 (procesamiento 04.00), ESA suma un **desplazamiento de +1.000** a los valores. La versión *harmonized* lo quita para que las fechas antiguas y recientes sean comparables.
- **Escala.** Los valores vienen multiplicados por 10.000. **Divide por 10.000** para obtener reflectancia de 0 a 1. Con esta colección no hay que restar nada más.
- *Si usaras la colección sin "harmonized"*, para imágenes posteriores a enero de 2022 la reflectancia sería (valor − 1.000) / 10.000.
- **Capa de calidad.** La banda `SCL` (clasificación de escena) viene a 20 m y es la que usarás en el [capítulo 6](06-procesamiento-raster.md) para enmascarar nubes.

## 5. Filtros de colección

Se combinan tres filtros:

- **Fecha:** `.filterDate()`.
- **Área:** `.filterBounds()`, con el contorno del lote.
- **Nubosidad:** propiedad `CLOUDY_PIXEL_PERCENTAGE`.

> **Advertencia.** Ese porcentaje corresponde a **toda la escena** (~110 km de lado), no a tu lote. Una escena "muy nublada" puede tener tu lote despejado, y al revés. Por eso se filtra con un umbral amplio y la calidad real del lote se evalúa después, con la máscara del [capítulo 6](06-procesamiento-raster.md).

## 6. El área de interés (AOI)

El contorno del lote (tarea del [capítulo 1](01-fundamentos.md)) se carga con **geopandas** o con **geemap**, y se convierte en geometría de Earth Engine.

```python
import geemap
lote = geemap.shp_to_ee("lote.shp").geometry()     # si es shapefile
# lote = geemap.kml_to_ee("lote.kml").geometry()   # si es KML
```

Dos cuidados con las coordenadas:

- **Orden:** Earth Engine usa **[longitud, latitud]**, no al revés.
- **Sistema:** EPSG:4326 está en grados; las proyecciones UTM están en metros. Para exportar conviene el UTM de tu zona (por ejemplo, EPSG:32719 = UTM 19 Sur, zona central de Chile).

### Script de referencia

```python
import ee, pandas as pd

ee.Authenticate()                          # abre una ventana para iniciar sesión
ee.Initialize(project="mi-proyecto-gee")   # tu proyecto de Google Cloud

# --- Parámetros que cambias para cada lote/campaña ---
lote = ee.Geometry.Polygon([[[-70.70, -33.50], [-70.69, -33.50],
                             [-70.69, -33.49], [-70.70, -33.49]]])  # [lon, lat]
inicio, fin = "2024-09-01", "2025-01-31"
BANDAS = ["B2", "B3", "B4", "B5", "B8", "B8A", "B11", "SCL"]       # el orden se mantiene en el [capítulo 6](06-procesamiento-raster.md)

coleccion = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
             .filterBounds(lote)
             .filterDate(inicio, fin)
             .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30)))

print("Imágenes encontradas:", coleccion.size().getInfo())

# Tabla de fechas y nubosidad de escena
def ficha(img):
    return ee.Feature(None, {"fecha": img.date().format("YYYY-MM-dd"),
                             "nubes_escena": img.get("CLOUDY_PIXEL_PERCENTAGE")})
filas = ee.FeatureCollection(coleccion.map(ficha)).getInfo()["features"]
tabla = pd.DataFrame([f["properties"] for f in filas]).sort_values("fecha")

# Imagen menos nublada, recortada al lote
imagen = coleccion.sort("CLOUDY_PIXEL_PERCENTAGE").first().select(BANDAS).clip(lote)

# Exportación a Google Drive
tarea = ee.batch.Export.image.toDrive(
    image=imagen.toUint16(),               # todas las bandas con el mismo tipo de dato
    description="lote_s2",
    folder="teledeteccion",
    fileNamePrefix="lote_s2",
    region=lote,
    scale=10,                              # metros por píxel
    crs="EPSG:32719",                      # UTM de tu zona
    maxPixels=1e9)
tarea.start()
```

**El patrón** —autenticar, definir lote y fechas, filtrar, ordenar, recortar y exportar— se repite en los capítulos siguientes.

## 7. Exportación

- **`Export.image.toDrive`:** indica siempre **escala**, **región** y **CRS**. Omitir alguno produce resultados inesperados.
- **Bandas de distinta resolución.** Con `scale=10`, las bandas de 20 m (B5, B8A, B11, SCL) se repiten en píxeles de 10 m. Por defecto el remuestreo es de vecino más cercano, que es lo correcto para `SCL` porque son clases, no valores continuos.
- **Descarga directa** de áreas pequeñas con geemap, sin tarea asincrónica.
- **Límites:** tamaño máximo de exportación y tiempos de las tareas (pueden tardar minutos).

---

## Práctica guiada

1. **Autenticar e inicializar** Earth Engine con el proyecto de Google Cloud creado como tarea del [capítulo 4](04-python.md).
2. **Cargar** el contorno de tu lote.
3. **Filtrar** una campaña completa y listar fechas y nubosidad en una tabla de pandas.
4. **Visualizar** en un mapa interactivo (geemap) una imagen en color natural y otra en falso color.
5. **Exportar** la imagen menos nublada, recortada al lote, a Google Drive.
6. *(Opcional)* Repetir el filtro con Landsat 8/9 (`LANDSAT/LC08/C02/T1_L2`) y comparar cuántas imágenes entrega frente a Sentinel‑2.

## Producto esperado

Un script que, cambiando solo el contorno y las fechas, devuelve las imágenes de cualquier lote. Es la base de los capítulos 6 a 9.

## Errores frecuentes

- **Proyecto de Cloud no registrado** para Earth Engine.
- **Coordenadas invertidas** (usar [lat, lon] en lugar de [lon, lat]).
- **Olvidar `.clip()`:** trae la escena completa en vez de tu lote.
- **Exportar sin escala** ni CRS.
- **Pensar que "30 % de nubes" describe tu lote:** es un dato de la escena.

## Ideas clave de cierre

1. Con una API, el procesamiento pesado ocurre en servidores remotos.
2. `Image`, `ImageCollection`, `Geometry` y `Feature`/`FeatureCollection` estructuran cualquier análisis en GEE.
3. Los objetos de GEE viven en el servidor; `.getInfo()` los trae al cliente y se usa con moderación.
4. El filtro de nubosidad de escena no garantiza que tu lote esté despejado.
5. Un script con lote y fechas como parámetros es reutilizable en cualquier campaña.
