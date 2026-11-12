Apunte teórico
# **Procesamiento de Modelos Digitales de Elevación (DEM) y generación de curvas de nivel con Python.**

Complemento teórico del notebook práctico: \
**Procesamiento de Modelos Digitales de Elevación (DEM) y Generación de Curvas de Nivel**\
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zelaznog-J/curvas-nivel/blob/main/dem_curvas_nivel.ipynb)


## **1. Introducción**

**Los Modelos Digitales de Elevación (DEM, Digital Elevation Models)** permiten representar las alturas del terreno mediante estructuras de datos ráster, posibilitando su procesamiento computacional y su integración con otras fuentes de información espacial.

Este notebook teórico aborda los fundamentos conceptuales y metodológicos del procesamiento de datos DEM y la generación de curvas de nivel, en concordancia con el flujo práctico desarrollado con Python y bibliotecas especializadas en análisis geoespacial [[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zelaznog-J/curvas-nivel/blob/main/dem_curvas_nivel.ipynb)]. Dicho flujo abarca la descarga, exploración, reproyección, visualización, recorte espacial, remuestreo, suavizado y extracción de isolíneas. Contempla la visualización de tres escalas: A nivel regional (en este ejemplo, la región de Ñuble), comunal (Chillán Viejo) y a nivel predial (un área delimitada para fines didácticos). El objetivo principal es evaluar y reflexionar sobre los alcances y limitaciones del procesamiento.

## **2. Fundamentos de los Modelos Digitales de Elevación**

### 2.1. Definición de un DEM

Un Modelo Digital de Elevación es una representación numérica de la distribución espacial de las alturas de una superficie terrestre. En su formato ráster, el modelo se organiza como una matriz de celdas, donde cada celda contiene un valor que representa la elevación correspondiente a una posición geográfica.

Matemáticamente, un DEM puede expresarse como una función espacial:

$$
z=f(x,y)
$$

Donde:

- $x$: coordenada horizontal en la dirección Este-Oeste.
- $y$: coordenada horizontal en la dirección Norte-Sur.
- $z$: valor de elevación asociado a la posición espacial.

Esta representación permite analizar el relieve mediante operaciones matemáticas, estadística espacial y procesamiento digital de imágenes.

### 2.2. Estructura ráster

Los datos ráster se caracterizan por una organización matricial regular. Cada celda posee una posición dentro de la matriz y una correspondencia con una ubicación geográfica determinada.

Los principales componentes de un DEM ráster son:

| Componente | Descripción |
|---|---|
| Filas y columnas | Definen las dimensiones de la matriz. |
| Resolución espacial | Tamaño del área terrestre representada por cada píxel. |
| Sistema de referencia | Define cómo se relacionan las coordenadas del ráster con la superficie terrestre. |
| Transformación afín | Establece la correspondencia entre índices de la matriz y coordenadas espaciales. |
| Valores de elevación | Representan las alturas de cada celda. |
| NoData | Identifica celdas sin información válida. |
| Extensión espacial | Define los límites geográficos del modelo. |

La correcta interpretación de estos componentes es indispensable para realizar operaciones espaciales consistentes.

### 2.3. Resolución espacial y precisión altimétrica

La resolución espacial corresponde al tamaño de la celda del modelo, mientras que la precisión altimétrica expresa el grado de incertidumbre asociado a los valores de elevación. Ambos conceptos son diferentes y no deben confundirse.

En el notebook práctico se utiliza un DEM ALOS PALSAR con una resolución de trabajo de aproximadamente 12,5 metros.

El área representada por una celda de 12,5 × 12,5 metros es:

$$
A=156,25 m^2
$$

Esto significa que cada píxel representa una superficie terrestre de aproximadamente 156,25 m². En consecuencia, las variaciones topográficas de dimensiones inferiores a esta escala pueden no estar adecuadamente representadas.

**La resolución espacial no garantiza precisión vertical ni capacidad para identificar microrelieves.**

### 2.4. Modelos digitales de elevación y superficie

Desde una perspectiva conceptual, es importante distinguir entre:

- **Modelo Digital del Terreno (DTM):** representa la elevación del terreno desnudo, excluyendo idealmente objetos como vegetación y edificaciones.
- **Modelo Digital de Superficie (DSM):** representa la elevación de la superficie incluyendo objetos presentes sobre el terreno.

## **3. Datos altimétricos**

