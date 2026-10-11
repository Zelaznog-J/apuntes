# Curvas de nivel desde un ráster con GDAL y Python

!!! question "Pregunta guía"
    ¿Qué hace exactamente el computador cuando "dibuja" una curva, y cómo lo controlo desde la terminal o desde Python?

> **Cómo leer este subcapítulo.** Profundiza el Paso 1 y el Paso 4 (b y c) de la sección 8 de [Curvas de nivel: conceptos y métodos](index.md). Lectura estimada: 55–70 minutos. Al terminar, ejecuta el [laboratorio](laboratorio.ipynb).

---

## Resultados de aprendizaje

Al terminar este subcapítulo podrás:

1. Explicar con tus palabras cómo un computador convierte una grilla de alturas en líneas.
2. Obtener un DEM real (gratuito o de mayor resolución) y juzgar si sirve para tu propósito.
3. Inspeccionar y preparar un DEM antes de contornearlo.
4. Configurar VS Code con GDAL y Python, y ejecutar `gdal_contour` de cuatro maneras distintas.
5. Generar curvas de nivel con `gdal_contour`, controlando intervalo, nivel base, niveles específicos y atributos.
6. Generar las mismas curvas con Python (rasterio, scikit-image, geopandas) y entender cada línea del código.
7. Elegir entre ambos métodos según la situación.
8. Detectar y corregir problemas típicos del resultado.

---

## 1. La idea general (sin código todavía)

### 1.1 ¿Qué es un ráster de elevación?

Piensa en una planilla de cálculo gigante donde cada celda guarda **una altura**. Esa planilla, además, "sabe" a qué lugar del mundo corresponde: tiene una esquina de origen, un tamaño de celda (por ejemplo, 30 m) y un sistema de coordenadas. A eso lo llamamos **DEM** en formato ráster (por ejemplo, un archivo `.tif`).

> **Imagen sugerida 1:** Una grilla pequeña (6×6) con números de altura escritos en cada celda y, al lado, la misma grilla coloreada de claro (bajo) a oscuro (alto). Pie: *"Un DEM es una tabla de alturas con ubicación geográfica."* Ubicación: al final de 1.1.

### 1.2 ¿Qué queremos obtener?

Queremos pasar de **celdas** (datos ráster) a **líneas** (datos vectoriales) que unan puntos de igual altura. En el camino ocurre un cambio importante: el ráster solo conoce alturas en el *centro* de cada celda, pero la curva debe pasar *entre* celdas. Para ubicarla se **interpola**.

### 1.3 La receta universal en tres pasos

Tanto GDAL como Python hacen, en el fondo, lo mismo:

1. **Elegir los niveles** que se quieren dibujar (por ejemplo 100, 105, 110… m).
2. **Buscar los cruces:** para cada nivel, encontrar dónde la superficie pasa de estar "por debajo" a "por encima" de ese valor.
3. **Unir los cruces** vecinos en líneas continuas y guardarlas con su altura como atributo.

Lo que cambia entre métodos es la herramienta, la comodidad y el grado de control. El corazón matemático es el mismo.

---

## 2. Cómo funciona por dentro: el algoritmo de cuadrados (*marching squares*)

Entender este algoritmo te ayuda a interpretar resultados y errores.

### 2.1 Paso A: sobre o bajo el nivel

Supón que quieres la curva de **20 m**. Para cada celda preguntas: ¿su altura es mayor o menor que 20? Así el ráster se convierte, mentalmente, en un mapa de "sí/no".

### 2.2 Paso B: mirar de a cuatro

Se toman cuatro celdas vecinas que forman un cuadrado (sus centros son las esquinas del cuadrado). Hay 16 combinaciones posibles de "sobre/bajo". Algunas no tienen curva (las cuatro sobre o las cuatro bajo). Otras tienen una línea que corta el cuadrado por dos de sus lados.

### 2.3 Paso C: ubicar el cruce con precisión

Si un lado va de 16 m a 26 m y buscamos 20 m, la curva cruza a **40 %** del camino:

```
fracción = (nivel − altura_A) / (altura_B − altura_A)
         = (20 − 16) / (26 − 16) = 0,4
```

Esa interpolación lineal evita que las curvas salgan "escalonadas" siguiendo los bordes de las celdas.

### 2.4 Paso D: encadenar

Los pequeños segmentos de cada cuadrado se unen con los de los cuadrados vecinos hasta formar líneas largas, abiertas (si llegan al borde del ráster) o cerradas (si dan la vuelta).

> **Imagen sugerida 2:** Secuencia de tres paneles sobre una grilla 4×4: (a) celdas coloreadas según estén sobre/bajo el nivel 20, (b) los segmentos de curva dentro de cada cuadrado con los puntos de cruce marcados en los bordes, (c) segmentos unidos en una sola línea. Ubicación: al final de la sección 2.

> **Nota:** hay un caso ambiguo (dos esquinas opuestas "sobre" y dos "bajo") en que la curva podría unirse de dos maneras. Cada software lo resuelve con una regla propia; es una razón por la que GDAL y Python pueden diferir levemente en detalles muy finos.

---

## 3. Cómo obtener un DEM real

Para practicar necesitas un archivo de elevación de verdad. Hay tres caminos, de más simple a más exigente:

1. **Descargar un DEM global gratuito** (cobertura mundial, unos 30 m de celda). Sirve para aprender y para análisis de cuenca.
2. **Conseguir datos de mayor resolución** de organismos públicos, universidades o empresas (útil a escala predial).
3. **Generar tu propio DEM** con dron o con un levantamiento GNSS/topográfico.

### 3.1 Cómo elegir: cinco preguntas

| Pregunta | Por qué importa |
|---|---|
| ¿Qué decisión voy a tomar y a qué escala? | Una cuenca de 5.000 ha tolera celdas de 30 m; el trazado de hileras en un huerto de 10 ha, no. |
| ¿Es un MDT o un MDS? | Los DEM globales derivados de radar suelen reflejar la superficie con vegetación y construcciones; no son un MDT "puro". |
| ¿Qué precisión vertical tiene en mi zona? | Define la equidistancia mínima razonable (sección 3.6). |
| ¿Qué licencia tiene? | Determina si puedes usarlo en clases, publicarlo o venderlo, y cómo citarlo. |
| ¿En qué CRS y datum viene? | Casi todos los globales vienen en grados (EPSG:4326); hay que reproyectar a metros. |

### 3.2 Fuentes gratuitas de cobertura global

