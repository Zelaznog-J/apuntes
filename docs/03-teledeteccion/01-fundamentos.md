# Fundamentos de teledetección

!!! question "Pregunta guía"
    ¿Qué "ve" un satélite cuando observa un cultivo?

> **Cómo leer este capítulo.** Cada sección parte con la idea en palabras simples y luego da el detalle técnico. Las cifras entre paréntesis son valores de referencia: sirven para orientarse, no para reemplazar la ficha técnica de cada sensor.

---

## Objetivos

Al terminar, podrás:

1. **Explicar** cómo un sensor registra la energía que refleja la superficie y qué le pasa a esa señal en el camino.
2. **Interpretar** las firmas espectrales de vegetación sana, vegetación estresada, suelo y agua.
3. **Elegir** el satélite y el nivel de producto según las cuatro resoluciones y la pregunta agronómica.
4. **Reconocer** que un índice como el NDVI *indica* pero no *diagnostica*.

---

## 1. ¿Qué es la teledetección?

**En simple:** conocer algo sin tocarlo, a partir de la luz (u otra energía) que devuelve. Un satélite hace lo mismo que tu ojo, pero con más "colores" de los que tú ves.

**Definición técnica:** obtener información de la superficie terrestre **sin contacto físico**, midiendo la **energía electromagnética** que refleja o emite, con sensores instalados en satélites, aviones o drones.

### Sensores pasivos y activos

| Tipo | Cómo funcionan | Ejemplos |
|---|---|---|
| **Pasivos** (ópticos y térmicos) | Miden energía de una fuente externa: luz solar reflejada o calor que emite la superficie | Sentinel-2, Landsat |
| **Activos** (radar / SAR) | Emiten su propia señal de microondas y registran el eco. Funcionan de día y de noche y atraviesan las nubes | Sentinel-1 (gratuito), ICEYE (comercial) |

### El recorrido de la señal (cadena del dato)

En un sensor óptico, la luz pasa **dos veces** por la atmósfera antes de ser una imagen útil:

1. **Sol** (la fuente).
2. **Atmósfera**, de bajada.
3. **Superficie**: el cultivo refleja o absorbe.
4. **Atmósfera**, de subida.
5. **Sensor** a bordo del satélite.
6. **Estación terrena**, que recibe la señal.
7. **Producto**: la imagen ya procesada.

**Por qué importa:** la atmósfera dispersa y absorbe parte de la señal en los dos trayectos. Por eso las imágenes se corrigen, y de ahí nacen los niveles de producto L1C y L2A (sección 5).

*En un radar la fuente es el propio sensor:* la antena emite y recibe. Por eso no depende de la luz del sol y las nubes lo afectan mucho menos.

### Órbitas: de dónde viene la "revisita"

| Órbita | Cómo es | Uso |
|---|---|---|
| **Heliosincrónica** | Casi polar, a ~700–800 km de altura. Pasa siempre a la **misma hora solar local** (Sentinel-2 ~10:30; Landsat ~10:00), así la iluminación es comparable entre fechas. La Tierra gira bajo el satélite y cada pasada cubre una franja distinta; el tiempo que tarda en volver al mismo punto es la **revisita** | Sentinel-2, Landsat, MODIS, Sentinel-1 |
| **Geoestacionaria** | A ~35.786 km sobre el ecuador, gira al mismo ritmo que la Tierra y mira siempre la misma región, con imágenes cada pocos minutos. Por la distancia, el píxel es de kilómetros | Meteorología (serie GOES) |

---

## 2. El espectro electromagnético y la vegetación

### Regiones que importan en agronomía

| Región | Longitud de onda aprox. | Para qué sirve |
|---|---|---|
| Azul | ~490 nm | La clorofila la absorbe con fuerza |
| Verde | ~560 nm | Se refleja en parte: por eso vemos verdes las hojas |
| Rojo | ~665 nm | La clorofila la absorbe |
| Borde rojo (*red edge*) | ~700–780 nm | Transición muy sensible al estado fisiológico |
| Infrarrojo cercano (NIR) | ~780–900 nm | Lo refleja con fuerza el tejido sano |
| Infrarrojo de onda corta (SWIR) | ~1.600 y ~2.200 nm | Lo absorbe el agua de la hoja |

*Reflectancia:* fracción de la luz incidente que la superficie devuelve (de 0 a 1). Es la magnitud que permite comparar fechas y sensores.

### Qué le pasa a la luz dentro de la hoja

La hoja tiene, de arriba hacia abajo: cutícula, epidermis, mesófilo en empalizada, mesófilo esponjoso, epidermis inferior con estomas y cutícula.

- **Azul y rojo:** los absorbe la clorofila del mesófilo en empalizada.
- **Verde:** se refleja en parte.
- **NIR:** rebota en las interfaces entre pared celular y aire del mesófilo esponjoso y sale hacia arriba. Por eso la vegetación sana es muy brillante en NIR.
- **SWIR:** lo absorbe el agua del tejido.