El flujo metodológico del notebook integra datos de elevación del terreno procedentes del sensor **PALSAR** (*Phased Array type L-band Synthetic Aperture Radar*), embarcado en la plataforma satelital **ALOS** (*Advanced Land Observing Satellite / Daichi*) de la Agencia Japonesa de Exploración Aeroespacial (JAXA). Los insumos originales fueron distribuidos por el Alaska Satellite Facility (ASF) DAAC y posteriormente procesados para cada Región de Chile por el [Geoportal de Chile](https://geoportal.cl/catalog)

> La tecnología RADAR de apertura sintética en Banda L (*frecuencia nominal de $1,27\text { GHz}$  y longitud de onda de $≈ 23,6\text { cm}$*) provee capacidad de penetración en la cobertura nubosa y el dosel vegetal, permitiendo registrar la superficie del terreno firme mediante escenas orbitales ascendentes y descendentes con una superficie de cobertura nominal de $85 × 85\text{ km}$.


###3.1. Corrección geoidal, conversión altimetrica y adecuacion a espacial.
Las alturas elipsoidales brutas capturadas por el satélite se convirtieron a altitudes ortométricas sobre el Nivel Medio del Mar (H = h - N) mediante la sustracción del *modelo geoidal EGM2008*. El mosaico continuo fue delimitado según el marco territorial oficial de la ODEPA y exportado como ráster JPEG 2000 en codificación de 16 bits. En resumen, el modelo presenta las siguientes características:

| Parámetro | Valor |
|---|---|
| Fuente | ALOS PALSAR |
| Región | Ñuble, Chile |
| Formato ráster | JPEG 2000 |
| Sistema de referencia original | EPSG:5360 |
| Resolución de trabajo | 12,5 m |

\
**La utilización de una fuente regional permite desarrollar análisis a diferentes escalas espaciales, siempre que se considere la adecuación del modelo a los objetivos del estudio.**

## **4. Sistemas de referencia de coordenadas y reproyección**

### 4.1. Concepto de sistema de referencia de coordenadas

Un Sistema de Referencia de Coordenadas (CRS, Coordinate Reference System) define cómo se representan las posiciones geográficas sobre la superficie terrestre.

Los CRS permiten establecer una relación entre las coordenadas de los datos y una referencia geodésica determinada. Su correcta utilización es indispensable para garantizar la compatibilidad espacial entre capas vectoriales y ráster.

En términos generales, se distinguen:

- **Sistemas geográficos:** expresan las posiciones mediante latitud y longitud, generalmente en grados.
- **Sistemas proyectados:** representan las posiciones sobre un plano mediante coordenadas cartesianas, generalmente en metros.

### 4.2. Proyección UTM

La proyección Universal Transversal de Mercator (UTM) permite representar sectores del territorio mediante coordenadas métricas, facilitando cálculos de distancia, superficie y análisis espacial.

En el notebook se utiliza el sistema:

$$
{EPSG:32718}
$$

Este código corresponde a WGS 84 / UTM zona 18 Sur.

La transformación a coordenadas UTM resulta particularmente importante para:

- Medir distancias y superficies.
- Definir buffers en metros.
- Establecer resoluciones espaciales métricas.
- Ejecutar recortes y análisis geométricos.
- Facilitar la interpretación cartográfica del territorio.

### 4.3. Reproyección de datos ráster

La reproyección consiste en transformar la ubicación espacial de las celdas desde un CRS de origen hacia un CRS de destino.

A diferencia de una capa vectorial, donde las coordenadas de los vértices pueden transformarse directamente, en los ráster la reproyección requiere construir una nueva cuadrícula y estimar los valores que corresponden a sus celdas.

Este procedimiento implica:

1. Definir el CRS de destino.
2. Determinar la extensión espacial del nuevo ráster.
3. Establecer el tamaño de celda de salida.
4. Calcular los valores mediante interpolación.
5. Asignar correctamente los valores NoData.
6. Generar el nuevo archivo ráster.

En Python, estas operaciones pueden desarrollarse mediante `rioxarray` y `rasterio`.

```python
import rioxarray as rxr
from rasterio.enums import Resampling

dem = rxr.open_rasterio(
    "dem_original.jp2",
    masked=True
).squeeze(drop=True)

dem_utm = dem.rio.reproject(
    "EPSG:32718",
    resolution=12.5,
    resampling=Resampling.bilinear
)
```

Este ejemplo representa una reproyección a UTM zona 18 Sur, con resolución de salida de 12,5 metros y remuestreo bilineal.

## **5. Remuestreo e interpolación espacial**

### 5.1. Fundamentos del remuestreo

El remuestreo es el procedimiento mediante el cual se estiman los valores de un ráster sobre una nueva cuadrícula espacial.

Este proceso se requiere cuando se modifica:

- La resolución espacial.
- La ubicación de las celdas.
- La extensión del ráster.
- El sistema de referencia de coordenadas.

El remuestreo no debe interpretarse como una mejora automática de la calidad del dato original. **Se trata de una transformación matemática que permite adaptar la estructura espacial del modelo.**

### 5.2. Interpolación bilineal

La interpolación bilineal utiliza los valores de los cuatro píxeles vecinos más próximos para estimar el valor de una nueva celda.

Su formulación se basa en una interpolación sucesiva en las dos direcciones espaciales. Este método genera superficies relativamente continuas y es apropiado para numerosas operaciones de reproyección de datos de elevación.

En el notebook se utiliza:

```python
resampling=Resampling.bilinear
```

### 5.3. Comparación conceptual de métodos

| Método | Característica | Consideración |
|---|---|---|
| Nearest | Selecciona el valor del píxel más cercano. | Conserva valores originales, pero puede producir discontinuidades. |
| Bilinear | Utiliza cuatro píxeles vecinos. | Genera superficies más suaves. |
| Cubic | Utiliza un conjunto mayor de píxeles vecinos. | Produce una interpolación más compleja. |
| Average | Calcula un promedio espacial de los valores contribuyentes. | Puede utilizarse para reducir resolución. |

\
La selección del método debe responder al objetivo del procesamiento y a las características de la información original.

## **6. Recorte espacial de Modelos Digitales de Elevación**

### 6.1. Concepto de Clip

El recorte espacial o *clipping* consiste en delimitar un ráster mediante una geometría vectorial que representa el área de interés.

Esta operación permite reducir la extensión de los datos y concentrar el procesamiento en un territorio específico.

En el notebook se aplican dos niveles de recorte:

- Recorte inicial mediante una caja envolvente.
- Recorte definitivo mediante el límite geométrico de la comuna o del predio.

### 6.2. Caja envolvente (Bbox)

La caja envolvente o *bounding box* corresponde al rectángulo mínimo que contiene una geometría.

Se define mediante cuatro coordenadas:

$$
Bbox = (x_{min},y_{min},x_{max},y_{max})
$$

Su principal utilidad es realizar una selección espacial preliminar eficiente.

### 6.3. Buffer espacial

Un buffer corresponde a una zona de influencia construida alrededor de una geometría a una distancia determinada.

En el procesamiento predial del notebook se establece un buffer de **150 m**. Este margen permite disponer de información adicional alrededor del predio antes de realizar las operaciones de suavizado.

La inclusión de un margen espacial contribuye a reducir los efectos de borde que pueden producirse cuando un filtro opera cerca de los límites de un ráster.

### 6.4. Flujo de recorte espacial

El procedimiento general puede sintetizarse en:

1. Cargar el límite de la comuna o predio.
2. Identificar su CRS.
3. Reproyectar la geometría al CRS de trabajo.
4. Construir un buffer, cuando corresponda.
5. Recortar preliminarmente el ráster mediante su extensión.
6. Reproyectar y remuestrear el DEM.
7. Aplicar el recorte geométrico definitivo.
8. Exportar el resultado.

Este procedimiento permite obtener un modelo de elevación espacialmente delimitado y adecuado para las etapas posteriores de análisis.

## **7. Suavizado espacial de modelos de elevación**

### 7.1. Fundamentos del suavizado

El suavizado espacial es una operación de procesamiento digital que modifica la distribución local de los valores de un ráster mediante un filtro.

En el contexto de los DEM, el suavizado permite reducir variaciones espaciales abruptas y generar una superficie más continua.

Sin embargo, debe considerarse que esta operación modifica los valores originales del modelo y puede atenuar características topográficas reales.

Por tanto, el suavizado constituye una transformación matemática de la superficie y no una corrección de errores altimétricos.

### 7.2. Filtro Gaussiano

El filtro Gaussiano es una técnica de convolución que utiliza una función de distribución normal como ponderador espacial.

La función Gaussiana bidimensional puede expresarse como:

$$
G(x,y)=\frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}
$$