| Producto | Celda aprox. | Tipo | Dónde se obtiene | Comentarios |
|---|---|---|---|---|
| **Copernicus DEM GLO-30** | 30 m | MDS (radar TanDEM-X) | OpenTopography; bucket público en AWS (`copernicus-dem-30m`) | Gratuito bajo licencia Copernicus. Formato GeoTIFF optimizado para la nube (COG). La versión pública en AWS no incluye algunos países. |
| **Copernicus DEM GLO-90** | 90 m | MDS | Bucket público en AWS (`copernicus-dem-90m`) | Para escalas muy regionales. |
| **SRTM 1 arc-second** | 30 m | Radar (misión del año 2000) | USGS EarthExplorer; OpenTopography | Cobertura entre unos 60° N y 56° S; verifica tu zona. |
| **NASADEM** | 30 m | Reprocesamiento de SRTM | NASA Earthdata; OpenTopography | Corrige parte de los huecos y errores de SRTM. |
| **ALOS World 3D (AW3D30)** | 30 m | Óptico estéreo (satélite ALOS) | JAXA (registro gratuito); OpenTopography | Muy usado en estudios de montaña. |
| **ASTER GDEM** | 30 m | Óptico estéreo | NASA Earthdata | Puede tener más artefactos locales. |

> **Un dato útil para Chile:** un estudio de validación en los Andes Centrales de Chile comparó siete DEM globales con puntos GNSS y datos del satélite ICESat-2. A escala local, ALOS World 3D 30 m fue el de mejor desempeño, seguido de ASTER GDEM v3, pero con errores verticales del orden de **decenas de metros** en alta montaña (Revista Geográfica de Chile *Terra Australis*). Moraleja: la precisión depende de la zona y del relieve; **valida siempre con puntos de control** antes de fijar una equidistancia.

> **Nota:** las versiones, los accesos y las condiciones de uso cambian. Antes de usar un producto en clases, confirma su versión y su licencia en la página oficial.

### 3.3 Datos de mayor resolución para predios

- **Organismos públicos chilenos.** Consulta la infraestructura de datos geoespaciales (IDE Chile), el Instituto Geográfico Militar (IGM), el Centro de Información de Recursos Naturales (CIREN) y el Servicio Aerofotogramétrico (SAF). Algunos tienen cartografía, modelos de elevación o vuelos LiDAR de ciertas zonas. La disponibilidad cambia: pregunta por la cobertura de tu predio, la resolución, la fecha del vuelo y la licencia.
- **Universidades y proyectos de investigación.** Muchos proyectos generan DEM de alta resolución que pueden compartirse con fines académicos.
- **Dron propio.** Un vuelo fotogramétrico produce un ortomosaico y un modelo de superficie (MDS) de pocos centímetros. Para curvas del suelo hay que obtener un MDT filtrando vegetación (ver [capítulo principal](index.md), sección 4.2). Programas libres como OpenDroneMap permiten procesarlo.
- **Levantamiento topográfico o GNSS.** Entrega puntos (x, y, z) que se interpolan a ráster (por ejemplo con `gdal_grid` o QGIS) o se convierten en un TIN.
- **Productos comerciales.** Modelos derivados de imágenes estéreo de satélite, con costo y licencias propias.

### 3.4 Paso a paso: cuatro formas de descargar un DEM

#### A) Desde un portal web (OpenTopography)

1. Entra al sitio de OpenTopography y busca la herramienta de **Global DEMs**.
2. Elige el producto (por ejemplo, **Copernicus GLO-30**).
3. Dibuja un rectángulo sobre tu zona de interés, un poco más grande que el predio (recuerda el margen de seguridad).
4. Elige el formato **GeoTIFF** y ejecuta la descarga. Puede pedirte crear una cuenta gratuita.
5. Guarda el archivo en la carpeta `datos/` de tu proyecto.

> **Imagen sugerida 3:** Captura anotada del portal de OpenTopography con el producto Copernicus GLO-30 seleccionado, un rectángulo dibujado sobre una zona de Chile central y flechas numeradas (1: producto, 2: rectángulo, 3: formato GeoTIFF, 4: botón de descarga). Ubicación: al final del método A.

#### B) Desde USGS EarthExplorer (SRTM)

1. Crea una cuenta gratuita en EarthExplorer e inicia sesión.
2. En **Search Criteria**, define tu área (dibujando un polígono, ingresando coordenadas o subiendo un archivo).
3. En **Data Sets**, abre *Digital Elevation* y marca **SRTM 1 Arc-Second Global**.
4. En **Results**, descarga la escena en formato GeoTIFF.
5. Si el área abarca varias escenas, únelas después con `gdalbuildvrt` o `gdal_merge`.

#### C) Con un script de Python (teselas Copernicus por HTTP)

El Copernicus DEM se publica en teselas de 1° × 1°. Cada tesela se nombra con la coordenada de su **esquina suroeste**. Por ejemplo, la tesela `S34_00_W071_00` cubre desde 34° S hasta 33° S y desde 71° W hasta 70° W, es decir, una parte importante de Santiago y su entorno.

> **Imagen sugerida 4:** Grilla de 1° × 1° sobre un mapa de Chile central, con la tesela `S34_00_W071_00` resaltada, sus esquinas rotuladas (34° S, 33° S, 71° W, 70° W) y una flecha que indique "la esquina suroeste da el nombre". Ubicación: antes del código del método C.

```python
import math
import pathlib
import urllib.request

def nombre_tesela(lat_sw: int, lon_sw: int) -> str:
    """Nombre de la tesela Copernicus GLO-30 según su esquina suroeste."""
    ns = "N" if lat_sw >= 0 else "S"
    ew = "E" if lon_sw >= 0 else "W"
    return f"Copernicus_DSM_COG_10_{ns}{abs(lat_sw):02d}_00_{ew}{abs(lon_sw):03d}_00_DEM"

def descargar_tesela(lat: float, lon: float, carpeta: str = "datos") -> pathlib.Path:
    """Descarga la tesela que contiene el punto (lat, lon), en grados decimales."""
    lat_sw, lon_sw = math.floor(lat), math.floor(lon)   # esquina suroeste
    nombre = nombre_tesela(lat_sw, lon_sw)
    url = (f"https://copernicus-dem-30m.s3.amazonaws.com/"
           f"{nombre}/{nombre}.tif")
    destino = pathlib.Path(carpeta)
    destino.mkdir(exist_ok=True)
    salida = destino / f"{nombre}.tif"
    if not salida.exists():
        urllib.request.urlretrieve(url, salida)
    return salida

# Ejemplo: un punto cerca de Santiago (lat -33,45; lon -70,67)
ruta = descargar_tesela(-33.45, -70.67)
print("Descargado en:", ruta)
```

Cómo leerlo:

- `math.floor` redondea **hacia abajo**: −33,45 pasa a −34 y −70,67 pasa a −71. Así se obtiene la esquina suroeste, incluso en el hemisferio sur y al oeste de Greenwich.
- La URL sigue el patrón público del bucket de AWS. Si la tesela no existe (zonas no liberadas, océano) la descarga falla con un error HTTP.
- Si tu predio cae en el borde entre dos teselas, descarga ambas y únelas (`gdalbuildvrt` o `rasterio.merge`).

#### D) Con GDAL, recortando directamente sin descargar la tesela completa

GDAL puede leer archivos remotos con el prefijo `/vsicurl/`. Como el DEM está en formato COG, GDAL pide solo la parte necesaria:

```bash
gdal_translate -projwin -70.80 -33.30 -70.60 -33.50 \
  /vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_S34_00_W071_00_DEM/Copernicus_DSM_COG_10_S34_00_W071_00_DEM.tif \
  datos/dem_wgs84.tif
```

