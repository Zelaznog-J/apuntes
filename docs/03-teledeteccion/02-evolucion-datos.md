# Evolución de la tecnología satelital y apertura de los datos

!!! question "Pregunta guía"
    ¿Por qué hoy cualquiera puede acceder gratis a lo que hace pocas décadas costaba cientos o miles de dólares por imagen?

> **Cómo leer este capítulo.** Es el capítulo "histórico" del libro: cuenta cómo llegamos a tener datos abiertos y por qué eso importa para el trabajo de lote. Las fechas son hitos de referencia; no hace falta memorizarlas, sí entender la secuencia.

---

## Objetivos

Al terminar, podrás:

1. **Reconocer** los hitos que marcaron la observación satelital de la Tierra.
2. **Explicar** cómo las políticas de datos abiertos (Landsat y Copernicus) hicieron accesible la teledetección agrícola.
3. **Ubicar** las principales fuentes de datos abiertas y comerciales disponibles hoy.

---

## 1. Orígenes de la observación satelital

Dos linajes distintos dan origen a la observación de la Tierra desde el espacio:

- **Programas militares de reconocimiento.** Por ejemplo CORONA (EE.UU., década de 1960), cuyas imágenes se mantuvieron clasificadas por décadas.
- **Satélites meteorológicos.** TIROS‑1 (1960) fue el primer satélite meteorológico operativo; miraba nubes y clima, no cultivos.

El giro hacia la **observación civil de recursos terrestres** llega en **1972** con **ERTS‑1**, rebautizado **Landsat 1**: el primer satélite diseñado para monitorear de forma sistemática la superficie terrestre, incluida la agricultura.

## 2. La era de acceso restringido (1972–2008)

Durante más de tres décadas, las imágenes Landsat y las de otros sensores (por ejemplo **SPOT**, Francia, 1986) se vendían a precios de **cientos a miles de dólares por escena**. En la práctica:

- Accedían gobiernos, grandes empresas y centros de investigación con financiamiento específico.
- Analizar **un lote** de un productor mediano o pequeño no era viable: una sola escena podía costar más que el beneficio esperado.
- El uso agrícola se limitaba a proyectos de investigación o a operaciones muy grandes que podían amortizar el costo.

## 3. El punto de inflexión: se abre el archivo Landsat (2008)

En 2008, el **USGS** y la **NASA** decidieron liberar **todo el archivo histórico Landsat**, con más de tres décadas de imágenes.

**Efecto documentado:** un aumento rápido y muy marcado en las descargas y en las publicaciones científicas que usan Landsat, apenas desapareció la barrera del costo.

Es, en los hechos, el comienzo del "big data" en teledetección: de un día para otro, décadas de imágenes de toda la superficie terrestre quedaron disponibles sin costo.

## 4. Copernicus y la constelación Sentinel (ESA, desde 2014)

**Copernicus** es el programa europeo de observación de la Tierra. A diferencia de Landsat —que se abrió después de años bajo pago—, fue diseñado **desde el inicio** con datos **gratuitos y abiertos**.

- **Sentinel‑1** (radar) se lanzó en 2014 y **Sentinel‑2** (óptico) en 2015. Cada misión es una constelación de varios satélites, para ganar frecuencia de revisita.
- La inversión pública sostenida en el tiempo no tiene precedentes para datos de libre acceso.
- **Sentinel‑2** se volvió el sensor de referencia para el lote: píxeles de 10–20 m, revisita de ~5 días con dos satélites operativos y tres bandas de borde rojo (clave para los índices del [capítulo 3](03-indices-vegetacion.md)).

*Estado de la constelación:* Sentinel‑2B (2017) y Sentinel‑2C (lanzado en 2024) operan juntos desde 2025, tras reemplazar 2C al 2A. Para el usuario no cambia nada: la colección sigue siendo continua.

## 5. De la escena aislada a la nube

Aunque los datos fueran gratuitos, **descargar y procesar** terabytes por campaña en un computador personal seguía siendo una barrera técnica. Surgieron plataformas que procesan **junto a los datos**:

- **Google Earth Engine** (2010): catálogo de petabytes con cómputo en servidores de Google.
- **STAC** (*SpatioTemporal Asset Catalog*): estándar abierto para buscar y describir imágenes de forma uniforme entre proveedores.
- **Microsoft Planetary Computer** y **AWS Open Data**: catálogos abiertos en la nube, con APIs estándar.

**Cambio de paradigma:** de *"llevar los datos al código"* (descargar todo) a *"llevar el código a los datos"* (procesar donde ya están almacenados).

## 6. Datos listos para analizar (*Analysis Ready Data*, ARD)