Donde:

- $x,y$: desplazamientos espaciales respecto del centro del filtro.
- $\\sigma$: desviación estándar de la distribución.
- $G(x,y)$: ponderación asignada a cada posición.

Los valores cercanos al centro del filtro reciben mayor ponderación que aquellos ubicados a mayor distancia.

### 7.3. Interpretación del parámetro sigma

El parámetro $\\sigma$ controla el grado de suavizado. Un valor elevado implica una mayor influencia espacial de los vecinos y, por tanto, una superficie más suavizada.

En el notebook se define:

$$\sigma = 20 \text{ m}$$

Dado que la resolución de trabajo es de 12,5 metros, el parámetro debe convertirse a unidades de píxel:

$$\sigma_{px} = \frac{\sigma_m}{RES_m}$$

$$\sigma_{px} = \frac{20}{12,5} = 1,6$$  

Esto significa que el filtro se aplica con una desviación estándar de 1,6 píxeles.

### 7.4. Tratamiento de valores NoData

Una dificultad importante en el procesamiento de DEM es la presencia de celdas sin información válida.

Los valores NoData no deben incorporarse directamente a los cálculos de suavizado, debido a que pueden generar artefactos y distorsiones en los valores vecinos.

El notebook implementa un filtro Gaussiano normalizado que considera únicamente las celdas válidas. Su funcionamiento se basa en:

1. Identificar las celdas válidas.
2. Reemplazar temporalmente los valores inválidos por cero.
3. Aplicar el filtro Gaussiano al numerador.
4. Filtrar una máscara de validez para obtener el denominador.
5. Dividir ambos resultados.
6. Mantener como NoData las posiciones sin información válida.

$$Z_s = \frac{G * (Z \cdot M)}{G * M}$$
Donde:

- $Z$: superficie original.
- $M$: máscara binaria de validez.
- $G$: filtro Gaussiano.
- $*$: operación de convolución.
- $Z_s$: superficie suavizada.

### 7.5. Implementación en Python

```python
import numpy as np
import scipy.ndimage as ndi

def suavizar_gauss_nan(a, sigma_px):
    # Filtro Gaussiano normalizado que considera celdas válidas
    valido = np.isfinite(a)

    num = ndi.gaussian_filter(
        np.where(valido, a, 0.0),
        sigma_px
    )

    den = ndi.gaussian_filter(
        valido.astype(float),
        sigma_px
    )

    return np.where(
        valido & (den > 1e-6),
        num / np.maximum(den, 1e-6),
        np.nan
    )
```

La función permite suavizar matrices de elevación sin incorporar directamente las celdas inválidas al cálculo.

## **8. Curvas de nivel: fundamentos teóricos y representación cartográfica**

### 8.1. Definición de curvas de nivel

Una curva de nivel es una línea que conecta puntos de igual elevación respecto de una superficie de referencia.

Matemáticamente, una curva de nivel corresponde al conjunto de puntos que satisface:

$$
f(x,y)=c
$$

Donde:

- $f(x,y)$: función de elevación del terreno.
- $c$: valor constante de elevación.
- $(x,y)$: coordenadas espaciales de los puntos pertenecientes a la curva.

En términos cartográficos, las curvas de nivel permiten representar una superficie tridimensional mediante elementos lineales bidimensionales.

### 8.2. Equidistancia de curvas de nivel

La equidistancia corresponde a la diferencia vertical constante entre curvas consecutivas.

Por ejemplo, para una equidistancia de 20 metros:

$$C_n = n \cdot 20$$

Donde $n$ representa un número entero asociado a los niveles de elevación.

En el notebook se utilizan dos configuraciones principales:

| Escala | Intervalo de curvas | Curvas maestras |
|---|---:|---:|
| Comunal | 20 m | Cada 100 m |
| Predial | 1 m | Cada 2 m |

Las curvas maestras permiten destacar determinadas elevaciones y facilitar la lectura cartográfica.

### 8.3. Interpretación topográfica

La distribución espacial de las curvas de nivel permite interpretar diferentes características del terreno.

**Pendiente del terreno:**

- Curvas muy próximas: indican cambios de elevación importantes en distancias horizontales pequeñas.
- Curvas separadas: indican cambios de elevación más graduales.
- Curvas equidistantes: sugieren una pendiente relativamente uniforme.

**Configuración del relieve:**

- Curvas cerradas con elevaciones crecientes hacia el centro: pueden representar una elevación.
- Curvas cerradas con elevaciones decrecientes hacia el centro: pueden representar una depresión.
- Curvas en forma de V o U: pueden reflejar estructuras de valle o cresta, dependiendo de la configuración altimétrica.

La interpretación debe considerar el contexto geomorfológico y la información altimétrica disponible.

### 8.4. Generación de curvas de nivel mediante GDAL

GDAL es una biblioteca de software especializada en la lectura, transformación y procesamiento de datos geoespaciales.

La herramienta `gdal_contour` permite generar curvas de nivel a partir de un modelo ráster de elevación.

El procedimiento consiste en identificar los niveles altimétricos establecidos y determinar las líneas que conectan las posiciones donde el modelo alcanza cada valor.

En el notebook se utiliza la herramienta mediante Python:

```python
import subprocess

subprocess.run([
    "gdal_contour",
    "-f", "GPKG",
    "-a", "ELEV",
    "-i", "1",
    "dem_predio_suave.tif",
    "curvas_predio.gpkg"
], check=True)
```

En este ejemplo:

- `gdal_contour`: ejecuta la extracción de curvas.
- `-f GPKG`: establece el formato GeoPackage.
- `-a ELEV`: almacena la elevación en el atributo `ELEV`.
- `-i 1`: define una equidistancia de un metro.
- El archivo `.tif`: corresponde al DEM de entrada.
- El archivo `.gpkg`: contiene las curvas de nivel generadas.

