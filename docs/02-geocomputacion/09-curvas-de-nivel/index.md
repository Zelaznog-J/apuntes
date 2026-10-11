# Curvas de nivel: conceptos y métodos

!!! question "Pregunta guía"
    ¿Cómo paso de una grilla de alturas a líneas que cualquier agricultor sepa leer en el mapa del predio?

> **Cómo leer este capítulo.** Es la teoría del capítulo 9 y se lee en 40–50 minutos. Luego, [GDAL y Python](gdal-y-python.md) profundiza la generación desde un ráster, y el [laboratorio](laboratorio.ipynb) la lleva a la práctica con un DEM real. Usa lo visto en los capítulos [1](../01-panorama.md) (Rasterio y GeoPandas) y [7](../07-reproyeccion.md) (reproyección).

---

## Resultados de aprendizaje

Al finalizar este capítulo podrás:

1. Definir qué es una curva de nivel y reconocer sus propiedades.
2. Distinguir las fuentes de datos de elevación y sus limitaciones.
3. Explicar los métodos de generación de curvas de nivel (manual, desde TIN, desde ráster).
4. Elegir una equidistancia adecuada según escala, resolución y uso agronómico.
5. Generar curvas de nivel a partir de un DEM con QGIS, GDAL y Python.
6. Evaluar críticamente la calidad del resultado y corregir errores comunes.

---

## 1. Introducción: representar el relieve en un mapa

El relieve es una superficie continua en tres dimensiones, pero los mapas son planos. Representar la altura sobre un papel o una pantalla es un problema histórico de la cartografía. Se han usado sombreados, colores hipsométricos, puntos acotados y, desde el siglo XVIII, **curvas de nivel**.

En agronomía, la forma del terreno condiciona decisiones centrales: hacia dónde escurre el agua, dónde se acumula, qué tan expuesta está una ladera al sol, qué riesgo de erosión existe y cómo se trazan hileras, canales de riego o terrazas. Por eso la capacidad de generar e interpretar curvas de nivel es una competencia básica del profesional del agro.

> **Imagen sugerida 1 (al final de esta sección):** Panel comparativo de un mismo sector de ladera mostrado de cuatro formas: (a) fotografía aérea, (b) puntos acotados, (c) sombreado de relieve, (d) curvas de nivel. Pie de figura: *"Cuatro formas de representar un mismo terreno."* Sirve para que el estudiante vea que las curvas de nivel son una de varias codificaciones de la misma realidad.

---

## 2. ¿Qué es una curva de nivel?

Una **curva de nivel** (o isohipsa) es una línea que une todos los puntos de la superficie del terreno que tienen **la misma elevación** respecto a un plano de referencia, normalmente el nivel medio del mar.

Una forma intuitiva de entenderla: imagina un cerro y un lago que sube de nivel de a 10 metros. Cada vez que el agua se detiene, la línea de costa dibuja una curva de nivel.

> **Imagen sugerida 2:** Esquema didáctico en 3D de un cerro cortado por planos horizontales equidistantes (como rebanadas), con la proyección de cada intersección hacia abajo sobre un plano, formando las curvas concéntricas. Ubicación: inmediatamente después del párrafo anterior. Es la imagen conceptual clave del capítulo.

### 2.1 Elementos y vocabulario

| Término | Definición |
|---|---|
| **Cota o elevación** | Valor de altura asignado a una curva (ej. 450 m s.n.m.). |
| **Equidistancia** | Diferencia de altura constante entre dos curvas consecutivas. |
| **Curva maestra** (o directriz) | Curva más gruesa, rotulada, que aparece cada cierto número de curvas (típicamente cada 5). |
| **Curva intermedia** | Curva delgada entre dos maestras. |
| **Curva auxiliar** | Curva de equidistancia menor, agregada en zonas muy planas. |
| **Curva de depresión** | Curva que indica un hoyo cerrado, con marcas (pequeños trazos) hacia el interior. |
| **Pendiente** | Inclinación del terreno; se refleja en la separación de las curvas. |

### 2.2 Propiedades fundamentales

Estas reglas permiten interpretar y también **detectar errores** en un mapa:

