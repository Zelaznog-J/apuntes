# Machine learning aplicado a la agronomía

!!! question "Pregunta guía"
    ¿Puede un algoritmo aprender a reconocer cultivos o estimar rendimientos a partir de imágenes?

> **Cómo leer este capítulo.** El machine learning (ML) se presenta como una herramienta más, con sus reglas y sus trampas. La trampa central es la **validación**: un modelo puede parecer excelente y fallar en un lote nuevo. Los ejemplos de código se ejecutaron con datos sintéticos incluidos en el libro ([`muestras_cultivos_v2.csv`](datos/muestras_cultivos_v2.csv), generado por [`generador_muestras.py`](datos/generador_muestras.py)).

---

## Objetivos

Al terminar, podrás:

1. **Explicar** los conceptos base del aprendizaje automático.
2. **Entrenar y validar** un clasificador Random Forest.
3. **Plantear** una regresión de rendimiento a partir de datos satelitales.

---

## 1. Conceptos base

- **Supervisado:** aprende de ejemplos con respuesta conocida. Incluye **clasificación** (qué cultivo es) y **regresión** (cuánto rinde).
- **No supervisado:** agrupa datos sin respuestas previas (por ejemplo, k‑means). Es la base de la zonificación del [capítulo 9](09-integracion.md).
- **Vocabulario:** variables predictoras (*features*), variable objetivo, conjunto de entrenamiento y de prueba, y **sobreajuste**: un modelo que memoriza lo que vio y no generaliza a datos nuevos.

## 2. Flujo de trabajo

**Pregunta** → **datos de referencia** (verdad de campo) → **variables** → **partición** → **entrenamiento** → **validación** → **predicción** → **interpretación**.

Es el mismo camino "del dato a la decisión" que se cierra en el [capítulo 9](09-integracion.md).

## 3. Datos de referencia (verdad de campo)

Fuentes habituales: relevamientos propios, registros de productores y, como último recurso, interpretación visual cuidadosa.

- **Calidad y balance de clases.** Una clase con muy pocos ejemplos produce un modelo poco confiable para esa clase.
- **Cantidad orientativa.** No hay un número mágico. Como guía: al menos 30–50 muestras por clase, y sobre todo **varios lotes distintos por clase** (muchos píxeles de un solo lote no cuentan como muestras independientes).

## 4. Variables predictoras

- **Bandas e índices** en varias **fechas clave** de la campaña. La dimensión temporal suele distinguir mejor los cultivos que una sola imagen.
- **Métricas fenológicas** del [capítulo 7](07-series-tiempo.md) (emergencia, máximo, fin de ciclo).
- **Estadísticas de la serie** (media, desvío, integral).

## 5. Random Forest

Es un conjunto (*ensemble*) de muchos árboles de decisión, cada uno entrenado con una submuestra distinta; el resultado es la "votación" de todos. En la práctica:

- Es **robusto** frente a variables ruidosas.
- Tiene **pocos hiperparámetros**: `n_estimators` (cantidad de árboles) y `max_depth` (profundidad).
- Entrega la **importancia de las variables**, que ayuda a interpretar qué fechas o índices pesan más.

## 6. Validación

- **Partición entrenamiento/prueba** y **validación cruzada** estiman qué tan bien generaliza el modelo.
- **Autocorrelación espacial: el punto más importante de la sesión.** Los píxeles de un mismo lote se parecen mucho. Si se reparten al azar entre entrenamiento y prueba, el modelo "reconoce el lote" en vez de aprender el cultivo, y la exactitud se **sobreestima**. **Solución:** separar por lote completo con `GroupKFold`, usando el identificador del lote como grupo.
- **Métricas de clasificación:** matriz de confusión, exactitud global, precisión, sensibilidad (*recall*) y F1 por clase.
- **Métricas de regresión:** R², RMSE y MAE.

### Demostración con los datos de ejemplo

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, KFold, cross_val_predict
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("muestras_cultivos_v2.csv")     # columnas: id_lote, cultivo, ndvi_oct, ndvi_nov, ndvi_ene
X, y, id_lote = df[["ndvi_oct", "ndvi_nov", "ndvi_ene"]], df["cultivo"], df["id_lote"]
rf = RandomForestClassifier(n_estimators=300, random_state=42)

# Validación "al azar": los píxeles de un lote caen en entrenamiento y en prueba
p_azar = cross_val_predict(rf, X, y, cv=KFold(5, shuffle=True, random_state=0))
# Validación por lote: cada lote entero queda fuera al evaluar
p_lote = cross_val_predict(rf, X, y, groups=id_lote, cv=GroupKFold(n_splits=5))