**La utilización de GDAL permite automatizar la extracción y generar datos vectoriales compatibles con sistemas de información geográfica.**

### 8.5. Formato GeoPackage

GeoPackage (`.gpkg`) es un formato geoespacial basado en SQLite que permite almacenar información vectorial y ráster.

En el flujo de trabajo se utiliza para almacenar las curvas de nivel como entidades lineales, incluyendo su atributo de elevación.

Entre sus ventajas se encuentran:

- Almacenamiento en un único archivo.
- Compatibilidad con sistemas de información geográfica.
- Conservación de atributos y geometrías.
- Facilidad de intercambio y distribución de información espacial.

## **9. Procesamiento de DEM a escala comunal**

### 9.1. Objetivo del análisis comunal

El análisis comunal busca representar las características generales del relieve dentro de una unidad administrativa.

En el notebook se desarrolla un procesamiento para la comuna de Chillán Viejo, utilizando un DEM regional previamente descargado.

El procedimiento considera:

1. Carga del límite comunal en formato GeoJSON.
2. Determinación del CRS UTM de trabajo.
3. Reproyección y remuestreo del DEM.
4. Recorte espacial según la geometría comunal.
5. Exportación del DEM procesado.
6. Generación de curvas de nivel cada 20 metros.
7. Visualización del relieve y de las curvas de nivel.

### 9.2. GeoJSON y datos vectoriales

GeoJSON es un formato de intercambio de información geográfica basado en JSON. Permite representar puntos, líneas, polígonos y multipolígonos.

En este caso, el límite comunal se representa mediante geometrías poligonales que permiten delimitar espacialmente el procesamiento del DEM.

La biblioteca GeoPandas facilita la lectura, transformación y manipulación de estas geometrías.

```python
import geopandas as gpd

comuna = gpd.read_file(
    "limite_comunal.geojson"
)

crs_utm = comuna.estimate_utm_crs()

comuna_utm = comuna.to_crs(
    crs_utm
)
```

El resultado corresponde a una capa vectorial reproyectada al sistema UTM estimado para el área de estudio.

### 9.3. Visualización del DEM comunal

La representación del DEM mediante Matplotlib permite visualizar la distribución espacial de las elevaciones. El uso de mapas de color facilita identificar sectores de menor y mayor altitud.

La superposición de curvas de nivel permite integrar la representación continua del DEM con una interpretación cartográfica basada en líneas de igual elevación.

Esta visualización es útil para:

- Reconocer patrones generales del relieve.
- Identificar gradientes altimétricos.
- Comparar sectores de distinta elevación.
- Interpretar la distribución espacial de las curvas.
- Contextualizar la ubicación de localidades y elementos territoriales.

## **10. Procesamiento de DEM a escala predial**

### 10.1. Particularidades del análisis predial

El análisis predial requiere una delimitación espacial más precisa del área de interés y una representación cartográfica que permita interpretar las variaciones del relieve dentro de una propiedad.

En el notebook se utiliza un predio ubicado en el sector Los Colihues.



> **Nota aclaratoria:** *La delimitación y selección del predio ubicado en el sector Los Colihues responde exclusivamente a fines didácticos y de ejercitación práctica. La ubicación y los límites trazados fueron determinados al azar. Dicha delimitación no posee validez legal, jurídica, deslindadora ni catastral, y no constituye una referencia oficial sobre el derecho de propiedad o deslindes reales del terreno.*

El procesamiento considera:

- Lectura del límite predial desde un archivo KML.
- Reproyección a coordenadas UTM.
- Aplicación de un buffer de 150 metros.
- Recorte del DEM regional.
- Reproyección y remuestreo a 12,5 metros.
- Suavizado Gaussiano con sigma de 20 metros.
- Generación de curvas de nivel cada 1 metro.
- Identificación de curvas maestras cada 2 metros.
- Recorte definitivo al límite del predio.
- Exportación y visualización cartográfica.

### 10.2. KML y representación de límites prediales

KML (Keyhole Markup Language) es un formato utilizado para representar y compartir información geográfica.

En el contexto del notebook, el límite predial se utiliza como geometría de referencia para delimitar el procesamiento y recortar las curvas de nivel.

La biblioteca GeoPandas (pyogrio) permite incorporar estas geometrías al flujo de procesamiento espacial.

### 10.3. Clasificación de curvas maestras

La clasificación de curvas maestras permite diferenciar visualmente determinados niveles altimétricos.

En el notebook, una curva se identifica como maestra cuando su elevación es múltiplo del intervalo establecido:

```python
curvas["maestra"] = (
    curvas["ELEV"] % 2
) == 0
```

Este procedimiento genera una variable booleana que permite distinguir curvas maestras de curvas secundarias.

La clasificación facilita:

- Diferenciar niveles altimétricos.
- Mejorar la jerarquía visual.
- Reducir la densidad de etiquetas.
- Favorecer la lectura cartográfica.

### 10.4. Visualización cartográfica predial

La representación final del predio integra tres componentes:

1. Curvas de nivel coloreadas según su elevación.
2. Límite geométrico del predio.
3. Imagen satelital de referencia.

La utilización de un mapa base satelital permite contextualizar espacialmente las curvas de nivel y relacionarlas con elementos visibles del territorio.

La visualización incorpora etiquetas de elevación y una diferenciación gráfica entre curvas maestras y secundarias.

## **11. Limitaciones técnicas y precisión altimétrica**

> **Concepto fundamental: falsa precisión**
>
> La generación de curvas de nivel con intervalos pequeños no implica que el modelo tenga una precisión vertical equivalente.

### 11.1. Falsa precisión en curvas de nivel prediales

Uno de los aspectos más importantes del notebook corresponde a las limitaciones del DEM ALOS PALSAR cuando se utiliza a escala predial.

El documento señala que el modelo presenta:

- Resolución espacial de aproximadamente 12,5 metros.
- Error vertical del orden de ±2 a ±5 metros.

Estas características condicionan la interpretación de curvas de nivel con intervalos reducidos.

**La generación de curvas cada 1 metro no implica que el modelo tenga una precisión vertical de un metro. Por el contrario, cuando la equidistancia de las curvas es inferior a la precisión altimétrica del modelo, se produce una representación con falsa precisión.**

### 11.2. ¿Qué significa falsa precisión?

La falsa precisión corresponde a la presentación de resultados con un nivel de detalle numérico o cartográfico superior al que permite justificar la calidad de los datos originales.

En este contexto, el software puede generar curvas de nivel cada metro, pero dichas curvas no representan necesariamente diferencias reales de elevación de un metro en el terreno.

La interpolación y el suavizado producen una superficie matemáticamente continua, pero no incorporan información topográfica adicional.

### 11.3. Consecuencias para el análisis predial

El uso de curvas de nivel derivadas de DEM de resolución moderada puede presentar limitaciones en:

- Identificación de pequeñas depresiones.
- Reconocimiento de zanjas y taludes.
- Representación de microrelieves.
- Estimación de pendientes locales.
- Diseño de obras de drenaje.
- Cálculo de movimientos de tierra.
- Determinación de cotas de construcción.

En consecuencia, las curvas de nivel obtenidas a partir de ALOS PALSAR deben utilizarse principalmente como herramientas de interpretación general del relieve predial, no como sustitutos de un levantamiento topográfico de alta precisión.

### 11.4. Fuentes de información de mayor precisión

Para aplicaciones que requieren precisión centimétrica o una representación detallada del microrelieve, el documento recomienda sustituir el DEM por fuentes de información de mayor resolución y precisión, tales como:

| Tecnología | Aplicación |
|---|---|
| Fotogrametría UAV | Generación de modelos de elevación mediante imágenes capturadas por drones. |
| LiDAR | Obtención de información tridimensional de alta densidad mediante mediciones láser. |
| GNSS-RTK | Determinación precisa de coordenadas mediante posicionamiento satelital diferencial en tiempo real. |

La selección de la tecnología depende de los requerimientos técnicos del proyecto, la extensión del área de estudio y el nivel de precisión necesario.

## **12. Ecosistema Python para ciencia de datos geoespaciales**

El procesamiento de DEM requiere integrar diferentes bibliotecas especializadas, debido a que cada una resuelve operaciones específicas dentro del flujo de trabajo.

### 12.1. Bibliotecas principales

| Biblioteca | Funcionalidad | Aplicación en el notebook |
|---|---|---|
| NumPy | Cálculo numérico y matrices. | Manipulación de elevaciones y operaciones matemáticas. |
| Rasterio | Lectura y escritura de ráster. | Exploración y gestión de DEM. |
| Rioxarray | Análisis ráster con coordenadas espaciales. | Reproyección y recorte espacial. |
| GeoPandas | Manipulación de datos vectoriales. | Lectura de GeoJSON, KML y GeoPackage. |
| GDAL | Procesamiento geoespacial. | Generación de curvas de nivel. |
| SciPy | Métodos científicos y filtros. | Suavizado Gaussiano. |
| Matplotlib | Visualización científica. | Representación del DEM y curvas de nivel. |
| Contextily | Integración de mapas base. | Visualización satelital del predio. |
| Requests | Comunicación HTTP. | Descarga de datos geoespaciales. |
| TQDM | Visualización de progreso. | Seguimiento de descargas y procesos. |

### 12.2. NumPy y matrices de elevación

NumPy constituye una herramienta esencial para la manipulación de estructuras matriciales.