1. Todos los puntos de una misma curva tienen la misma cota.
2. Las curvas de nivel **nunca se cruzan ni se bifurcan**, salvo en acantilados o cuevas (caso excepcional).
3. Toda curva es **cerrada**, aunque su cierre esté fuera del mapa.
4. **Curvas muy juntas** indican pendiente fuerte; **curvas muy separadas** indican pendiente suave.
5. Las curvas son **perpendiculares a la línea de máxima pendiente**, es decir, a la dirección en que escurre el agua.
6. En un valle o cauce, las curvas forman **"V" que apuntan aguas arriba**. En una loma o espolón forman "V" que apuntan **hacia abajo**.
7. Curvas concéntricas cerradas indican una cima o una depresión; para distinguirlas se usan las cotas o los trazos de depresión.

> **Imagen sugerida 3:** Mosaico de 6 mini-mapas de curvas de nivel con su perfil topográfico al lado: (a) ladera uniforme, (b) ladera cóncava, (c) ladera convexa, (d) valle en V, (e) loma, (f) depresión cerrada. Ubicación: al final de 2.2. Incluir flechas de escurrimiento en cada caso.

---

## 3. ¿Para qué sirven en agronomía?

Las curvas de nivel son un insumo, no un fin. Algunos usos directos:

- **Riego y drenaje:** diseño de canales, trazado de acequias, decisión entre riego por surco, goteo o aspersión según la pendiente.
- **Conservación de suelos:** cultivo en contorno, terrazas, zanjas de infiltración, líneas clave (*keyline*).
- **Plantaciones frutales y viñedos:** orientación de hileras, selección de sectores por exposición y drenaje de aire frío (heladas).
- **Manejo de cuencas:** delimitación de microcuencas, cálculo de área de aporte.
- **Infraestructura rural:** caminos, tranques, embalses.
- **Zonificación y agricultura de precisión:** pendientes, exposición y posición topográfica como capas para zonas de manejo.

> **Imagen sugerida 4:** Mapa de un predio agrícola con curvas de nivel superpuestas a una ortofoto, mostrando el trazado de hileras de cultivo en contorno y un canal de desvío. Ubicación: al final de la sección 3.

---

## 4. Datos de entrada: de dónde viene la elevación

Antes de dibujar una curva hay que **medir o estimar la elevación**. La calidad de las curvas depende totalmente de la calidad de estos datos.

### 4.1 Fuentes principales

| Fuente | Resolución típica | Observaciones |
|---|---|---|
| **Levantamiento topográfico** (estación total, nivel) | Puntos a demanda, precisión de centímetros | Alta precisión, costoso en superficies grandes. |
| **GNSS/RTK** | Puntos a demanda, precisión de pocos centímetros | Muy usado en predios; requiere diseño del muestreo. |
| **Fotogrametría con dron (SfM)** | 2–10 cm de píxel | Genera un modelo que incluye vegetación (MDS); requiere filtrar para obtener terreno desnudo (MDT). |
| **LiDAR aéreo/dron** | 0,5–5 m | Permite separar suelo de vegetación; el estándar para terrenos con cobertura. |
| **DEM globales** (SRTM, NASADEM, ALOS, Copernicus GLO-30) | Cerca de 30 m | Gratuitos y de cobertura global; adecuados para escala regional y de cuenca. |
| **Cartografía existente** (IGM, otras agencias) | Según escala | Curvas ya digitalizadas; pueden usarse como fuente para generar un DEM. |

> **Verifica siempre** la versión, la resolución, el datum vertical y la precisión declarada de la fuente que uses. Los productos globales se actualizan y cambian.

### 4.2 MDT vs. MDS

- **MDT (Modelo Digital del Terreno):** representa el suelo desnudo. Es el que se debe usar para curvas de nivel.
- **MDS (Modelo Digital de Superficie):** incluye árboles, edificios, cultivos. Si generas curvas desde un MDS en un huerto o bosque, estás contorneando la copa de los árboles, no el suelo.
- **DEM:** término genérico; conviene averiguar a cuál de los dos corresponde.

> **Imagen sugerida 5:** Perfil transversal esquemático de un terreno con árboles y una casa, mostrando dos líneas: la del MDS (siguiendo las copas) y la del MDT (siguiendo el suelo). Ubicación: al final de 4.2.

---

## 5. Modelos de datos para representar la superficie

Para generar curvas hay que partir de un modelo de superficie. Existen tres estructuras principales:

### 5.1 Nube de puntos con cota (vectorial puntual)
Conjunto de puntos (x, y, z) irregularmente distribuidos, como los de un levantamiento GNSS o un LiDAR. No se pueden contornear directamente: hay que construir una superficie.