- `-projwin` recibe: `x_izq y_arriba x_der y_abajo` (en este caso, longitud/latitud porque el DEM está en grados).
- Es la forma más rápida de obtener solo tu predio.
- Requiere una instalación de GDAL con soporte de red (las versiones de conda-forge y OSGeo4W suelen incluirlo).
- En Windows (cmd) reemplaza `\` por `^` al final de las líneas, o escribe el comando en una sola línea.

### 3.5 Después de descargar: revisar y dejar el DEM listo

Un DEM de Copernicus viene en grados (EPSG:4326). Antes de contornear conviene reproyectarlo a un sistema métrico y fijar la celda:

```bash
gdalinfo datos/dem_wgs84.tif

# Reproyectar a UTM 19 sur con celda de 30 m
gdalwarp -t_srs EPSG:32719 -tr 30 30 -r bilinear \
  datos/dem_wgs84.tif datos/dem_utm.tif
```

- Ajusta el EPSG a tu zona (en Chile continental suelen ser 32718, 32719 o 32720, según la longitud).
- Una celda de 1 segundo de arco equivale a unos 30 m, por eso `-tr 30 30` es razonable aquí.
- Revisa la **referencia vertical** en la documentación del producto: los DEM globales usan alturas referidas a un geoide (la versión depende del producto), mientras que un GNSS entrega alturas elipsoidales. Si comparas con puntos de campo, convierte primero.

### 3.6 ¿Qué equidistancia permite un DEM de 30 m?

Aplica la regla del [capítulo principal](index.md): la equidistancia no debería ser menor que unas 2–3 veces el RMSE vertical. Con un DEM global de 30 m, donde el error puede ir de pocos metros a decenas de metros según el relieve, lo habitual es trabajar con **10 m o más**. Para un predio con curvas cada 1 o 2 m necesitas datos de dron, LiDAR o topografía.

> **Imagen sugerida 5:** Dos mapas del mismo sector de ladera: izquierda con curvas de 10 m obtenidas de un DEM de 30 m, derecha con curvas de 1 m obtenidas de un DEM de dron de 10 cm. Rotular fuente, celda y equidistancia. Ubicación: al final de 3.6, para mostrar por qué la resolución define el uso.

### 3.7 Licencia y citación

- Los datos Copernicus y SRTM se pueden usar gratuitamente, pero **con condiciones**: lee la licencia y cita la fuente en tus mapas e informes.
- Incluye siempre en el pie del mapa el nombre del producto, la versión y el año de descarga.
- Los datos de organismos públicos o de proyectos académicos pueden tener restricciones de redistribución.

---

## 4. Antes de contornear: preparar y revisar el DEM

Un buen resultado empieza antes de ejecutar cualquier comando. Esta revisión es común a ambos métodos.

### 4.1 Checklist previo

| Pregunta | Por qué importa | Cómo revisarlo |
|---|---|---|
| ¿Cuál es el sistema de coordenadas? | Si está en grados, las distancias horizontales no están en metros. | `gdalinfo dem.tif` |
| ¿Cuál es el tamaño de celda? | Define el detalle máximo posible. | `gdalinfo dem.tif` |
| ¿Cuál es el valor NoData? | Si no se declara, `-9999` se tomará como altura real. | `gdalinfo dem.tif` |
| ¿Las alturas son enteras o decimales? | Alturas enteras producen curvas con "escalones" en terreno plano. | Tipo de dato (`Int16` vs `Float32`) |
| ¿Es MDT o MDS? | Para curvas del suelo se necesita el MDT. | Documentación de la fuente |
| ¿Hay huecos o valores absurdos? | Generan curvas espurias. | Visualizar en QGIS con un *hillshade* |

### 4.2 Revisar con `gdalinfo`

```bash
gdalinfo dem.tif
```

Fíjate en estos datos de la salida:

- `Size is ...` → número de columnas y filas.
- `Coordinate System is ...` → CRS.
- `Pixel Size = ...` → tamaño de celda.
- `NoData Value=...` → valor que se ignora.
- `Type=...` → tipo de dato (Int16, Float32, etc.).

Para ver estadísticas (mínimo y máximo) usa:

```bash
gdalinfo -stats dem.tif
```

Esto te dice el rango de alturas y, con él, qué niveles tiene sentido dibujar.

### 4.3 Recortar y reproyectar (si hace falta)

```bash
# Reproyectar a UTM zona 19 sur (ejemplo; ajusta el EPSG a tu zona)
gdalwarp -t_srs EPSG:32719 -r bilinear dem.tif dem_utm.tif