Un DEM puede almacenarse como una matriz bidimensional:

```python
import numpy as np

elevaciones = np.array([
    [100, 105, 110],
    [102, 108, 115],
    [104, 112, 120]
])
```

Cada elemento representa un valor de elevación asociado a una posición dentro de la cuadrícula.

NumPy permite ejecutar operaciones sobre toda la matriz, como:

```python
zmin = np.nanmin(elevaciones)
zmax = np.nanmax(elevaciones)
zmean = np.nanmean(elevaciones)
```

Estas operaciones permiten obtener estadísticas básicas del relieve.

### 12.3. Rasterio y lectura de datos ráster

Rasterio permite acceder a los datos y metadatos de los archivos ráster.

```python
import rasterio

with rasterio.open("dem.tif") as src:
    dem = src.read(1)

    print(src.crs)
    print(src.res)
    print(src.bounds)
    print(src.width)
    print(src.height)
```

Los metadatos permiten verificar:

- Sistema de referencia.
- Resolución espacial.
- Extensión geográfica.
- Dimensiones de la matriz.
- Tipo de dato.
- Valor NoData.

La inspección de estos parámetros debe preceder cualquier operación de procesamiento.

### 12.4. Google Colab como entorno de ejecución

El notebook utiliza Google Colab como entorno de programación.

Este entorno permite:

- Ejecutar código Python en la nube.
- Instalar bibliotecas geoespaciales.
- Ejecutar celdas de forma secuencial.
- Integrar almacenamiento mediante Google Drive.
- Generar visualizaciones.
- Exportar resultados.

La conexión con Google Drive permite mantener archivos de entrada y salida disponibles entre sesiones. La organización de carpetas es relevante para garantizar la reproducibilidad del procesamiento.

## **13. Flujo metodológico integrado del procesamiento**

El procesamiento desarrollado en el notebook puede sintetizarse mediante la siguiente secuencia:

1. **Adquisición de datos**
   Descarga DEM ALOS PALSAR y límites vectoriales\
   ↓

2. **Exploración y validación**
   Metadatos, CRS, resolución, extensión y NoData\
   ↓

3. **Preparación espacial**
   Reproyección, remuestreo y recorte inicial\
   ↓

4. **Procesamiento del DEM**
   Suavizado espacial y tratamiento de celdas inválidas\
   ↓

5. **Extracción de curvas de nivel**
   GDAL, intervalo altimétrico y atributos de elevación\
   ↓

6. **Recorte y representación cartográfica**
   Límites comunales o prediales, curvas maestras y mapas\
   ↓

7. **Exportación y evaluación**
   GeoTIFF, GeoPackage y evaluación de precisión

\
Este flujo constituye una estructura metodológica reproducible que puede adaptarse a diferentes áreas geográficas y escalas de análisis.

## **14. Consideraciones de calidad y reproducibilidad**

En ciencia de datos geoespaciales, la calidad de un producto no depende exclusivamente de su apariencia cartográfica, sino también de la consistencia de los datos, la trazabilidad de los procedimientos y la reproducibilidad de los resultados.

Para asegurar un procesamiento técnicamente adecuado, es recomendable verificar:

- La correspondencia entre los CRS del DEM y de las geometrías vectoriales.
- La correcta identificación de las celdas NoData.
- La resolución espacial del ráster de salida.
- La conservación de los valores de elevación.
- La coherencia entre el intervalo de curvas y la precisión del modelo.
- La integridad de los archivos vectoriales exportados.
- La correcta delimitación espacial de los resultados.
- La documentación de los parámetros utilizados.

En el notebook, la centralización de parámetros mediante variables globales facilita la modificación del flujo de procesamiento sin alterar directamente las funciones principales.

Por ejemplo:

```python
RES_M = 12.5

INTERVALO_COMUNA_M = 20

BUFFER_PREDIO_M = 150

SIGMA_SUAVIZADO_M = 20

INTERVALO_PREDIO_M = 1

INTERVALO_MAESTRAS_PREDIO_M = 2
```

Esta estrategia favorece la legibilidad, la mantención y la reproducibilidad del código.

## **15. Aplicaciones en ingeniería agronómica y gestión territorial**

Los Modelos Digitales de Elevación y las curvas de nivel presentan aplicaciones relevantes en diferentes disciplinas vinculadas al territorio.

### 15.1. Agricultura de precisión

La información altimétrica puede contribuir a comprender la distribución espacial del relieve en terrenos agrícolas.

Entre sus aplicaciones potenciales se encuentran:

- Caracterización topográfica de predios.
- Identificación de sectores con diferentes condiciones de pendiente.
- Contextualización espacial de información agronómica.
- Apoyo al análisis de escurrimiento superficial.
- Integración con datos de productividad y manejo agrícola.

