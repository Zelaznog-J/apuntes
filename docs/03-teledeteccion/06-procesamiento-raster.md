# Procesamiento raster y cálculo de índices en Python

!!! question "Pregunta guía"
    ¿Cómo convierto una imagen cruda en un mapa confiable del lote?

> **Cómo leer este capítulo.** Aquí cierras el circuito: la imagen que exportaste en el [capítulo 5](05-acceso-imagenes.md) se transforma en un mapa de índice que puedes abrir en QGIS. El código fue ejecutado de punta a punta sobre un GeoTIFF de prueba con la misma estructura que el del [capítulo 5](05-acceso-imagenes.md) (8 bandas, 10 m, UTM).

---

## Objetivos

Al terminar, podrás:

1. **Leer y manipular** rasters con `rasterio` y `xarray`/`rioxarray`.
2. **Enmascarar nubes** antes de calcular cualquier índice.
3. **Calcular índices** con álgebra de bandas (NDVI, NDRE, NDMI).
4. **Exportar mapas** en GeoTIFF listos para QGIS.

---

## 1. Anatomía de un raster georreferenciado

Un raster es una **matriz de valores** más **metadatos** que le dan sentido geográfico:

- **CRS:** sistema de coordenadas.
- **Transformada afín:** origen y tamaño de píxel; traduce cada celda a una coordenada real.
- **Valor *nodata*:** valor reservado para píxeles sin dato.
- **Tipo de dato:** entero de 16 bits para reflectancia escalada; `float32` una vez convertida a reflectancia real.

**Remuestrear o no.** Para combinar bandas de 10 y 20 m hay que llevarlas a una misma grilla. En el [capítulo 5](05-acceso-imagenes.md) la exportación con `scale=10` ya lo hizo, así que tu GeoTIFF tiene todas las bandas a 10 m. Ten presente que B5, B8A, B11 y SCL tienen información real de 20 m.

## 2. `rasterio`

Abre archivos, lee bandas como arreglos numpy, entrega el **perfil** (metadatos) y escribe rasters nuevos.

```python
import rasterio
with rasterio.open("lote_s2.tif") as src:
    print(src.crs, src.transform.a, src.width, src.height, src.count)
    print(src.descriptions)   # nombres de banda: ('B2', 'B3', 'B4', 'B5', 'B8', 'B8A', 'B11', 'SCL')
```

## 3. `xarray` y `rioxarray`

- **xarray:** arreglos con **dimensiones con nombre** (`band`, `y`, `x`, `time`), cómodos para las series del [capítulo 7](07-series-tiempo.md).
- **rioxarray:** agrega lo geoespacial: `.rio.crs`, `.rio.clip()`, `.rio.to_raster()`.

## 4. Máscaras de nubes

Enmascarar nubes es obligatorio antes de calcular un índice: una nube fina baja el NDVI y simula estrés ([capítulo 1](01-fundamentos.md)).

| Fuente | Descripción |
|---|---|
| **SCL** (clasificación de escena, L2A) | Clasifica cada píxel: vegetación, suelo, agua, nubes, sombras, cirros, nieve. Resolución de 20 m |
| **QA60** | Máscara histórica, menos precisa |
| **Cloud Score+** (Earth Engine) | Puntaje de calidad por píxel (banda `cs_cdf`); es la opción recomendada actualmente |

**Clases SCL que se aceptan como válidas en un lote de cultivo:** 4 (vegetación) y 5 (suelo desnudo). Si te interesan anegamientos, suma 6 (agua).

**Criterio agronómico:** calcula el porcentaje de píxeles válidos **dentro del lote** (no de la escena). Si es menor a ~80 %, descarta la fecha.

## 5. Álgebra de bandas

Antes de calcular un índice:

- **Separa SCL.** Es una clase, no una reflectancia: **no se divide por 10.000**.
- **Convierte a reflectancia** (÷ 10.000, igual que en el [capítulo 5](05-acceso-imagenes.md)).
- **Trabaja en `float32`.**
- **Aplica la máscara con `NaN`**, para que los píxeles inválidos no se confundan con valores reales.
- **Llama a las bandas por nombre**, no por posición. Es el error más frecuente: tras la exportación el orden es B2, B3, B4, B5, B8, B8A, B11, SCL, y la posición 4 es B5, no el NIR.