print("Exactitud al azar:", round(accuracy_score(y, p_azar), 3))     # 0.997
print("Exactitud por lote:", round(accuracy_score(y, p_lote), 3))    # 0.826
print(classification_report(y, p_lote))
```

**Resultado con estos datos:** 0,997 con validación al azar frente a **0,826 por lote**. La diferencia es el "premio" falso por reconocer lotes ya vistos. En el reporte por clase, el maíz se confunde más (sensibilidad ~0,70), un problema que la exactitud global esconde.

## 7. Estimación de rendimiento

Se plantea como una **regresión** entre índices en etapas críticas (o la integral de la serie) y el rendimiento de monitores de cosecha o registros históricos. También se valida por lote:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

rf_r = RandomForestRegressor(n_estimators=300, random_state=42)
pred = cross_val_predict(rf_r, X_rend, y_rend, groups=id_lote_rend, cv=GroupKFold(5))
print(r2_score(y_rend, pred), mean_squared_error(y_rend, pred) ** 0.5, mean_absolute_error(y_rend, pred))
```

**Limitaciones que debes comunicar:** pocos datos en la mayoría de los casos, el efecto del año climático sobre la relación índice–rendimiento y la necesidad de **calibración local**. Presenta siempre una **estimación con incertidumbre** (por ejemplo, "6,0 ± 0,5 t/ha"), nunca un dato exacto.

---

## Práctica guiada

1. **Cargar** [`muestras_cultivos_v2.csv`](datos/muestras_cultivos_v2.csv) (trigo, maíz, pradera, suelo desnudo; 10 lotes por clase, 40 píxeles por lote).
2. **Explorar:** grafica la curva media de NDVI de cada clase antes de entrenar.
3. **Entrenar** Random Forest y comparar validación al azar frente a validación por lote.
4. **Interpretar** la matriz de confusión, las métricas por clase y la importancia de variables.
5. **Mapa clasificado:** aplica el modelo a una imagen apilada (cada píxel es una fila con sus NDVI de las tres fechas). *Opcional:* clasificar directamente en Earth Engine con `ee.Classifier.smileRandomForest`.
6. **Demostración breve** de regresión de rendimiento con datos de muestra.

## Producto esperado

Un modelo entrenado con su reporte de métricas (por clase) y un mapa clasificado de la zona de estudio.

## Errores frecuentes

- **Validar con píxeles del mismo lote** repartidos entre entrenamiento y prueba.
- **Clases desbalanceadas** que distorsionan las métricas globales.
- **Confiar en la exactitud global** cuando una clase minoritaria falla: mira las métricas por clase.
- **Extrapolar el modelo** a otra región o campaña sin validarlo.
- **Contar píxeles como muestras independientes** cuando provienen de pocos lotes.

---

## Mirada hacia adelante: modelos fundacionales y *embeddings*

Hasta aquí construimos variables a mano (índices y fenología) y entrenamos un modelo para una tarea. Hay un enfoque complementario.

**Modelos fundacionales geoespaciales (GeoFM).** Modelos como **Prithvi** (NASA–IBM) o **Clay** se **preentrenan de forma autosupervisada** con enormes volúmenes de imágenes satelitales (por ejemplo, con autoencoders enmascarados sobre *Vision Transformers*). No aplican fórmulas fijas: aprenden representaciones espaciales y temporales.

- *Entradas típicas:* imágenes ópticas, radar, modelos de elevación y series temporales.
- *Tareas posibles (con ajuste fino):* estado del cultivo, humedad del suelo, detección de cambios y clasificación de cultivos.

**De píxeles a vectores (*embeddings*).** Un GeoFM convierte cada recorte de imagen (*chip*, por ejemplo 224 × 224 píxeles en Prithvi) en un **vector** de decenas a más de mil números que resume vegetación, texturas, agua y estructuras. Cada número por sí solo **no** significa "humedad" ni "suelo"; el significado se reparte entre todos y se aprovecha **comparando vectores entre sí**.

**Aplicaciones agronómicas:**

- **Búsqueda por similitud:** marcas un foco de estrés y buscas patrones parecidos en miles de hectáreas, sin entrenar un modelo nuevo.
- **Detección de anomalías:** una ruptura del ciclo estacional en los *embeddings* puede revelar cambios que un índice aislado no ve.

**Lo que no cambia:** para tareas agronómicas específicas estos modelos siguen necesitando **ajuste fino con datos etiquetados y validación en terreno**. Una anomalía en *embeddings* también puede deberse a nubes, cosecha, riego o cambio de cultivo: sigue siendo una hipótesis que se verifica en campo. Esta idea se retoma en "Recursos para continuar" del [capítulo 9](09-integracion.md).

## Ideas clave de cierre

1. El aprendizaje supervisado necesita datos de referencia de calidad; ningún algoritmo compensa una mala verdad de campo.
2. Random Forest es un buen punto de partida: robusto y con pocos hiperparámetros.
3. La autocorrelación espacial es la trampa más común: valida por lote, no por píxel.
4. La importancia de variables ayuda a interpretar el modelo; no lo uses como caja negra.
5. Toda estimación de rendimiento se comunica con su incertidumbre.
6. Los GeoFM y los *embeddings* amplían las herramientas, pero no reemplazan la validación en terreno.