### Pigmentos

| Pigmento | Picos de absorción |
|---|---|
| Clorofila *a* | ~430 y ~662 nm |
| Clorofila *b* | ~453 y ~642 nm |
| Carotenoides | ~400–520 nm (parte de la absorción en el azul) |

---

## 3. Firmas espectrales

**En simple:** la "huella digital" de una superficie: cuánta luz devuelve en cada color.

### Cómo leer cada firma

- **Vegetación sana:** poco azul y poco rojo (clorofila), un pequeño pico en verde, salto brusco en el borde rojo, NIR alto y caída en SWIR por el agua foliar.
- **Vegetación estresada o senescente:** sube el rojo (menos clorofila), baja el NIR, el borde rojo se corre hacia longitudes menores y **sube el SWIR** (menos agua en el tejido).
- **Suelo:** curva suave y ascendente. Cambia con humedad, materia orgánica y textura; un suelo húmedo se ve más oscuro.
- **Agua:** reflectancia muy baja, casi nula en NIR y SWIR. Por eso contrasta tanto con la vegetación.

### Cuidado con el borde rojo

Su desplazamiento es una señal temprana de estrés, pero **pequeña y ambigua**:

- Mide pocos nanómetros: solo se ve con bandas angostas (B5–B7 de Sentinel-2).
- También cambia con el índice de área foliar y la estructura del cultivo, no solo con el estrés.
- Es la base física del NDRE, que verás en el [capítulo 3](03-indices-vegetacion.md).

---

## 4. Las cuatro resoluciones

| Resolución | Qué mide | Ejemplo |
|---|---|---|
| **Espacial** | Tamaño del píxel en el terreno | 10 m × 10 m en Sentinel-2 |
| **Espectral** | Cuántas bandas hay, dónde están y qué tan anchas son | 13 bandas en Sentinel-2 |
| **Temporal** | Cada cuánto se observa el mismo lugar | ~5 días en Sentinel-2 con dos satélites operativos |
| **Radiométrica** | Cuántos niveles de gris distingue | 8 bits = 256; 12 bits = 4.096 (Sentinel-2 y Landsat 8); 14 bits = 16.384 (Landsat 9) |

**Regla práctica de resolución espacial:** el lote debe contener varios píxeles "puros" (sin borde), lejos de caminos y cercos.

**Revisita teórica y efectiva.** La cifra de revisita es el máximo posible; con nubes, la frecuencia útil es menor.

### Idea clave: las resoluciones compiten entre sí

- Más detalle espacial suele significar franja más angosta, menos revisita o costo comercial.
- Más bandas angostas reciben menos energía cada una: cuesta mantener la calidad.
- **Manda la pregunta agronómica:** ¿lote, predio o región? ¿seguimiento semanal o por temporada?

### Satélites de observación agrícola

| Satélite | Píxel | Revisita | Qué aporta | Acceso |
|---|---|---|---|---|
| **Sentinel-2** (ESA) | 10 / 20 / 60 m | ~5 días (2 satélites) | 13 bandas, 3 de borde rojo | Gratuito · el "caballo de batalla" del lote |
| **Landsat 8 y 9** (NASA/USGS) | 30 m (térmico 100 m) | 16 días c/u · ~8 juntos | SWIR y térmico; el programa tiene archivo desde 1972 | Gratuito · series largas |
| **MODIS** (Terra/Aqua) | 250–1.000 m | Diaria | Escala regional. Las misiones están al final de su vida útil; VIIRS continúa la serie | Gratuito · monitoreo regional |
| **PlanetScope** | ~3 m | Casi diaria | 4 u 8 bandas | Comercial · detalle dentro del lote |
| **Sentinel-1** (ESA) | ~10 m (SAR banda C) | 6–12 días según cuántos satélites operen | Radar: ve a través de las nubes | Gratuito · zonas nubosas |

*Nota:* Landsat 8 y 9 se lanzaron en 2013 y 2021; "desde 1972" se refiere al programa Landsat completo.

**Síntesis:** Sentinel-2 equilibra detalle y frecuencia para el lote; Landsat aporta la historia larga; MODIS, la escala regional; PlanetScope, el detalle fino; Sentinel-1, la observación con cielo nublado.

---

## 5. Niveles de producto: L1C frente a L2A

| | Sentinel-2 · Nivel 1C | Sentinel-2 · Nivel 2A |
|---|---|---|
| **Qué representa** | Reflectancia en el tope de la atmósfera (TOA) | Reflectancia de superficie (BOA) |
| **Corrección** | Corregida y ortorrectificada, pero **incluye el efecto de la atmósfera** | Corrección atmosférica con **Sen2Cor**; incluye la capa de clasificación de escena (**SCL**) para enmascarar nubes y sombras |
| **Cuándo usarla** | Visualización rápida o si harás tu propia corrección | **Recomendada para índices y series de tiempo** |

### Errores frecuentes