```python
import numpy as np, rioxarray
from shapely.geometry import mapping

# 1. Leer y nombrar las bandas
img = rioxarray.open_rasterio("lote_s2.tif").astype("float32")
img = img.assign_coords(band=list(img.attrs["long_name"]))   # ['B2','B3','B4','B5','B8','B8A','B11','SCL']

# 2. Recortar al lote con un buffer interno de 15 m (CRS en metros)
#    'contorno' = geometría del lote en el mismo CRS que la imagen (por ejemplo, de geopandas: gdf.to_crs(img.rio.crs))
interior = contorno.buffer(-15)
img = img.rio.clip([mapping(interior)], crs=img.rio.crs, drop=False)
dentro = img.sel(band="B4").notnull()          # píxeles dentro del lote

# 3. Máscara de nubes con SCL
valido = img.sel(band="SCL").isin([4, 5])
refl = (img.drop_sel(band="SCL") / 10000).where(valido)
b = lambda nombre: refl.sel(band=nombre)

# 4. Porcentaje de píxeles válidos dentro del lote
pct_validos = float(valido.where(dentro).sum() / dentro.sum()) * 100
print(f"Píxeles válidos: {pct_validos:.1f} %")     # si < 80 %, descartar la fecha

# 5. Índices (mismas fórmulas y bandas del [capítulo 3](03-indices-vegetacion.md))
ndvi = (b("B8")  - b("B4"))  / (b("B8")  + b("B4"))
ndre = (b("B8A") - b("B5"))  / (b("B8A") + b("B5"))
ndmi = (b("B8A") - b("B11")) / (b("B8A") + b("B11"))
ndvi = ndvi.where((ndvi >= -1) & (ndvi <= 1))

# 6. Exportar
ndvi.attrs.pop("long_name", None)               # evita un error de nombres al escribir una sola banda
ndvi.rio.to_raster("ndvi_lote.tif", dtype="float32")
```

> **Prueba de referencia.** Con el GeoTIFF sintético de prueba (60 × 60 píxeles, 8 bandas), el código entrega NDVI ≈ 0,84, NDRE ≈ 0,59 y NDMI ≈ 0,39, con ~90 % de píxeles válidos dentro del lote. Son valores de un cultivo sano e ilustran el orden de magnitud esperado.

## 6. Mapas por lote

Para que un mapa sea interpretable y comparable:

- **Paleta adecuada.** Rojo–amarillo–verde es habitual, pero no se distingue bien con daltonismo; considera `viridis` o una paleta de un solo color.
- **Rango fijo** entre fechas (por ejemplo, 0 a 1), para que un cambio de color sea un cambio real del índice y no un reescalado automático.
- **Estadísticas del lote:** media, desvío estándar, percentiles y coeficiente de variación (CV = desvío / media). El CV resume cuán heterogéneo es el lote.

```python
import matplotlib.pyplot as plt
v = ndvi.values[np.isfinite(ndvi.values)]
print(f"Media {v.mean():.2f} · Desv. {v.std():.3f} · P10 {np.percentile(v,10):.2f} · "
      f"P90 {np.percentile(v,90):.2f} · CV {100*v.std()/v.mean():.1f} %")

plt.imshow(ndvi.squeeze(), cmap="RdYlGn", vmin=0, vmax=1)
plt.colorbar(label="NDVI"); plt.title("NDVI del lote"); plt.show()
```

## 7. Exportación e integración con QGIS

Exporta como **GeoTIFF** con el **CRS correcto** (UTM de tu zona, en metros). En QGIS:

1. Abre el GeoTIFF y el contorno del lote.
2. Aplica **simbología por rangos** (por ejemplo, 5 clases).
3. Superpón una imagen base para dar contexto.

---

## Práctica guiada

1. **Leer** la imagen del [capítulo 5](05-acceso-imagenes.md) e inspeccionar CRS, tamaño de píxel y bandas.
2. **Aplicar la máscara** con SCL (o con Cloud Score+ si trabajas directamente en GEE).
3. **Calcular NDVI y NDRE** y obtener las estadísticas del lote.
4. **Generar mapas** con matplotlib usando la misma escala de color.
5. **Exportar a GeoTIFF** y abrirlo en QGIS con 5 clases.

## Producto esperado

Un flujo reproducible "imagen cruda → mapa de índice" y el GeoTIFF de tu lote abierto en QGIS.

## Errores frecuentes

- **Elegir bandas por posición** en vez de por nombre.
- **Dividir SCL por 10.000** junto con las reflectancias (arruina la máscara).
- **No escalar por 10.000** las reflectancias.
- **Comparar mapas con escalas de color distintas.**
- **Efecto de borde por píxeles mixtos:** aplica un buffer interno de 10–20 m. El buffer en metros solo funciona si el contorno está en un CRS proyectado (UTM), no en grados.
- **Usar pocos píxeles válidos** sin avisar: informa siempre el porcentaje.

## Ideas clave de cierre

1. Un raster es una matriz más metadatos; sin ellos no tiene sentido espacial.
2. Enmascarar nubes no es opcional: separa un mapa confiable de uno con artefactos.
3. `rasterio` trabaja directo con archivos; `xarray`/`rioxarray` aportan dimensiones con nombre, útiles para las series del [capítulo 7](07-series-tiempo.md).
4. Para comparar fechas, mantén la misma escala de color y el mismo criterio de máscara.
5. El GeoTIFF es el punto de encuentro entre Python y QGIS.