# Recortar con un margen de seguridad (xmin ymax xmax ymin)
gdal_translate -projwin 340000 6300000 345000 6295000 dem_utm.tif dem_recorte.tif
```

Notas:

- `-r bilinear` es un método de remuestreo adecuado para datos continuos como la altura (evita `nearest` si quieres superficies suaves).
- Recorta **con margen** un poco mayor al área de interés, para evitar efectos de borde.
- El valor de EPSG depende de tu zona; verifica el que corresponde a tu predio.

---

## 5. Preparar VS Code y ejecutar `gdal_contour`

Hasta aquí usamos comandos sueltos. Ahora los llevamos a un entorno de trabajo ordenado: **Visual Studio Code (VS Code)**, donde puedes tener a la vez tus archivos, una terminal y tus scripts de Python.

### 5.1 Qué necesitas instalado

| Componente | Para qué | Cómo conseguirlo |
|---|---|---|
| **VS Code** | Editor y terminal integrada | Instalador oficial desde el sitio de VS Code |
| **Extensión Python** (Microsoft) | Elegir el entorno, ejecutar y depurar scripts | Panel *Extensions* (Ctrl+Shift+X) → buscar "Python" |
| **GDAL** (con sus comandos) | `gdal_contour`, `gdalinfo`, `gdalwarp` | Ver 5.2 |
| **Bibliotecas de Python** | rasterio, geopandas, scikit-image, etc. | Ver 5.2 |

### 5.2 Instalar GDAL y Python de forma ordenada

La forma más simple y reproducible es usar un **entorno de conda** con el canal *conda-forge*, que instala GDAL con sus comandos y las bibliotecas de Python compatibles entre sí. Si no tienes conda, instala Miniforge o Miniconda.

```bash
conda create -n geo -c conda-forge python gdal rasterio geopandas scikit-image scipy matplotlib
conda activate geo
```

- `-n geo` es el nombre del entorno (puedes elegir otro).
- Instalar todo **en un solo comando** evita conflictos de versiones.
- Evita mezclar `pip install` y `conda install` para GDAL y rasterio dentro del mismo entorno: es una causa frecuente de errores.

Alternativas según el sistema operativo:

- **Windows:** el instalador OSGeo4W (incluido con QGIS) entrega una consola con GDAL ya configurado.
- **macOS:** `brew install gdal`.
- **Ubuntu/Debian:** `sudo apt install gdal-bin`.

### 5.3 Organizar el proyecto

1. En VS Code: **File → Open Folder** y elige (o crea) una carpeta para el proyecto.
2. Crea esta estructura:

```
curvas_de_nivel/
├── datos/        # DEM descargados (originales, no se editan)
├── salidas/      # curvas, hillshade, mapas
└── scripts/      # archivos .py
```

Separar originales y resultados evita sobrescribir datos y facilita repetir el trabajo.

> **Imagen sugerida 6:** Captura de VS Code con el explorador de archivos a la izquierda mostrando las carpetas `datos`, `salidas` y `scripts`. Ubicación: al final de 5.3.

### 5.4 Elegir el intérprete y abrir la terminal

1. Abre la paleta de comandos con **Ctrl+Shift+P** (en macOS, Cmd+Shift+P).
2. Escribe **Python: Select Interpreter** y elige el entorno `geo`. Si no aparece, revisa que el entorno tenga Python instalado y reinicia VS Code.
3. Abre la terminal integrada con **Ctrl+\`** (o menú *Terminal → New Terminal*). Si el entorno está seleccionado, debería activarse solo; verás `(geo)` al inicio de la línea.
4. Si no se activó, escribe `conda activate geo`.

Comprueba que todo funciona:

```bash
gdalinfo --version
gdal_contour --help
python -c "import rasterio, geopandas; print('ok')"
```

Si estos comandos responden, estás listo. Si alguno falla, revisa la sección 5.9.

> **Imagen sugerida 7:** Captura de VS Code con tres zonas marcadas: (1) el selector de intérprete en la barra inferior mostrando `geo`, (2) la terminal integrada con `(geo)` en el prompt y la salida de `gdalinfo --version`, (3) el explorador de archivos. Ubicación: al final de 5.4.

> **Nota sobre Windows y PowerShell:** la activación automática de entornos de conda puede no funcionar en algunas configuraciones de PowerShell. Si te ocurre, cambia el perfil de la terminal a *Command Prompt* (flecha junto al botón "+" de la terminal → *Select Default Profile*) o ejecuta `conda init powershell` una vez y reinicia VS Code.

### 5.5 Ejecutar `gdal_contour` en la terminal integrada

1. Ubícate en la carpeta del proyecto (la terminal normalmente se abre ahí). Compruébalo con `pwd` (macOS/Linux) o `cd` (Windows).
2. Revisa el DEM:

```bash
gdalinfo -stats datos/dem_utm.tif
```

3. Genera las curvas:

```bash
gdal_contour -a ELEV -i 10 datos/dem_utm.tif salidas/curvas_10m.gpkg
```

4. Verifica la salida:

```bash
ogrinfo -so -al salidas/curvas_10m.gpkg
```

Detalles prácticos:

- Las rutas son **relativas a la carpeta donde está la terminal**. Si aparece "no such file", casi siempre estás en otra carpeta.
- Si una ruta tiene **espacios**, enciérrala entre comillas: `"datos/mi dem.tif"`.
- Para partir un comando largo en varias líneas, el carácter de continuación depende de la terminal: `\` en bash/zsh, `` ` `` en PowerShell y `^` en cmd.
- Si repites el comando con el mismo archivo de salida, puede fallar o agregar otra capa. Cambia el nombre o borra el archivo anterior antes de volver a ejecutar (verifica el comportamiento en tu versión de GDAL).

### 5.6 Cuatro maneras de ejecutarlo desde VS Code

#### a) Directamente en la terminal
Es lo que hicimos en 5.5. Ideal para explorar y probar.

#### b) Con un archivo de comandos (reproducible)
Guarda los comandos en `scripts/curvas.sh` (macOS/Linux) o `scripts/curvas.bat` (Windows) y ejecútalos con un solo gesto.

`scripts/curvas.sh`:

```bash
#!/usr/bin/env bash
set -e                       # se detiene si un comando falla
mkdir -p salidas
gdal_contour -a ELEV -i 10 datos/dem_utm.tif salidas/curvas_10m.gpkg
gdal_contour -a ELEV -i 50 datos/dem_utm.tif salidas/curvas_50m.gpkg
echo "Listo"
```

Ejecútalo con `bash scripts/curvas.sh`.

`scripts/curvas.bat`:

```bat
@echo off
if not exist salidas mkdir salidas
gdal_contour -a ELEV -i 10 datos\dem_utm.tif salidas\curvas_10m.gpkg || exit /b 1
gdal_contour -a ELEV -i 50 datos\dem_utm.tif salidas\curvas_50m.gpkg || exit /b 1
echo Listo
```

Ejecútalo con `scripts\curvas.bat`.

#### c) Desde un script de Python (con `subprocess`)
Útil cuando el contorneo es un paso dentro de un flujo más grande. Guarda esto como `scripts/curvas_gdal.py`:

```python
import subprocess
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent      # carpeta del proyecto
dem = raiz / "datos" / "dem_utm.tif"
salida = raiz / "salidas" / "curvas_10m.gpkg"
salida.parent.mkdir(exist_ok=True)

subprocess.run(
    ["gdal_contour", "-a", "ELEV", "-i", "10", str(dem), str(salida)],
    check=True,        # detiene el script con un error claro si falla
)
print("Curvas generadas en:", salida)
```

Ejecútalo con el botón **▶ Run Python File** (arriba a la derecha del editor) o con `python scripts/curvas_gdal.py` en la terminal.

- `Path(__file__)` hace que las rutas no dependan de la carpeta desde la que ejecutes.
- Si aparece `FileNotFoundError: gdal_contour`, el entorno de conda no está activo en ese proceso. Ejecuta el script desde la terminal con `(geo)` activo.

#### d) Con una tarea de VS Code (un atajo para el comando)
Las *tasks* permiten lanzar el comando con un atajo. Crea `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Curvas de nivel 10 m",
      "type": "shell",
      "command": "conda",
      "args": [
        "run", "-n", "geo",
        "gdal_contour", "-a", "ELEV", "-i", "10",
        "${workspaceFolder}/datos/dem_utm.tif",
        "${workspaceFolder}/salidas/curvas_10m.gpkg"
      ],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": []
    }
  ]
}
```

- Lánzala con **Ctrl+Shift+B** (o *Terminal → Run Build Task*).
- `conda run -n geo` ejecuta el comando dentro del entorno `geo` sin depender de la activación de la terminal.
- `${workspaceFolder}` es la carpeta abierta en VS Code, así que las rutas no se rompen.

### 5.7 Ejecutar y depurar los scripts de Python

- **Ejecutar:** botón ▶ del editor, o clic derecho → *Run Python File in Terminal*.
- **Depurar:** F5. Puedes poner un punto de interrupción (clic a la izquierda del número de línea) y revisar los valores de `z`, `niveles` o `transform` mientras el código corre. Es muy útil para entender el script de la sección 7.
- **Por celdas:** si escribes `# %%` entre bloques de código y tienes la extensión Jupyter, VS Code ofrece "Run Cell" y una ventana interactiva donde ves los gráficos al instante.

### 5.8 Ver el resultado sin salir de VS Code

