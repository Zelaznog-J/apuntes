# 5. Interacciones ráster-vector

Ráster y vector no son mundos separados: pueden **extraerse información mutuamente y convertirse entre sí**.

## Integrar ambos modelos

**Ráster y vector pueden integrarse en un mismo flujo de análisis.** Este capítulo conecta ambos modelos mediante enmascaramiento, recorte, extracción, rasterización y vectorización.

## Enmascaramiento y recorte

**El enmascaramiento mantiene la extensión del ráster pero convierte en `nodata` las celdas fuera de una geometría vectorial.** Es útil para limitar el análisis a un área de interés sin cambiar el tamaño espacial del archivo.

**El recorte reduce la extensión del ráster.** Con `crop=True`, el resultado se limita espacialmente a la geometría o a su envolvente, por lo que cambian dimensiones y transformación espacial.

**Ráster y vector deben estar en el mismo CRS antes de combinarlos.** Normalmente resulta más sencillo reproyectar la capa vectorial al CRS del ráster.

## Extracción de valores ráster

**La extracción a puntos obtiene el valor ráster en ubicaciones específicas.** `rasterstats.point_query()` permite asociar, por ejemplo, elevación, temperatura o índice de vegetación a una capa de puntos.

**La extracción a líneas puede construirse muestreando puntos a intervalos regulares.** Esto permite obtener perfiles continuos, como un perfil de elevación a lo largo de una transecta.

**La extracción a polígonos produce estadísticas zonales.** `rasterstats.zonal_stats()` resume las celdas dentro de cada polígono mediante estadísticas como media, mínimo, máximo o conteo.

## Rasterización

**La rasterización convierte entidades vectoriales en celdas ráster.** Puntos, líneas y polígonos pueden transformarse en una cuadrícula y asignar valores a las celdas mediante `rasterio.features.rasterize()`.

**La rasterización depende de una plantilla espacial.** La resolución, extensión, `transform`, dimensiones y opciones como `all_touched` determinan qué píxeles reciben valores.

## Vectorización

**La vectorización realiza el proceso inverso.** Los datos ráster pueden convertirse a polígonos, puntos o curvas de nivel; `rasterio.features.shapes()` permite obtener geometrías poligonales asociadas a valores de píxel.

!!! note "Idea clave del capítulo"
    Ráster y vector no son mundos separados; pueden **extraerse información mutuamente y convertirse entre sí**.
