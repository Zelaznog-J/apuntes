# Series de tiempo y detección de anomalías

!!! question "Pregunta guía"
    ¿Cómo evolucionó mi cultivo durante la campaña y cuándo algo salió de lo esperado?

> **Cómo leer este capítulo.** Pasamos de mapas de una fecha ([capítulo 6](06-procesamiento-raster.md)) a la película completa de la campaña. El hilo es: construir la serie, limpiarla, suavizarla, sacar fechas clave y buscar desvíos. El código de pandas y scipy se probó con el CSV de ejemplo ([`lote_reflectancias_v2.csv`](datos/lote_reflectancias_v2.csv)); el bloque de Earth Engine sigue la API oficial, pero no se ha ejecutado de punta a punta.

---

## Objetivos

Al terminar, podrás:

1. **Construir** la serie temporal de un índice por lote.
2. **Suavizarla** sin perder la señal agronómica.
3. **Estimar fechas clave** (emergencia, máximo, fin de ciclo).
4. **Generar alertas** cuando el cultivo se aleja de lo esperado.

---

## 1. La curva fenológica

Un cultivo anual sigue una forma típica: **suelo desnudo** → **ascenso** (implantación y crecimiento) → **meseta** (máximo desarrollo) → **descenso** (senescencia) → **caída abrupta** (cosecha).

La forma no es universal. En **praderas** y en **frutales o viñas**, la señal mezcla al cultivo con la vegetación de la entrefila (pasto, cobertura o suelo), lo que complica la lectura.

> **Un cuidado de lectura.** El satélite no ve la siembra: ve la **emergencia**, cuando el cultivo ya cubre algo de suelo. La fecha de siembra se estima restando a la emergencia los días típicos del cultivo, o se toma del registro del productor.

## 2. Construcción de la serie

- **En Earth Engine:** calcula el índice en cada imagen y reduce a un valor por lote (media o mediana) con `.map()`.
- **A tabla:** exporta y convierte a `DataFrame` de pandas.
- **Calidad:** guarda junto a cada valor el **porcentaje de píxeles válidos** ([capítulo 6](06-procesamiento-raster.md)). Dice cuánto confiar en ese punto.

```python
def punto(img):
    scl = img.select("SCL")
    valido = scl.eq(4).Or(scl.eq(5))                       # misma regla del [capítulo 6](06-procesamiento-raster.md)
    refl = img.select(["B4", "B8"]).divide(10000).updateMask(valido)
    ndvi = refl.normalizedDifference(["B8", "B4"]).rename("ndvi")
    media = ndvi.reduceRegion(ee.Reducer.mean(), lote, 10).get("ndvi")
    pct = valido.reduceRegion(ee.Reducer.mean(), lote, 20).get("SCL")   # fracción de píxeles válidos
    return ee.Feature(None, {"fecha": img.date().format("YYYY-MM-dd"),
                             "ndvi": media, "validos": pct})

filas = ee.FeatureCollection(coleccion.map(punto)).getInfo()["features"]
df = pd.DataFrame([f["properties"] for f in filas])
df["fecha"] = pd.to_datetime(df["fecha"])
```

## 3. Limpieza de la serie

- **Descartar** fechas con baja cobertura válida (por ejemplo, < 80 %).
- **Detectar caídas aisladas:** suelen ser nubes que la máscara no atrapó.
- **Regularizar** a una grilla de espaciado fijo (por ejemplo, cada 5 días) mediante interpolación.

> **Cuidado.** Interpolar rellena los huecos con una línea recta. Si falta un mes, la serie parecerá "normal" justo donde no hay información. Registra los tramos largos sin dato (por ejemplo, > 15 días) y trátalos como "sin información", no como "sin problema".

## 4. Suavizado

| Método | Características |
|---|---|
| **Media móvil** | Simple, pero desplaza y aplana los picos |
| **Savitzky–Golay** (`scipy.signal.savgol_filter`) | Ajusta polinomios locales; conserva mejor la forma y el máximo. Parámetros: largo de ventana (impar) y orden del polinomio |
| **Otras** | Ajuste doble logístico, filtro de Whittaker |

*Ejemplo de ventana:* con grilla de 5 días, `window_length=7` abarca 35 días. Una ventana mayor suaviza más y puede ocultar eventos cortos.

## 5. Métricas fenológicas

Desde la serie suavizada:

- **Emergencia o inicio:** primer cruce de un umbral (por ejemplo, 20 % de la amplitud entre la base y el máximo) o punto de máxima pendiente positiva.
- **Máximo:** fecha y valor.
- **Fin de ciclo o cosecha:** punto de máxima pendiente negativa o caída brusca.
- **Integral bajo la curva:** aproximación de la productividad acumulada.

## 6. Detección de anomalías