Son productos **ya corregidos** (atmosférica y geométricamente) y **armonizados**, para analizar sin preprocesamiento extenso.

**Ejemplo que usarás desde el [capítulo 5](05-acceso-imagenes.md):** la colección `COPERNICUS/S2_SR_HARMONIZED` de Earth Engine. Desde el 25 de enero de 2022, ESA suma un **desplazamiento de +1.000** a los valores de Sentinel‑2 (procesamiento 04.00). La versión *harmonized* lo corrige, de modo que las imágenes antiguas y recientes son comparables.

## 7. El ecosistema actual: lo abierto y lo comercial conviven

| Tipo | Ejemplos | Características |
|---|---|---|
| **Datos abiertos** | Landsat, Sentinel, MODIS/VIIRS | Píxel de 10 a 1.000 m, revisita de días, gratuitos |
| **Datos comerciales** | PlanetScope (~3 m, casi diaria), Maxar/WorldView (submétrico) | Más detalle y frecuencia, con costo por imagen o suscripción (hay programas académicos) |
| **Smallsats y cubesats** | Constelaciones de decenas a cientos de satélites pequeños | Abarataron el lanzamiento y la operación de sensores |
| **Radar comercial** | ICEYE, Capella | Observación bajo nubes con alta resolución |

## 8. Qué significa para la agricultura

La apertura de datos es la condición que permite que este libro exista: sin ella, la agricultura de precisión satelital seguiría siendo un servicio caro y tercerizado.

**Misiones que ampliarán la disponibilidad:**

- **NISAR** (NASA–ISRO): radar de alta resolución con datos abiertos, lanzado el 30 de julio de 2025.
- **Próximas generaciones de Sentinel‑2**, con nuevas bandas previstas.

### Línea de tiempo de referencia

| Año | Hito |
|---|---|
| 1960 | TIROS‑1, primer satélite meteorológico operativo |
| 1960s | Reconocimiento militar (CORONA) |
| 1972 | Landsat 1 (ERTS‑1) |
| 1986 | SPOT 1 (Francia): imágenes comerciales |
| 2008 | USGS/NASA abren el archivo Landsat |
| 2010 | Google Earth Engine |
| 2014–2015 | Sentinel‑1 y Sentinel‑2 (Copernicus, datos abiertos) |
| 2013 / 2021 | Landsat 8 / Landsat 9 |
| 2025 | Sentinel‑2C operativo; lanzamiento de NISAR |

---

## Práctica guiada

1. **Imágenes históricas.** En **USGS EarthExplorer** o en un catálogo STAC (Earth Search / Planetary Computer), busca imágenes Landsat de las décadas de 1970–1980 sobre una zona agrícola conocida. Anota su calidad y limitaciones frente a una imagen Sentinel‑2 actual.
2. **Salto en frecuencia.** Para el mismo lote, cuenta cuántas imágenes hay por año en 1985, 2000, 2015 y 2025.
3. **Abierto frente a comercial.** En **Copernicus Browser** observa la política de acceso de Sentinel‑2 y compárala con la vista de muestra de un catálogo comercial (por ejemplo Planet Explorer): resolución, frecuencia y costo.
4. **Línea de tiempo.** Arma en papel o pizarra digital la línea de tiempo con los hitos que encontraste.

## Producto esperado

- **Línea de tiempo** con al menos **seis hitos**.
- **Tabla comparativa** de tres fuentes (una histórica de acceso restringido, una abierta actual y una comercial actual) con resolución espacial, revisita y costo.

## Errores frecuentes

- Pensar que los datos satelitales **siempre fueron gratuitos**.
- Creer que la revisita de días es lo normal: es un fenómeno reciente.
- Confundir **datos abiertos** con **procesamiento fácil**: tener los datos gratis no resuelve el problema de la escala, y eso motiva los capítulos de programación y nube.

## Ideas clave de cierre

1. La observación satelital nace de lo militar y lo meteorológico; se orienta a recursos terrestres con Landsat 1 (1972).
2. Por más de 30 años, el costo por escena dejó la teledetección fuera del alcance de la mayoría de los productores.
3. Dos hitos democratizaron el acceso: la apertura de Landsat (2008) y el diseño abierto de Copernicus.
4. La nube (Earth Engine, STAC) permite procesar datos gratuitos pero voluminosos sin descargarlos.
5. Hoy conviven datos abiertos y comerciales, y esa oferta seguirá creciendo.

**Puente hacia el [capítulo 3](03-indices-vegetacion.md):** con el acceso resuelto, la pregunta es cómo transformar reflectancias en información agronómica. Eso son los índices de vegetación.