| Error | Cómo evitarlo |
|---|---|
| Calcular índices con L1C | Usar L2A |
| No enmascarar nubes ni sombras | Usar SCL (o Cloud Score+): una nube fina baja el NDVI y simula estrés |
| Olvidar el factor de escala | S2 L2A: dividir por 10.000. Desde el 25‑ene‑2022 (procesamiento 04.00) los datos originales traen un desplazamiento de +1.000; la colección *HARMONIZED* de Earth Engine ya lo corrige ([capítulo 5](05-acceso-imagenes.md)). Landsat Collection 2 L2: ND × 0,0000275 − 0,2 |
| Mezclar bandas de 10, 20 y 60 m | Llevarlas a una misma grilla antes de combinarlas |
| Incluir píxeles del borde del lote | Aplicar un *buffer* negativo (10–20 m) |
| Comparar fechas sin mirar la fenología | Comparar estados de desarrollo equivalentes |
| Leer un NDVI bajo como estrés | Descartar antes suelo expuesto, cosecha, fenología y nubes |

---

## 6. El límite de los índices

Durante décadas se trabajó con fórmulas fijas como el **NDVI** = (NIR − Rojo) / (NIR + Rojo), que va de −1 a 1.

**Limitaciones:**

- **Nubes finas:** bajan el valor sin que el cultivo cambie.
- **Saturación:** con mucha biomasa (índice de área foliar > ~3) el índice deja de crecer.
- **Malezas y suelo:** se mezclan en el píxel y distorsionan la lectura.

**Valores orientativos de NDVI:** agua < 0; suelo desnudo ~0,1–0,2; cultivo en pleno desarrollo ~0,6–0,9 (dependen de cultivo, suelo y sensor).

**Idea central de la sesión: un índice indica, no diagnostica.** Un NDVI bajo dice "algo pasa", no "qué pasa": puede ser estrés hídrico, plaga, suelo expuesto, cosecha reciente o simplemente la fenología.

Existen índices que mitigan algunos problemas (EVI, SAVI, NDRE, NDMI). Los **calcularás y compararás en el [capítulo 3](03-indices-vegetacion.md)**; por ahora basta saber que ninguno elimina la inespecificidad de fondo.

> **Adelanto — modelos que aprenden del planeta.** Los *modelos fundacionales geoespaciales* (como Prithvi o Clay) y los *embeddings* no usan fórmulas fijas: aprenden patrones de grandes volúmenes de imágenes. Se presentan en el cierre del **[capítulo 8](08-machine-learning.md)** y se retoman en "Recursos para continuar" del **[capítulo 9](09-integracion.md)**. Por ahora solo importa una idea: complementan, pero no reemplazan, la verificación en terreno.

---

## Práctica guiada

1. Abre **Copernicus Browser** o **EO Browser** (gratuitos, con registro) y ubica una zona agrícola conocida.
2. Filtra **Sentinel-2 L2A** por fecha y porcentaje de nubes.
3. Compara visualizaciones: **color natural** (B4‑B3‑B2), **falso color infrarrojo** (B8‑B4‑B3; la vegetación se ve roja) y **agricultura** (B11‑B8‑B2).
4. Con la herramienta de punto o de perfil, mira la reflectancia en un lote con cultivo, uno en barbecho y un cuerpo de agua.
5. **Comparación de dos fechas:** elige un lote conocido y dos fechas sin nubes; compara color natural, falso color y NDVI. Anota qué cambió y qué otras causas, además del estrés, podrían explicarlo.

## Producto esperado

Ficha breve con tres capturas (color natural, falso color, comparación entre fechas) y una interpretación de 5 líneas.

## Errores frecuentes en la práctica

Confundir L1C con L2A; tomar la sombra de una nube por suelo húmedo o por estrés.

**Avance del proyecto:** elegir el lote del proyecto integrador y obtener su contorno (KML dibujado en Google Earth o shapefile). Se usa desde el [capítulo 5](05-acceso-imagenes.md).

---

## Ideas clave de cierre

1. Un sensor mide energía reflejada o emitida; la atmósfera la altera dos veces en el camino.
2. La hoja sana absorbe azul y rojo, refleja NIR y absorbe SWIR por su agua.
3. El estrés sube el rojo y el SWIR, baja el NIR y corre el borde rojo.
4. Las cuatro resoluciones compiten: el satélite se elige según la pregunta, no al revés.
5. Usa L2A, enmascara nubes y recuerda: un índice indica, no diagnostica.

## Referencias

- Chuvieco, E. *Fundamentals of Satellite Remote Sensing*. CRC Press.
- Jensen, J. R. *Remote Sensing of the Environment*. Pearson.
- ESA. Documentación de Sentinel-2 (SentiWiki) y Sen2Cor.
- USGS. Documentación de Landsat Collection 2.
- Jakubik, J. et al. (2023). *Foundation Models for Generalist Geospatial Artificial Intelligence* (Prithvi). arXiv.

*Créditos de imágenes: espectros y gráficos de elaboración propia, con curvas ilustrativas.*