### 5.2 TIN (*Triangulated Irregular Network*)
Red de triángulos formada uniendo los puntos (habitualmente por triangulación de Delaunay). Cada triángulo es un plano inclinado.

- **Ventaja:** respeta exactamente los puntos medidos y puede densificarse en zonas complejas.
- **Limitación:** produce curvas angulosas si hay pocos puntos.

### 5.3 Ráster (grilla regular)
Matriz de celdas con un valor de elevación cada una. Es el formato más común hoy.

- **Ventaja:** simple, eficiente y compatible con casi todo el software.
- **Limitación:** la resolución fija limita el detalle que se puede extraer.

> **Imagen sugerida 6:** Tres paneles lado a lado del mismo terreno: (a) puntos dispersos con su cota, (b) TIN con triángulos, (c) ráster de celdas con escala de grises. Ubicación: al final de la sección 5.

---

## 6. ¿Cómo se generan las curvas de nivel? Visión general

Existen tres familias de métodos, de más antigua a más actual:

1. **Método manual por interpolación lineal** (el original, base conceptual de todo lo demás).
2. **Generación desde un TIN.**
3. **Generación desde un ráster (DEM).** Es el flujo dominante en la práctica actual.

Todos comparten una idea central: **encontrar dónde, entre dos puntos de cota conocida, la superficie "cruza" el valor de la curva buscada.**

### 6.1 El principio: interpolación lineal entre dos puntos

Si el punto A tiene cota 102 m y el punto B tiene cota 118 m, y quiero la curva de 110 m, asumo que la pendiente entre A y B es constante. La curva pasa por un punto P ubicado a una fracción de la distancia AB:

```
fracción = (cota_curva − cota_A) / (cota_B − cota_A)
         = (110 − 102) / (118 − 102) = 8 / 16 = 0,5
```

El punto P está exactamente a la mitad entre A y B. Repitiendo esto para todos los pares de puntos vecinos y uniendo los puntos hallados con igual cota, se obtiene la curva.

> **Imagen sugerida 7:** Esquema con dos puntos A (102 m) y B (118 m) conectados por una línea, con una escala vertical mostrando los niveles 100, 110, 120 y el punto P marcado donde cruza el nivel 110. Ubicación: tras la fórmula anterior.

### 6.2 Método manual (paso a paso, para fines didácticos)

1. Dibujar los puntos con su cota sobre el plano.
2. Unirlos mentalmente o con líneas auxiliares formando triángulos o segmentos que respeten el relieve (siguiendo vaguadas y lomas).
3. Interpolar linealmente sobre cada segmento las cotas que son múltiplos de la equidistancia.
4. Unir los puntos de igual cota con trazo suave.
5. Rotular las curvas maestras y revisar las propiedades de la sección 2.2.

> **Imagen sugerida 8:** Secuencia en 4 pasos de un ejemplo manual con ~12 puntos acotados: (1) puntos, (2) triangulación, (3) puntos interpolados marcados, (4) curvas trazadas. Ubicación: al final de 6.2.

### 6.3 Desde un TIN

El software calcula en cada triángulo (un plano) por dónde pasa cada nivel: el resultado es un segmento recto. La unión de segmentos de triángulos vecinos forma la polilínea de la curva.

### 6.4 Desde un ráster (algoritmo tipo *marching squares*)

Es la técnica que usan GDAL, QGIS, ArcGIS y la mayoría de bibliotecas de Python. Funcionamiento resumido:

1. Para el nivel deseado, cada celda del ráster se clasifica como **por encima** o **por debajo**.
2. Se recorren grupos de cuatro celdas vecinas. Según cuántas estén por encima, el patrón indica si la curva atraviesa ese cuadro y por qué lados.
3. Se interpola linealmente la posición exacta del cruce en cada lado.
4. Los segmentos de cuadros vecinos se encadenan en polilíneas.
5. Se repite para cada nivel (cada múltiplo de la equidistancia).

> **Imagen sugerida 9:** Grilla de 4×4 celdas con valores de elevación escritos, un nivel objetivo destacado, celdas coloreadas según estén sobre/bajo el nivel, y el segmento de curva resultante dibujado con los puntos interpolados en los bordes. Ubicación: al final de 6.4.

---

## 7. Decisiones de diseño antes de generar

### 7.1 Elección de la equidistancia

La equidistancia debe ser coherente con tres cosas:

- **La escala del mapa.** Regla orientativa de uso común: equidistancia (m) ≈ denominador de la escala / 1000. A 1:10.000, unos 10 m; a 1:5.000, unos 5 m.
- **La pendiente del terreno.** En terreno plano conviene equidistancias pequeñas (0,25–1 m); en terreno montañoso, grandes (10–50 m).
- **La resolución y precisión vertical del DEM.** *No tiene sentido* generar curvas de 1 m desde un DEM de 30 m cuya precisión vertical es de varios metros: obtendrás líneas que parecen precisas pero no lo son (**falsa precisión**).

| Uso agronómico | Equidistancia habitual (orientativa) |
|---|---|
| Diseño de riego por surco en terreno plano | 0,25 – 0,5 m |
| Diseño de terrazas o hileras a nivel predial | 0,5 – 2 m |
| Planificación predial (escala 1:5.000) | 2 – 5 m |
| Análisis de cuenca (escala 1:50.000) | 10 – 25 m |

### 7.2 Resolución del DEM

La resolución espacial determina el detalle mínimo que puede aparecer. Una celda de 30 m no puede mostrar un camino de 4 m de ancho ni una zanja.

### 7.3 Sistema de referencia

- Usa un **sistema proyectado** en metros (por ejemplo, UTM) para que la equidistancia y las distancias tengan sentido.
- Si tu DEM está en grados (EPSG:4326), la unidad horizontal son grados y la vertical metros. Esto puede causar errores en cálculos de pendiente. **Reproyecta antes de analizar.**
- Verifica la referencia **vertical** (nivel medio del mar, elipsoide), que puede diferir entre fuentes.

---

## 8. Flujo de trabajo para generar curvas desde un DEM

### Paso 0. Preparar el entorno de trabajo
Carpeta ordenada, proyecto con CRS definido, copias de los datos originales intactas.

### Paso 1. Obtener y revisar el DEM
Recortar al área de estudio con un margen (buffer) para evitar efectos de borde. Revisar visualmente con un sombreado de relieve y detectar huecos, valores anómalos o escalones.

### Paso 2. Reproyectar si es necesario
A un sistema métrico adecuado a la zona.

### Paso 3. (Opcional) Suavizar el DEM
Los DEM tienen ruido que genera curvas dentadas. Un filtro de media o gaussiano de 3×3 puede mejorar el resultado, a costa de perder algo de detalle. **Suaviza el DEM, no la curva final**, siempre que sea posible, para no producir cruces entre curvas.

### Paso 4. Generar las curvas
Tres opciones equivalentes:

**a) QGIS (interfaz gráfica)**
`Ráster > Extracción > Curvas de nivel` (algoritmo basado en GDAL).

- *Capa de entrada:* el DEM.
- *Intervalo entre curvas:* la equidistancia, por ejemplo 5.
- *Nombre del atributo:* `ELEV`.
- Guardar como GeoPackage (`.gpkg`) o Shapefile.

**b) GDAL (línea de comandos)**

```bash
gdal_contour -a ELEV -i 5 dem.tif curvas.gpkg
```

`-i` es el intervalo (equidistancia) y `-a` nombra el campo de elevación.

**c) Python (rasterio + scikit-image + geopandas)**

```python
import numpy as np
import rasterio
from skimage import measure
from shapely.geometry import LineString
import geopandas as gpd

equidistancia = 5

with rasterio.open("dem.tif") as src:
    z = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs
    nodata = src.nodata

if nodata is not None:
    z[z == nodata] = np.nan

zmin, zmax = np.nanmin(z), np.nanmax(z)
niveles = np.arange(np.ceil(zmin / equidistancia) * equidistancia,
                    zmax, equidistancia)

lineas = []
for nivel in niveles:
    for c in measure.find_contours(z, nivel):
        xs, ys = rasterio.transform.xy(transform, c[:, 0], c[:, 1],
                                       offset="center")
        if len(xs) >= 2:
            lineas.append({"ELEV": nivel,
                           "geometry": LineString(zip(xs, ys))})

curvas = gpd.GeoDataFrame(lineas, crs=crs)
curvas.to_file("curvas.gpkg", driver="GPKG")
```

> **Imagen sugerida 10:** Capturas de pantalla anotadas del cuadro de diálogo de QGIS (`Ráster > Extracción > Curvas de nivel`) con los parámetros resaltados con flechas numeradas (1: capa de entrada, 2: intervalo, 3: atributo, 4: salida). Ubicación: dentro del Paso 4a.