### 15.2. Manejo del agua y drenaje

La topografía constituye un factor determinante en el comportamiento del agua sobre la superficie terrestre.

Los DEM permiten desarrollar análisis complementarios relacionados con:

- Dirección de escurrimiento.
- Acumulación de flujo.
- Identificación de zonas potenciales de concentración de agua.
- Delimitación de cuencas.
- Evaluación preliminar de condiciones topográficas de drenaje.

Estos análisis requieren algoritmos específicos y deben considerar las limitaciones del modelo de elevación.

### 15.3. Planificación predial

La información altimétrica puede utilizarse como antecedente para:

- Evaluación general de condiciones topográficas.
- Planificación espacial de actividades agrícolas.
- Reconocimiento de sectores con diferentes gradientes altimétricos.
- Análisis preliminar de accesibilidad.
- Integración de información topográfica con cartografía predial.

No obstante, los productos derivados de DEM de resolución moderada deben utilizarse con precaución en decisiones que requieran precisión topográfica.

## **16. Síntesis conceptual**

El procesamiento de Modelos Digitales de Elevación constituye una aplicación relevante de la ciencia de datos geoespaciales, debido a que permite transformar información altimétrica en productos cartográficos y analíticos mediante procedimientos computacionales. La generación de curvas de nivel representa una de las principales aplicaciones de estos modelos, permitiendo interpretar la distribución espacial de las elevaciones y reconocer características generales del relieve.

El flujo de trabajo desarrollado en el notebook integra adquisición de datos, exploración de metadatos, reproyección, remuestreo, recorte espacial, suavizado Gaussiano y extracción de curvas de nivel mediante Python y GDAL.

La aplicación a escala regional ofrece una visión macro del comportamiento del territorio y sus grandes unidades morfológicas; la escala comunal permite obtener una representación general del relieve local; mientras que el procesamiento predial facilita una visualización espacialmente delimitada de las variaciones altimétricas específicas.

Sin embargo, la interpretación de los resultados exige distinguir entre resolución espacial, precisión vertical y nivel de detalle cartográfico. La generación de curvas con intervalos pequeños no implica necesariamente una mayor precisión del terreno representado. Esto se debe a que **el nivel de detalle utilizable en una escala predial está intrínsecamente limitado por la resolución espacial del Modelo Digital de Elevación (MDE) de origen y el Error Medio Cuadrático (RMSE) de sus datos base.**

Cuando se fuerzan intervalos de isolíneas menores que la resolución del MDE o que la incertidumbre vertical del sensor, el proceso de interpolación simplemente reescribe o suaviza matemáticamente la misma malla de datos base. Lejos de aportar información morfológica nueva, esta práctica genera una falsa sensación de precisión (artesanía o ruido cartográfico), donde la densidad de líneas representa artefactos geométricos propios del algoritmo de interpolación y no microtopografía real del terreno. En consecuencia, si la densidad de puntos o el tamaño del píxel del modelo de origen —diseñado conceptualmente para coberturas regionales o comunales— no captura variaciones a métrica predial, subdividir los intervalos altimétricos solo sobresatura la representación cartográfica sin incrementar la exactitud topográfica real.

**El principio fundamental de esta materia es comprender que el procesamiento geoespacial permite transformar y analizar información topográfica, pero no puede generar precisión altimétrica que no esté presente en los datos originales.**

## Referencia al material de estudio

Este apunte fue elaborado con el fin de facilitar la comprensión del flujo computacional en el notebook [Apunte práctico: Procesamiento de Modelos Digitales de Elevación (DEM) y Generación de Curvas de Nivel]()

---

## Bibliografía y recursos:

- **Materiales bibliográficos:**
    - (Book) Dorman, M., Graser, A., Nowosad, J., & Lovelace, R. (2025). Geocomputation with Python. CRC Press. https://py.geocompx.org/

    - (Book) Tenkanen, H., Heikinheimo, V., & Whipp, D. (s. f.). Introduction to Python for Geographic Data Analysis. https://pythongis.org/

    - (Course) Python Foundation for Spatial Analysis Course by Ujaval Gandhi https://courses.spatialthoughts.com/python-foundation.html

- **Rasterio:** https://rasterio.readthedocs.io/
- **Rioxarray:** https://corteva.github.io/rioxarray/
- **GeoPandas:** https://geopandas.org/
- **GDAL:** https://gdal.org/
- **NumPy:** https://numpy.org/doc/
- **SciPy:** https://docs.scipy.org/doc/scipy/
- **Matplotlib:** https://matplotlib.org/
- **Google Colab:** https://colab.research.google.com/

---

**Recopilación y edición:** Javiera González Mardones *(2026)* \
Redacción con asistencia de IA, supervisada.