| Enfoque | Descripción | Requisito |
|---|---|---|
| **Umbral fijo** | El índice baja de un valor en una etapa dada | Conocer los valores esperados por etapa |
| **Comparación con referencia** | Desvío respecto de la media histórica del lote (puntaje z) o de lotes vecinos del mismo cultivo | El puntaje z requiere varias campañas previas (idealmente 5 o más); con una sola, usa lotes vecinos |
| **Cambio brusco** | Caída entre fechas consecutivas mayor a un umbral | Aplicar **solo entre la emergencia y el final de la meseta** |

> **Por qué la ventana de aplicación importa.** En la senescencia normal el NDVI cae de forma natural, y en la cosecha cae de golpe. Si aplicas la regla de "caída > 0,10" a toda la campaña, la senescencia genera alertas falsas. En el CSV de ejemplo, sin ventana saltan 3 alertas (1, 15 y 29 de diciembre, todas senescencia); con ventana, 0.

**Interpretación:** una anomalía es una **hipótesis** (estrés hídrico, plaga, granizo, falla de riego, anegamiento, helada) que se verifica en terreno, como se vio en el [capítulo 3](03-indices-vegetacion.md).

```python
import pandas as pd, numpy as np
from scipy.signal import savgol_filter

df = pd.read_csv("lote_reflectancias_v2.csv", parse_dates=["fecha"])
df["ndvi"] = (df["nir"] - df["red"]) / (df["nir"] + df["red"])
inv = df["nir"].le(0) | df["red"].le(0) | ~df["ndvi"].between(-1, 1)   # criterio del [capítulo 4](04-python.md)
limpio = df[~inv].set_index("fecha")["ndvi"]

# Regularizar y suavizar
serie = limpio.resample("5D").mean().interpolate()
suave = pd.Series(savgol_filter(serie, window_length=7, polyorder=2), index=serie.index)

# Fechas fenológicas
fecha_max, valor_max = suave.idxmax(), suave.max()
base = suave.iloc[:3].mean()
umbral = base + 0.2 * (valor_max - base)
emergencia = suave[(suave.index <= fecha_max) & (suave >= umbral)].index[0]
integral = np.trapezoid(suave.values, dx=5)       # unidades: NDVI × días (NumPy ≥ 2.0; en versiones previas, np.trapz)

# Alertas por caída brusca, solo entre emergencia y máximo, sobre la serie limpia (sin interpolar)
dif = limpio.diff()
ventana = (limpio.index >= emergencia) & (limpio.index <= fecha_max)
alertas = dif[ventana & (dif < -0.10)]
```

*Resultados con el CSV de ejemplo:* base ≈ 0,16; máximo ≈ 0,82 hacia el 10 de noviembre; emergencia (20 % de la amplitud) hacia fines de septiembre; sin alertas, porque el lote de ejemplo no tiene anomalía.

---

## Práctica guiada

1. **Obtener la serie** de NDVI de una campaña de tu lote (con el bloque de Earth Engine) o usar `lote_reflectancias_v2.csv`.
2. **Limpiar, regularizar y suavizar.** Compara media móvil y Savitzky–Golay en un mismo gráfico.
3. **Estimar** emergencia, máximo y fin de ciclo.
4. **Referencia histórica:** si tienes campañas anteriores, superpón la media con una banda de ±1 desvío estándar.
5. **Alertas:** programa una función que devuelva una tabla con las caídas bruscas y los NDVI bajo un umbral, aplicada solo a la ventana correcta.
6. **Prueba de sensibilidad:** introduce a mano una caída artificial (por ejemplo, −0,25 en una fecha de octubre) y verifica que tu función la detecte y que el suavizado no la borre.

## Producto esperado

Un gráfico de la campaña con las fechas fenológicas marcadas y una tabla de alertas con su interpretación preliminar.

## Errores frecuentes

- **Sobresuavizar** y borrar la anomalía que buscas.
- **Tomar huecos de nubes por cambios reales**, o interpolarlos como si fueran datos.
- **Aplicar la regla de caída brusca a toda la campaña** (senescencia y cosecha disparan falsas alertas).
- **Comparar campañas con distinta fecha de siembra** sin alinearlas (por ejemplo, por días desde la emergencia).

**Avance del proyecto:** identificar al menos una anomalía o hallazgo en tu lote. Es un insumo **obligatorio** del proyecto integrador.

## Ideas clave de cierre

1. La curva fenológica da la referencia para distinguir un cambio normal de una anomalía.
2. El suavizado es un compromiso: reduce ruido, pero en exceso oculta lo que buscas.
3. Las métricas fenológicas convierten la curva en fechas comparables entre campañas.
4. Las reglas de alerta se aplican en la etapa correcta del ciclo.
5. Una anomalía es una hipótesis: se verifica en terreno antes de decidir.
6. Estas métricas son las variables predictoras del [capítulo 8](08-machine-learning.md).