### Paso 5. Clasificar maestras e intermedias
Agrega un campo `TIPO` y asígnalo con una regla (por ejemplo, maestra si la cota es múltiplo de 5 × equidistancia). En QGIS se puede hacer con la calculadora de campos:

```
CASE WHEN "ELEV" % 25 = 0 THEN 'maestra' ELSE 'intermedia' END
```

(con equidistancia de 5 m, las maestras caen cada 25 m).

### Paso 6. Simbolizar y etiquetar

- Maestras: trazo más grueso, con etiqueta de cota sobre la línea.
- Intermedias: trazo delgado, sin etiqueta.
- Usar un color pardo/sepia, convención cartográfica clásica para el relieve.
- Colocar las etiquetas siguiendo la línea y con orientación legible.

> **Imagen sugerida 11:** Comparación antes/después de un mismo sector: a la izquierda curvas sin clasificar ni etiquetar (todas iguales), a la derecha con maestras gruesas, etiquetadas y color pardo. Ubicación: al final del Paso 6.

### Paso 7. Validar y limpiar
Ver sección 9.

---

## 9. Control de calidad y errores comunes

### 9.1 Lista de verificación

- ¿Las curvas se cruzan? (No deberían.)
- ¿Hay curvas minúsculas o "islas" sin sentido físico? (Ruido del DEM.)
- ¿Las curvas se ven escalonadas o en "terrazas" artificiales? (Resolución o cuantización del DEM.)
- ¿Las curvas siguen coherentemente los cauces y las divisorias conocidas?
- ¿Las cotas de las curvas coinciden con puntos de control conocidos (GNSS, hitos)?
- ¿Se ven artefactos en los bordes del área? (Falta de buffer.)

### 9.2 Errores frecuentes y cómo corregirlos

| Problema | Causa probable | Solución |
|---|---|---|
| Curvas dentadas o ruidosas | Ruido o resolución del DEM | Suavizar el DEM (filtro 3×3) antes de contornear. |
| Curvas siguiendo árboles o edificios | Se usó un MDS | Usar MDT o filtrar el terreno (clasificación de suelo en LiDAR). |
| Líneas en forma de escalera | DEM con baja resolución vertical (cota entera) | Usar un DEM con valores decimales o aumentar la equidistancia. |
| Equidistancia "fantasma" (muy fina) | Falsa precisión | Subir la equidistancia a un valor coherente con la precisión vertical. |
| Curvas con valores extraños o gigantes | Valores *NoData* (ej. −9999) tratados como cota | Definir correctamente el valor NoData. |
| Curvas distorsionadas | CRS geográfico (grados) | Reproyectar a sistema métrico. |
| Huecos en las curvas | Vacíos en el DEM | Rellenar huecos por interpolación antes de contornear. |

### 9.3 Medir la calidad

Compara la cota del DEM con puntos de control medidos en terreno y calcula el **RMSE vertical**:

```
RMSE = sqrt( Σ (z_DEM − z_control)² / n )
```

Una regla práctica: la equidistancia no debería ser menor que aproximadamente 2–3 veces el RMSE vertical del modelo.

> **Imagen sugerida 12:** Dos mapas del mismo sector con un mismo DEM ruidoso: izquierda con curvas dentadas y pequeños bucles, derecha tras suavizar el DEM. Marcar con círculos rojos las diferencias. Ubicación: al final de 9.2.

---

## 10. Ejemplo aplicado: predio frutal en ladera

**Contexto.** Un predio de 40 ha con huerto de paltos en ladera, con pendientes entre 8 % y 25 %. Se necesita decidir el trazado de hileras y una red de canales de desvío de aguas lluvia.

**Datos.** Vuelo con dron con fotogrametría (MDS de 10 cm) y 15 puntos de control GNSS.

**Procedimiento resumido.**

1. Filtrar el MDS para obtener un MDT (clasificación de puntos de suelo).
2. Remuestrear el MDT a 1 m para manejar tamaño de archivo.
3. Verificar RMSE con los 15 puntos GNSS (supongamos 0,25 m).
4. Elegir equidistancia de 1 m (≥ 3 veces el RMSE).
5. Suavizar con filtro 3×3 y generar curvas con `gdal_contour -i 1`.
6. Marcar maestras cada 5 m y etiquetar.
7. Trazar hileras en contorno y ubicar canales de desvío en las zonas de mayor concentración de escurrimiento.

**Lectura del resultado.** Donde las curvas se aprietan (pendiente mayor al 20 %), se evalúan terrazas o cultivo en curvas con mayor densidad de obras de conservación; donde se abren, se prioriza el drenaje para evitar anegamiento.