Un gráfico rápido con matplotlib, para comprobar que las curvas calzan con el DEM (ambos deben estar en el mismo CRS):

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show

with rasterio.open("datos/dem_utm.tif") as src:
    fig, ax = plt.subplots(figsize=(8, 8))
    show(src, ax=ax, cmap="terrain")                 # DEM de fondo
    curvas = gpd.read_file("salidas/curvas_10m.gpkg")
    curvas.plot(ax=ax, color="saddlebrown", linewidth=0.6)
    ax.set_title("DEM y curvas de nivel de 10 m")
plt.show()
```

> **Imagen sugerida 8:** Captura de la ventana de matplotlib con el DEM en colores hipsométricos y las curvas de nivel de 10 m en café, junto al código que la genera en el editor de VS Code. Ubicación: al final de 5.8.

### 5.9 Problemas frecuentes en VS Code

| Síntoma | Causa probable | Solución |
|---|---|---|
| `gdal_contour` no se reconoce como comando | GDAL no instalado o entorno sin activar | Activa el entorno (`conda activate geo`); en Windows prueba la consola de OSGeo4W. |
| `ModuleNotFoundError: rasterio` | VS Code usa otro intérprete de Python | **Ctrl+Shift+P → Python: Select Interpreter** y elige `geo`; mira el intérprete en la barra inferior. |
| El entorno no aparece en la lista | El entorno no contiene Python | Recréalo incluyendo `python` en el comando de conda. |
| Se activa el entorno equivocado | Se abrió una terminal antes de elegir el intérprete | Cierra la terminal y abre una nueva con *Terminal → New Terminal*. |
| Avisos de `PROJ` o `GDAL_DATA` | Mezcla de instalaciones (pip + conda, o varias copias de GDAL) | Usa un entorno limpio e instala todo desde conda-forge. |
| "No such file or directory" | La terminal está en otra carpeta | Verifica con `pwd`/`cd`, o usa rutas completas o `Path(__file__)`. |
| Rutas de Windows se rompen en Python | Las barras invertidas se interpretan como escapes | Usa `pathlib.Path`, barras normales `/` o cadenas crudas `r"C:\datos\dem.tif"`. |
| PowerShell bloquea la activación | Política de ejecución de scripts | Cambia a *Command Prompt* o ejecuta `conda init powershell` y reinicia. |
| La tarea de `tasks.json` no encuentra el comando | La tarea no hereda el entorno | Usa `conda run -n geo ...` como en 5.6d. |

---

## 6. Método 1: GDAL (`gdal_contour`)

### 6.1 ¿Qué es GDAL y por qué usarlo?

**GDAL** es una biblioteca de código abierto para leer y escribir datos geoespaciales. Muchísimos programas (QGIS, ArcGIS, R, Python) la usan por debajo. Sus herramientas de línea de comandos son rápidas, repetibles y fáciles de automatizar.

**Cuándo conviene:** cuando quieres un resultado rápido, estándar y reproducible, sobre rásters grandes, o integrar el proceso en un script de lotes.

### 6.2 El comando más simple

```bash
gdal_contour -a ELEV -i 5 dem.tif curvas.gpkg
```

Lectura "en español":

> "Toma `dem.tif`, genera una curva cada **5** unidades de altura (`-i 5`), guarda la altura en un campo llamado **ELEV** (`-a ELEV`) y escribe el resultado en `curvas.gpkg`."

Esto produce un archivo vectorial de **líneas**, cada una con su altura como atributo.

> **Imagen sugerida 9:** Captura de terminal con el comando y, al lado, el resultado abierto en QGIS sobre el DEM en transparencia. Flechas que conecten cada parte del comando (`-a`, `-i`, entrada, salida) con su significado. Ubicación: al final de 6.2.

### 6.3 Opciones más usadas

| Opción | Qué hace | Ejemplo |
|---|---|---|
| `-i` | Intervalo (equidistancia) entre curvas. | `-i 10` |
| `-a` | Nombre del campo donde guarda la altura. | `-a ELEV` |
| `-off` | Desplaza el nivel de partida (nivel base). | `-off 2` |
| `-fl` | Lista de niveles fijos, en lugar de un intervalo. | `-fl 100 250 500` |
| `-b` | Banda del ráster a usar (por defecto, la 1). | `-b 1` |
| `-snodata` | Valor que se tratará como NoData si el archivo no lo declara. | `-snodata -9999` |
| `-inodata` | Ignora el valor NoData declarado y usa todos los píxeles. | `-inodata` |
| `-3d` | Guarda la altura como coordenada Z de la geometría. | `-3d` |
| `-nln` | Nombre de la capa de salida. | `-nln curvas_5m` |
| `-f` | Formato de salida (GPKG, ESRI Shapefile, GeoJSON…). | `-f GPKG` |
| `-p` | Genera **polígonos** (áreas entre niveles) en lugar de líneas. Requiere una versión de GDAL que lo soporte (≥ 2.4) y los atributos `-amin`/`-amax`. | `-p -amin ELEV_MIN -amax ELEV_MAX` |

> **Verifica tu versión** con `gdal_contour --version` o `gdalinfo --version`, y consulta la ayuda con `gdal_contour --help`, porque las opciones disponibles dependen de la versión instalada. Las versiones más recientes de GDAL también incorporan una sintaxis unificada (`gdal raster contour ...`); revisa la documentación oficial de la versión que uses.

### 6.4 Entender `-i` y `-off` con un ejemplo

Con `-i 10`, GDAL dibuja curvas en 0, 10, 20, 30… (múltiplos de 10).

Si necesitas que partan desde otro valor, usas `-off`. Por ejemplo, `-i 10 -off 5` genera curvas en 5, 15, 25, 35… Es útil cuando quieres curvas de "cotas redondas" distintas, o alinear con cartografía existente.

### 6.5 Curvas de niveles específicos

Para marcar solo ciertas cotas (por ejemplo, el nivel donde llega un embalse proyectado):

```bash
gdal_contour -a ELEV -fl 420 425 430 dem.tif niveles_embalse.gpkg
```

### 6.6 Generar maestras e intermedias en dos pasadas

Una forma práctica de clasificar sin editar atributos después:

```bash
gdal_contour -a ELEV -i 5  dem.tif intermedias.gpkg
gdal_contour -a ELEV -i 25 dem.tif maestras.gpkg
```

Luego, en QGIS, simbolizas las maestras con línea gruesa y las intermedias con línea delgada. Alternativa: una sola pasada y luego una columna `TIPO` con una regla (cota múltiplo de 25 → maestra).

### 6.7 Salidas: ¿qué formato elegir?

- **GeoPackage (`.gpkg`)**: recomendado. Un solo archivo, sin límite práctico de 2 GB ni de 10 caracteres en nombres de campos.
- **Shapefile**: compatible con todo, pero con limitaciones (nombres de campo cortos, varios archivos).
- **GeoJSON**: ideal para web, pero pesado en grandes volúmenes.

### 6.8 Verificar el resultado

```bash
ogrinfo -so -al curvas.gpkg
```

Muestra el número de entidades, el CRS y los campos. Luego, **mira el mapa**: superpón las curvas a un sombreado de relieve:

```bash
gdaldem hillshade dem.tif hillshade.tif
```

Si las curvas "encajan" con las formas del sombreado (cauces, lomas), vas por buen camino.

### 6.9 Usar GDAL desde Python (sin salir de GDAL)

GDAL también se puede llamar desde Python, útil para automatizar. Una forma sencilla y robusta es ejecutar el comando desde un script:

```python
import subprocess

