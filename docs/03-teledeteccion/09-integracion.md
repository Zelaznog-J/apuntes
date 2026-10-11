# Integración y mapas de manejo sitio‑específico

!!! question "Pregunta guía"
    ¿Qué decisión concreta tomo con todo esto?

> **Cómo leer este capítulo.** Cierra el recorrido con zonas de manejo, dosis variable y comunicación de resultados, y termina con una pauta para presentar y evaluar el proyecto integrador. El código de zonificación se probó con datos sintéticos.

---

## Objetivos

Al terminar, podrás:

1. **Delimitar** zonas de manejo dentro de un lote.
2. **Traducir** esas zonas en una prescripción de dosis variable.
3. **Comunicar** resultados a productores y equipos técnicos.
4. **Presentar y evaluar** el proyecto integrador.

---

## 1. Zonas de manejo

Son áreas del lote con comportamiento productivo **relativamente homogéneo y estable en el tiempo**: no se definen por una sola campaña, sino por un patrón que se repite.

### Insumos posibles

- **NDVI de varias campañas** (idealmente tres o más), normalizado por fecha: por ejemplo, cada valor dividido por la media del lote en esa fecha, para poder comparar campañas.
- **Mapas de rendimiento** de monitores de cosecha.
- **Conductividad eléctrica aparente** del suelo.
- **Topografía** (pendiente y posición en el relieve).
- **Muestreos de suelo**.

### Método

Se aplica **k‑means** (o su variante difusa, *fuzzy c‑means*) a las capas de insumo, **estandarizadas** para que ninguna domine solo por su escala. El número de zonas se decide con criterio práctico: **2 a 4** es lo manejable con la maquinaria habitual.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy import ndimage

# pila: arreglo (alto, ancho, n_capas) con NDVI normalizado de 3 campañas + otras capas
valido = np.isfinite(pila).all(axis=-1)
X = StandardScaler().fit_transform(pila[valido])              # estandarizar
km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)

zonas = np.full(valido.shape, -1)
zonas[valido] = km.labels_

# Numerar las zonas de menor a mayor NDVI (para que "zona 0" sea siempre la de menor vigor)
orden = np.argsort([pila[..., 0][zonas == k].mean() for k in range(3)])
zonas = np.vectorize({k: i for i, k in enumerate(orden)}.get)(zonas)

# Filtro de mayoría 5×5 para eliminar píxeles sueltos
moda = lambda v: np.bincount(v.astype(int)).argmax()
zonas_filtradas = ndimage.generic_filter(zonas, moda, size=5, mode="nearest")
```

### Posprocesamiento

- **Filtro de mayoría:** elimina píxeles aislados que no forman una zona coherente.
- **Superficie mínima por zona:** compatible con el ancho de labor de la maquinaria.

### Validación

Una zonificación es válida si **reduce la varianza** del rendimiento o de las propiedades del suelo dentro de cada zona, frente a tratar el lote como una unidad, y si se **confirma con muestreo dirigido** en terreno.

## 2. Mapas de aplicación variable (VRA)

- **De zona a dosis.** Se define un criterio agronómico por zona. Por ejemplo, más nitrógeno donde el potencial es alto y el agua no limita, o la estrategia inversa para nivelar las zonas bajas, según el objetivo del productor.
- **Formato.** Polígonos con un atributo de dosis, en shapefile, ajustados al ancho de labor. **Verifica con el proveedor** el formato que acepta el monitor de la maquinaria.
- **Franjas de validación.** Deja franjas con dosis uniforme dentro del lote para medir el resultado real de la dosis variable.

## 3. De los datos a la decisión

El recorrido completo del libro:

**imagen → índice → serie temporal → anomalía o zona → recorrida de campo → decisión → verificación**

Qué **puede** afirmar un análisis satelital: dónde mirar, qué zonas se comportan distinto, cuándo cambió el patrón. Qué **no puede**: la causa por sí solo ni el criterio agronómico. Orienta la decisión; no reemplaza la verificación en terreno.

## 4. Comunicar resultados a productores

- **Empieza por la conclusión y la recomendación**, no por el método.
- **Mapas simples**, con leyenda, escala, norte, fecha y fuente.
- **Pocas clases y colores intuitivos**; valores relativos ("sobre o bajo la mediana del lote") antes que absolutos.
- **Explicita la incertidumbre y los supuestos** (como en el [capítulo 8](08-machine-learning.md)).
- **Propón una acción concreta** y cómo se verificará.

---

## Estructura sugerida para presentar el proyecto (10 minutos)

| Min | Contenido |
|---|---|
| 1 | Lote y pregunta agronómica |
| 2 | Datos y método, resumidos |
| 2 | Mapas de índice y serie temporal |
| 2 | Anomalía o hallazgo e interpretación |
| 2 | Zonificación o recomendación |
| 1 | Limitaciones y próximos pasos |

## Pauta de autoevaluación del proyecto integrador

| Criterio | Peso |
|---|---|
| Adquisición y procesamiento correcto de imágenes (máscaras, índices) | 20 % |
| Serie temporal y detección de la anomalía o hallazgo | 20 % |
| Calidad de la interpretación agronómica y de la recomendación | 25 % |
| Reproducibilidad y documentación del notebook | 20 % |
| Claridad de la presentación y de los mapas | 15 % |
| **Total** | **100 %** |

## Recursos para continuar

- **Radar Sentinel‑1** (y, desde 2025, datos abiertos de **NISAR**), para zonas con muchas nubes.
- **Datos meteorológicos y de evapotranspiración**, para sumar contexto climático.
- **Drones**, para el detalle dentro del lote.
- **Modelos de cultivo**, que combinan clima, suelo y manejo.
- **Modelos fundacionales geoespaciales y *embeddings*** (Prithvi, Clay), presentados en el [capítulo 8](08-machine-learning.md): útiles para buscar zonas parecidas y detectar anomalías, siempre con ajuste fino y validación en terreno.
- **Automatización de reportes periódicos por lote**, como paso natural de escalamiento.

---

## Ideas clave de cierre

1. Las zonas de manejo se definen por estabilidad en el tiempo, no por una sola campaña.
2. Una zonificación sirve si es operativa: 2 a 4 zonas, con superficie compatible con la maquinaria real.
3. Todo el recorrido cabe en un esquema: imagen → índice → serie → anomalía o zona → campo → decisión → verificación.
4. Comunicar a productores es priorizar la recomendación sobre el método y ser claro con la incertidumbre.
5. El proyecto integrador reúne en un solo flujo lo aprendido, desde el acceso a datos ([capítulo 5](05-acceso-imagenes.md)) hasta el machine learning ([capítulo 8](08-machine-learning.md)).