> **Imagen sugerida 13:** Mapa final del predio: ortofoto de fondo, curvas con maestras etiquetadas, hileras propuestas en contorno (líneas finas verdes) y canales de desvío (azul). Ubicación: al final de la sección 10, como figura de síntesis.

---

## 11. Más allá de las curvas: productos derivados

Las curvas de nivel son solo una forma de explotar un DEM. Con el mismo modelo se pueden obtener:

- **Mapa de pendientes** (en % o grados).
- **Mapa de exposición** (orientación de la ladera).
- **Sombreado de relieve** (*hillshade*) para visualización.
- **Redes de drenaje y cuencas** (dirección y acumulación de flujo).
- **Índices topográficos** (por ejemplo, índice de humedad topográfica).

Estos productos suelen ser más útiles para el análisis cuantitativo; las curvas son excelentes para **comunicar y planificar** a escala predial.

---

## 12. Resumen del capítulo

- Una curva de nivel une puntos de igual elevación; la **equidistancia** es la diferencia constante entre curvas.
- Sus propiedades (no se cruzan, son cerradas, su separación indica pendiente) sirven para interpretar y validar.
- Los datos de elevación pueden provenir de topografía, GNSS, LiDAR, fotogrametría o DEM globales; hay que usar un **MDT** y conocer su precisión.
- La generación se basa en **interpolación lineal**; en la práctica se usa el algoritmo *marching squares* sobre un ráster o contorneo desde un TIN.
- La equidistancia debe ser coherente con la escala, la pendiente y, sobre todo, con la **precisión vertical** del DEM.
- Siempre se debe validar: cruces, ruido, coherencia con el drenaje y comparación con puntos de control.

---

## 13. Actividades

### 13.1 Preguntas de repaso

1. Explica con tus palabras por qué las curvas de nivel nunca se cruzan.
2. ¿Qué indica una "V" de curvas en un valle y hacia dónde apunta?
3. ¿Por qué es un error generar curvas de 0,5 m desde un DEM global de 30 m?
4. Diferencia un MDT de un MDS y explica cuál usarías para trazar hileras en un huerto.
5. Describe, en 4 pasos, cómo funciona la generación de curvas desde un ráster.

### 13.2 Ejercicio de cálculo
Los puntos A (cota 214 m) y B (cota 226 m) están separados 60 m. Con equidistancia de 5 m, ¿a qué distancia de A pasan las curvas de 215, 220 y 225 m? *(Pista: usa la fracción de la sección 6.1.)*

### 13.3 Práctico en laboratorio

El [notebook de laboratorio](laboratorio.ipynb) resuelve estos pasos con un DEM de ejemplo; repítelos luego con tu propia zona.

1. Descarga un DEM de un predio o cuenca de tu interés y recórtalo.
2. Reproyéctalo a UTM.
3. Genera curvas con tres equidistancias distintas (por ejemplo 5, 10 y 25 m).
4. Compara visualmente y discute cuál es la adecuada para un mapa a escala 1:10.000.
5. Genera una versión suavizada del DEM y compara el efecto en las curvas.
6. Entrega un mapa con curvas maestras etiquetadas, leyenda, escala y norte.

---

## Glosario

- **Cota:** valor de altura de un punto.
- **DEM / MDE:** modelo digital de elevación; término genérico.
- **Equidistancia:** diferencia de altura entre curvas consecutivas.
- **Isohipsa:** sinónimo de curva de nivel.
- **MDS / MDT:** modelo digital de superficie / del terreno.
- **RMSE:** raíz del error cuadrático medio, medida de exactitud.
- **TIN:** red irregular de triángulos.
- **Vaguada:** línea de menor cota de un valle, por donde escurre el agua.

---

## Lecturas y recursos sugeridos

*(Verificar edición y disponibilidad vigente antes de entregarlas al curso.)*

- Documentación oficial de GDAL: utilidad `gdal_contour`.
- Documentación oficial de QGIS: algoritmo de curvas de nivel (Contour).
- Burrough, P. A. y McDonnell, R. A. *Principles of Geographical Information Systems*. Oxford University Press.
- Wilson, J. P. y Gallant, J. C. (eds.). *Terrain Analysis: Principles and Applications*. Wiley.
- Documentación del conjunto de datos de elevación que se use (SRTM, Copernicus DEM, etc.), en particular sus precisión y datum vertical.