subprocess.run([
    "gdal_contour",
    "-a", "ELEV",
    "-i", "5",
    "dem.tif",
    "curvas.gpkg",
], check=True)
```

`check=True` hace que el script se detenga con un error claro si el comando falla.

### 6.10 Ventajas y limitaciones del método GDAL

**Ventajas**

- Rápido, incluso con rásters muy grandes.
- Una sola línea de comando; fácil de repetir y documentar.
- Maneja NoData y formatos de salida de forma nativa.

**Limitaciones**

- Menos control fino sobre qué hacer con cada línea (filtrado, suavizado, reglas propias).
- Las curvas salen "tal cual" del DEM; si el DEM tiene ruido, el ruido aparece en las curvas.

---

## 7. Método 2: Python (rasterio + scikit-image + geopandas)

### 7.1 ¿Por qué usar Python si GDAL ya lo hace?

Porque en Python **tú controlas cada etapa**: puedes suavizar el DEM, elegir los niveles con una regla propia, descartar curvas pequeñas, asignar atributos (maestra/intermedia), simplificar geometrías y combinar con otros análisis (pendiente, cuencas, estadísticas) en un mismo flujo.

**Cuándo conviene:** cuando quieres personalizar, automatizar procesos complejos o integrar el contorneo dentro de un análisis más grande.

### 7.2 Las herramientas y su papel

| Biblioteca | Para qué la usamos |
|---|---|
| `rasterio` | Leer el DEM y su georreferenciación (transformación, CRS, NoData). |
| `numpy` | Manejar la grilla como una matriz de números. |
| `scipy.ndimage` | (Opcional) Suavizar el DEM. |
| `scikit-image` | Función `find_contours`, que implementa *marching squares*. |
| `shapely` | Crear las geometrías de línea y simplificarlas. |
| `geopandas` | Reunir líneas y atributos en una tabla espacial y guardarla. |

Instalación (si hace falta):

```bash
pip install rasterio scikit-image shapely geopandas scipy numpy
```

### 7.3 Una idea clave: dos tipos de coordenadas

Esto es lo que más confunde al principio, así que vale la pena detenerse.

- **Coordenadas de matriz:** `(fila, columna)`. La fila 0 es la **superior**. Son números que cuentan celdas.
- **Coordenadas geográficas:** `(x, y)` en metros o grados, según el CRS.

`find_contours` trabaja en coordenadas de matriz y entrega valores **fraccionarios** (por ejemplo, fila 10,4 y columna 25,0), porque la curva pasa *entre* celdas. Para llevarlas al mapa se usa la **transformación afín** del ráster, que es la "regla de conversión" de celdas a coordenadas.

> **Imagen sugerida 10:** Diagrama con una grilla pequeña donde a la izquierda se muestran los ejes (fila, columna) con origen arriba a la izquierda, y a la derecha los ejes (x, y) geográficos con el norte arriba. Una flecha rotulada "transformación afín" une ambos. Ubicación: al final de 7.3.

### 7.4 Código completo (versión base)

```python
import numpy as np
import rasterio
from skimage import measure
from shapely.geometry import LineString
import geopandas as gpd

# --- 1. Parámetros ---
ruta_dem = "dem.tif"
ruta_salida = "curvas.gpkg"
equidistancia = 5          # metros
largo_minimo = 3           # nº mínimo de vértices para conservar una línea

# --- 2. Leer el DEM ---
with rasterio.open(ruta_dem) as src:
    z = src.read(1).astype(float)   # matriz de alturas
    transform = src.transform       # regla celdas -> coordenadas
    crs = src.crs                   # sistema de coordenadas
    nodata = src.nodata             # valor "sin dato"

# --- 3. Marcar NoData ---
if nodata is not None:
    z[z == nodata] = np.nan
mascara = np.isfinite(z)            # True donde hay dato válido
z_relleno = np.where(mascara, z, 0) # find_contours no acepta NaN

# --- 4. Definir los niveles ---
zmin, zmax = np.nanmin(z), np.nanmax(z)
primer_nivel = np.ceil(zmin / equidistancia) * equidistancia
niveles = np.arange(primer_nivel, zmax, equidistancia)

# --- 5. Buscar curvas nivel por nivel ---
registros = []
for nivel in niveles:
    for linea in measure.find_contours(z_relleno, nivel, mask=mascara):
        if len(linea) < largo_minimo:
            continue
        filas, cols = linea[:, 0], linea[:, 1]
        # celda (fila, col) -> coordenada del centro de la celda
        xs, ys = transform * (cols + 0.5, filas + 0.5)
        registros.append({
            "ELEV": float(nivel),
            "geometry": LineString(zip(xs, ys)),
        })

# --- 6. Guardar ---
curvas = gpd.GeoDataFrame(registros, crs=crs)
curvas.to_file(ruta_salida, driver="GPKG")
print(f"Curvas generadas: {len(curvas)}")
```

### 7.5 Lectura comentada, bloque por bloque

**Bloque 2: leer.** `src.read(1)` trae la primera banda como matriz de NumPy. La convertimos a decimales (`float`) para poder usar `NaN`.

**Bloque 3: NoData.** Las celdas "sin dato" no deben ser tratadas como alturas. Las convertimos a `NaN` (no es un número) y creamos una **máscara** que indica dónde sí hay datos válidos. `find_contours` no acepta `NaN`, así que rellenamos con 0 y le pasamos la máscara para que ignore esas celdas.

**Bloque 4: niveles.** Calculamos el menor múltiplo de la equidistancia que esté sobre la altura mínima (`np.ceil`) y generamos la lista hasta la altura máxima. Así, con `equidistancia = 5` y alturas entre 312 y 487, los niveles serán 315, 320, 325… 485.

**Bloque 5: el núcleo.** Para cada nivel, `find_contours` devuelve **una lista de líneas** (una por cada curva separada que exista a esa altura). Cada línea es una matriz con columnas `(fila, columna)`. Luego:

1. Descartamos líneas con muy pocos puntos (generalmente ruido).
2. Separamos filas y columnas.
3. Aplicamos la transformación afín. El `+ 0.5` desplaza al **centro** de la celda, porque `find_contours` cuenta desde el centro de las celdas y la transformación del ráster parte desde la esquina.
4. Construimos una `LineString` (línea) con sus coordenadas.

**Bloque 6: guardar.** Armamos una tabla espacial (cada fila = una línea con su altura) y la escribimos a un GeoPackage.

> **Verifica siempre el resultado en QGIS:** si las curvas aparecen desplazadas medio píxel o invertidas, revisa el manejo de la transformación (ver sección 9).

### 7.6 Mejora 1: suavizar el DEM antes de contornear

Si el DEM tiene ruido, las curvas salen dentadas. Un filtro gaussiano suave ayuda:

```python
from scipy.ndimage import gaussian_filter

# Rellenar huecos antes de suavizar para no "contagiar" el NaN a los vecinos
z_suave = gaussian_filter(z_relleno, sigma=1)   # sigma en celdas
z_suave = np.where(mascara, z_suave, np.nan)
```

- `sigma=1` es un suavizado leve; valores mayores suavizan más (y borran más detalle).
- Rellenar con 0 antes de suavizar distorsiona las alturas cerca de los bordes con NoData. Si tu DEM tiene muchos huecos, rellénalos mejor por interpolación (por ejemplo con `rasterio.fill.fillnodata`) antes de suavizar.
- Después de suavizar, vuelve a usar `z_suave` en lugar de `z` en los pasos siguientes.

> **Regla de oro:** suaviza el **DEM**, no la curva ya dibujada. Suavizar líneas por separado puede hacer que se crucen entre sí.

### 7.7 Mejora 2: clasificar maestras e intermedias

```python
curvas["TIPO"] = np.where(curvas["ELEV"] % (equidistancia * 5) == 0,
                          "maestra", "intermedia")
```

Con `equidistancia = 5`, las maestras caen cada 25 m.

### 7.8 Mejora 3: simplificar las líneas (reducir peso)

Las líneas pueden tener miles de vértices innecesarios. `simplify` reduce vértices respetando la forma:

```python
curvas["geometry"] = curvas.geometry.simplify(tolerance=0.5,
                                              preserve_topology=True)
```

- `tolerance` está en **unidades del CRS** (metros si usas UTM). Un valor cercano a la mitad del tamaño de celda suele ser razonable; prueba y compara visualmente.
- `preserve_topology=True` evita, en lo posible, que las líneas se crucen o se degeneren.

### 7.9 Mejora 4: etiquetar la altura como atributo de texto o 3D

Si necesitas la altura como coordenada Z en la geometría (útil para exportar a CAD o 3D), crea las líneas con tres coordenadas:

```python
from shapely.geometry import LineString
LineString([(x, y, nivel) for x, y in zip(xs, ys)])
```

### 7.10 Mejora 5: trabajar por zonas si el ráster es enorme

Cargar un DEM gigante en memoria puede ser inviable. Opciones:

- **Recortar** primero con GDAL (`gdal_translate -projwin`) y procesar por bloques o por sectores.
- Para un solo predio, normalmente basta recortar el DEM con un margen.
- Para áreas muy grandes, en general `gdal_contour` es más eficiente que la versión en Python.

### 7.11 Ventajas y limitaciones del método Python

**Ventajas**

- Control total: suavizado, filtros, reglas, atributos.
- Se integra con otros análisis y con visualización (matplotlib).
- Excelente para enseñar y entender el proceso paso a paso.

**Limitaciones**

- Más código y más posibilidades de errores (sobre todo con coordenadas).
- Más lento y con más consumo de memoria en rásters muy grandes.
- Es responsabilidad tuya manejar NoData, CRS y orientación correctamente.

---

## 8. Comparación directa

| Criterio | GDAL (`gdal_contour`) | Python (rasterio + skimage) |
|---|---|---|
| Facilidad de uso | Muy alta (un comando) | Media (requiere programar) |
| Velocidad en rásters grandes | Alta | Media/Baja |
| Control sobre el proceso | Básico | Total |
| Suavizado y filtros propios | No incluido | Sí, a medida |
| Reproducibilidad | Excelente (comando + versión) | Excelente (script + entorno) |
| Atributos personalizados | Limitado (altura) | Cualquiera |
| Ideal para | Producción rápida y estándar | Flujos personalizados e investigación |
| Riesgo de error | Bajo | Mayor (coordenadas, NoData) |

**Criterio práctico de decisión:**

- ¿Necesitas curvas estándar de un DEM, rápido? → **GDAL**.
- ¿Necesitas suavizar, filtrar, clasificar o encadenar con otros análisis? → **Python**.
- ¿Estás aprendiendo? → **Haz ambos** y compara resultados: es la mejor manera de entender el proceso.

> **Imagen sugerida 11:** Diagrama de flujo con dos ramas que parten del mismo DEM: rama izquierda (GDAL: un solo bloque "gdal_contour"), rama derecha (Python: bloques "leer → NoData → suavizar → find_contours → transformar → guardar"). Ambas convergen en "Archivo de curvas (.gpkg)". Ubicación: al final de la sección 8.

---

## 9. Problemas frecuentes y cómo resolverlos

| Síntoma | Causa probable | Solución |
|---|---|---|
| Curvas con alturas absurdas (por ejemplo, −9999 o 32767) | NoData no declarado | GDAL: `-snodata -9999`. Python: `z[z == -9999] = np.nan`. |
| Curvas desplazadas medio píxel | Se olvidó el `+ 0.5` o se usó la convención equivocada | Revisar la conversión fila/col → x/y. |
| Curvas "espejadas" o rotadas | Se intercambiaron filas y columnas | Recordar: `find_contours` entrega `(fila, columna)`. |
| Curvas en lugares que no corresponden | CRS mal asignado al guardar | Usar `crs=src.crs` al crear el GeoDataFrame. |
| Curvas "en escalera" en zonas planas | DEM con alturas enteras | Usar un DEM con decimales, o aumentar la equidistancia. |
| Muchísimas líneas diminutas | Ruido o mucha resolución para la equidistancia | Suavizar el DEM, descartar líneas cortas, subir la equidistancia. |
| Bordes extraños al límite del DEM | Sin margen en el recorte | Recortar con buffer y luego recortar las curvas al área final. |
| Archivo de salida enorme | Demasiados vértices | Simplificar o usar una equidistancia mayor. |
| Curvas "cuadradas" | DEM de baja resolución para la escala de trabajo | Usar un DEM de mejor resolución. |
| Resultados distintos entre GDAL y Python | Manejo del caso ambiguo, suavizado, NoData, medio píxel | Comparar con el mismo DEM sin suavizar y revisar la conversión de coordenadas. |

---

## 10. Comparar ambos métodos: un mini-experimento

Una excelente forma de aprender y de verificar tu código:

1. Genera curvas de 5 m con `gdal_contour` → `curvas_gdal.gpkg`.
2. Genera curvas de 5 m con el script de Python (sin suavizar) → `curvas_python.gpkg`.
3. Ábrelas en QGIS superpuestas, con colores distintos (por ejemplo, GDAL en azul, Python en rojo).
4. Haz zoom a un sector. Si ambas líneas casi coinciden, tu script está bien georreferenciado.
5. Revisa dónde difieren: normalmente en esquinas de NoData o en casos ambiguos.

> **Imagen sugerida 12:** Captura de QGIS con dos capas de curvas superpuestas (azul = GDAL, rojo = Python) en un sector; un círculo señala una zona donde difieren levemente y se rotula la posible causa. Ubicación: al final de la sección 10.

---

## 11. Ejemplo integrado: predio en ladera

**Contexto.** Predio de 25 ha, DEM de 1 m en `dem_predio.tif` (UTM, metros, alturas decimales).

**Objetivo.** Curvas cada 2 m con maestras cada 10 m, para planificar hileras.

**Ruta con GDAL (rápida).**

```bash
gdalinfo -stats dem_predio.tif
gdal_contour -a ELEV -i 2 dem_predio.tif curvas_2m.gpkg
```

Luego, en QGIS, se clasifica por `ELEV % 10 = 0` para simbolizar las maestras.

**Ruta con Python (personalizada).**

1. Suavizar el DEM con `sigma=1` para atenuar el ruido de la fotogrametría.
2. Generar curvas con `equidistancia = 2`.
3. Clasificar maestras con `ELEV % 10 == 0`.
4. Simplificar con tolerancia de 0,5 m.
5. Guardar en GeoPackage.

**Comparación sugerida.** Mide cuántas entidades y cuántos vértices produjo cada ruta, y evalúa qué tan "limpio" se ve el resultado en una zona de pendiente suave.

> **Imagen sugerida 13:** Dos mapas lado a lado del mismo sector del predio: izquierda con curvas directas de GDAL (más ruidosas), derecha con curvas desde un DEM suavizado en Python (más limpias). Rotular la equidistancia y la fuente. Ubicación: al final de la sección 11.

---

## 12. Resumen

- Un DEM ráster es una grilla de alturas georreferenciada; las curvas de nivel son líneas que unen puntos de igual altura obtenidos por **interpolación** entre celdas.
- Ambos métodos aplican la misma idea: elegir niveles, buscar cruces con *marching squares* y encadenar segmentos.
- **GDAL** (`gdal_contour -a ELEV -i 5 dem.tif curvas.gpkg`) es rápido, estándar y reproducible; ideal para producción.
- **Python** (rasterio + scikit-image + geopandas) ofrece control total, a cambio de más código y más cuidado con coordenadas y NoData.
- Un DEM real se puede obtener de portales gratuitos (OpenTopography, USGS EarthExplorer), de teselas públicas (Copernicus GLO-30), de organismos públicos o de un levantamiento propio; los DEM globales de 30 m limitan la equidistancia a 10 m o más.
- En VS Code conviene trabajar con un entorno de conda (conda-forge), elegir el intérprete correcto y ejecutar `gdal_contour` desde la terminal, un archivo de comandos, un script de Python o una tarea (*task*).
- Antes de contornear conviene revisar CRS, tamaño de celda, NoData, tipo de dato y si el modelo es MDT o MDS.
- Suaviza el **DEM** (no las líneas), elige una equidistancia coherente con la precisión vertical y valida siempre el resultado visualmente y con puntos de control.

---

## 13. Actividades

### 13.1 Preguntas de comprensión

1. Explica con tus palabras por qué las curvas no siguen los bordes de las celdas.
2. ¿Qué significa `-i 10 -off 5` en `gdal_contour`? ¿Qué cotas se generan?
3. ¿Por qué `find_contours` entrega coordenadas fraccionarias de (fila, columna)?
4. ¿Por qué se suma 0,5 al convertir a coordenadas geográficas en el script?
5. ¿Qué pasa si no declaras el valor NoData y tu DEM usa −9999?

### 13.2 Ejercicio de cálculo
En un cuadrado de cuatro celdas, los centros tienen alturas: arriba-izquierda 18 m, arriba-derecha 26 m, abajo-izquierda 14 m, abajo-derecha 22 m. Para el nivel de 20 m, calcula en qué fracción de cada lado cruza la curva e indica por qué lados pasa.

### 13.3 Práctico de laboratorio

Antes de empezar con tu zona, recorre el [notebook de laboratorio](laboratorio.ipynb), que ejecuta este flujo completo con un DEM de ejemplo.

1. Prepara en VS Code el entorno `geo` y la carpeta del proyecto (secciones 5.2 a 5.4) y comprueba que `gdal_contour --help` responde.
2. Descarga un DEM de tu zona con uno de los cuatro métodos de la sección 3.4 y revisa sus metadatos con `gdalinfo`.
3. Reproyecta a UTM y recorta con margen.
4. Genera curvas con `gdal_contour` a dos equidistancias distintas, una desde la terminal y otra con una tarea de VS Code.
5. Reproduce una de ellas con el script de Python.
6. Superpón ambos resultados en QGIS (o con matplotlib, sección 5.8) y describe las diferencias.
7. Suaviza el DEM con `sigma = 1` y `sigma = 2` y discute el equilibrio entre limpieza y pérdida de detalle.
8. Justifica la equidistancia elegida con la resolución y la precisión vertical del DEM (sección 3.6).
9. Entrega un mapa con curvas maestras etiquetadas, la fuente del DEM citada y un breve informe (una página) con tus decisiones.

---

## Glosario del subcapítulo

- **Transformación afín:** regla matemática que convierte coordenadas de celda (fila, columna) en coordenadas geográficas (x, y).
- **NoData:** valor reservado que indica "sin información" en una celda.
- **Marching squares:** algoritmo que recorre la grilla de a cuadrados de cuatro celdas para trazar curvas.
- **Máscara:** matriz de verdadero/falso que indica qué celdas son válidas.
- **Remuestreo:** cambio de resolución o de grilla de un ráster.
- **Simplificación:** reducción de vértices de una línea manteniendo su forma general.
- **COG (Cloud Optimized GeoTIFF):** GeoTIFF organizado para leer solo la parte necesaria desde un servidor remoto.
- **Tesela:** bloque rectangular de un producto cartográfico (por ejemplo, 1° × 1°) que se descarga por separado.
- **`/vsicurl/`:** prefijo de GDAL que permite leer archivos remotos por HTTP como si fueran locales.
- **Entorno de conda:** espacio aislado con versiones compatibles de Python y sus bibliotecas.
- **Falsa precisión:** curvas con detalle superior a la exactitud real del DEM.

---

## Recursos sugeridos

*(Verificar la versión vigente de cada herramienta antes de usarla en clases.)*

- Documentación oficial de GDAL: `gdal_contour`, `gdalinfo`, `gdalwarp`, `gdal_translate`, `gdaldem`.
- Documentación de rasterio: lectura de rásters, transformaciones afines y `fill`.
- Documentación de scikit-image: `skimage.measure.find_contours`.
- Documentación de geopandas y shapely: escritura de GeoPackage y `simplify`.
- Documentación del Copernicus DEM (manual del producto y licencia) y registro del conjunto de datos abierto en AWS (`copernicus-dem-30m`).
- OpenTopography y USGS EarthExplorer: guías de descarga de DEM globales.
- Documentación de VS Code: *Python environments*, *Integrated Terminal* y *Tasks*.
- Documentación de conda-forge para instalar GDAL.
- Validación de modelos de elevación digital en los Andes Centrales de Chile, *Revista Geográfica de Chile Terra Australis* (para discutir precisión vertical).
