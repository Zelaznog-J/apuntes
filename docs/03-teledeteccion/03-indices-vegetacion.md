# Índices de vegetación y su interpretación agronómica

!!! question "Pregunta guía"
    ¿Cómo convierto reflectancias en información sobre el cultivo?

> **Cómo leer este capítulo.** Cada índice se explica primero con su idea, luego con su fórmula y sus bandas de Sentinel‑2. Todos los ejemplos numéricos son ilustrativos y están calculados paso a paso para que los repliques en una planilla.

---

## Objetivos

Al terminar, podrás:

1. **Calcular** los principales índices a partir de las bandas de Sentinel‑2.
2. **Interpretar** cada índice en relación con biomasa, vigor, nitrógeno y estado hídrico.
3. **Reconocer** cuándo un índice deja de ser confiable y qué hacer en ese caso.

---

## 1. La lógica de un índice normalizado

**En simple:** comparar dos colores en que la vegetación se comporta muy distinto y expresar esa diferencia como un número fácil de comparar.

$$\text{Índice} = \frac{\text{Banda A} - \text{Banda B}}{\text{Banda A} + \text{Banda B}}$$

El resultado queda siempre entre −1 y +1. Se apoya en tres ideas:

- **Dos bandas con comportamiento distinto.** La vegetación absorbe el rojo (clorofila) y refleja mucho el NIR (estructura del mesófilo). El suelo y el agua no muestran ese contraste.
- **La diferencia mide el contraste.** Más vegetación activa, mayor distancia entre NIR y rojo.
- **La suma normaliza.** Dividir por la suma reduce el efecto de la iluminación y permite comparar fechas y zonas.

### Por qué normalizar: el mismo cultivo con dos niveles de luz

Valores ilustrativos. Con media iluminación, **ambas bandas** bajan a la mitad:

| Condición | NIR | Rojo | NIR − Rojo | NDVI |
|---|---|---|---|---|
| Pleno sol | 0,50 | 0,05 | 0,45 | 0,45 / 0,55 = **0,82** |
| Media iluminación | 0,25 | 0,025 | 0,225 | 0,225 / 0,275 = **0,82** |

La resta simple cae a la mitad; el índice no cambia.

**Matiz:** la normalización reduce los efectos de la iluminación, pero **no elimina** los de la atmósfera (vapor de agua, aerosoles) ni los de la geometría de observación (ángulo del sol y del sensor). Por eso se usa reflectancia de superficie (L2A).

---

## 2. Índices principales con Sentinel‑2

Todas las fórmulas usan **reflectancia de 0 a 1** (el valor del producto dividido por 10.000).

| Índice | Fórmula | Bandas S2 | Para qué sirve |
|---|---|---|---|
| **NDVI** | (NIR − R) / (NIR + R) | (B8 − B4) / (B8 + B4) | Vigor y cobertura general |
| **NDRE** | (NIR − RE) / (NIR + RE) | (B8A − B5) / (B8A + B5)* | Clorofila y nitrógeno en canopias densas |
| **GNDVI** | (NIR − G) / (NIR + G) | (B8 − B3) / (B8 + B3) | Clorofila en etapas intermedias |
| **SAVI** | (NIR − R)(1 + L) / (NIR + R + L) | B8 y B4; L = 0,5 | Baja cobertura y suelo expuesto |
| **EVI** | 2,5 (NIR − R) / (NIR + 6R − 7,5B + 1) | B8, B4 y B2 (azul) | Canopias densas (satura menos) y corrección de aerosoles |
| **NDMI** (= NDWI de Gao) | (NIR − SWIR) / (NIR + SWIR) | (B8A − B11) / (B8A + B11)* | Agua en la vegetación |
| **NDWI de McFeeters** | (G − NIR) / (G + NIR) | (B3 − B8) / (B3 + B8) | Agua libre: anegamientos, tranques |

\* Existen variantes con B8 en lugar de B8A u otras bandas de borde rojo. Lo importante es **documentar cuál usaste**. En este libro se usa B8A con B5 para NDRE y B8A con B11 para NDMI, porque son bandas de 20 m que calzan entre sí.

### NDVI y SAVI: vigor y cobertura

**NDVI — (B8 − B4) / (B8 + B4)**
- *Qué resume:* el contraste rojo–NIR, ligado a la vegetación verde activa.
- *Cuándo usarlo:* seguimiento general; es el más usado y el más comparable en la literatura.
- *Cuidado:* satura en canopias densas y se ve afectado por el suelo cuando la cobertura es baja.

**SAVI — (NIR − R)(1 + L) / (NIR + R + L)**
- *Qué agrega:* el factor L atenúa el brillo y color del suelo.
- *Cuándo usarlo:* cultivos recién emergidos, frutales jóvenes o baja cobertura.
- *Sobre L:* con L = 0 el SAVI es igual al NDVI; L = 0,5 es el valor típico.

### NDRE y GNDVI: clorofila y nitrógeno

**NDRE — (B8A − B5) / (B8A + B5)**
- *Qué aprovecha:* el borde rojo (B5, ~705 nm), donde la reflectancia sube bruscamente y se desplaza con el contenido de clorofila.
- *Cuándo usarlo:* canopias densas y seguimiento de nitrógeno, donde el NDVI ya saturó.
- *Resolución:* B5 y B8A son de 20 m; el NDVI con B8 y B4 es de 10 m.

**GNDVI — (B8 − B3) / (B8 + B3)**
- *Qué aprovecha:* la banda verde: la hoja refleja más verde cuando baja su clorofila.
- *Cuándo usarlo:* clorofila en etapas intermedias.
- *Ventaja:* mantiene los 10 m nativos.

### EVI: cuando hay mucha biomasa

**EVI — 2,5 (B8 − B4) / (B8 + 6·B4 − 7,5·B2 + 1)**
- *Qué agrega:* usa el azul (B2) para corregir aerosoles y sigue respondiendo cuando el NDVI ya se aplanó.
- *Cuidado:* requiere reflectancia entre 0 y 1; con valores sin escalar, el "+1" del denominador pierde sentido.

### Un nombre, dos índices: el caso NDWI

| | NDWI de Gao (= NDMI) | NDWI de McFeeters |
|---|---|---|
| **Mide** | Agua dentro de la vegetación | Agua libre en superficie |
| **Fórmula** | (B8A − B11) / (B8A + B11) | (B3 − B8) / (B3 + B8) |
| **Lógica** | El SWIR lo absorbe el agua foliar: más valor, más agua en la hoja | Verde frente a NIR: resalta anegamientos, tranques y canales |

**Regla práctica:** si escribes "NDWI", escribe también la fórmula y las bandas. El nombre solo es ambiguo.

---

## 3. Valores de referencia del NDVI

| Situación | NDVI aproximado |
|---|---|
| Agua | < 0 |
| Suelo desnudo | ~0,1 – 0,2 |
| Cultivo en implantación | ~0,2 – 0,4 |
| Cobertura intermedia o con estrés | ~0,4 – 0,6 |
| Cultivo en pleno desarrollo | ~0,6 – 0,9 |

Son **rangos orientativos**, no umbrales universales: cambian con el cultivo, el suelo y el sensor. Sirven para orientarse, no para decidir con un único valor.

---

## 4. Cálculo paso a paso

Reflectancias ilustrativas de cuatro tipos de píxel. Para simplificar se usa el mismo NIR en NDVI (B8) y en NDRE (B8A):

| Píxel | Rojo (B4) | Borde rojo (B5) | NIR | NDVI | NDRE |
|---|---|---|---|---|---|
| Cultivo sano | 0,04 | 0,12 | 0,45 | **0,84** | **0,58** |
| Cultivo estresado | 0,10 | 0,18 | 0,30 | 0,50 | 0,25 |
| Suelo | 0,20 | 0,23 | 0,27 | 0,15 | 0,08 |
| Agua | 0,03 | 0,025 | 0,01 | −0,50 | −0,43 |

**Cultivo sano, paso a paso:**
- NDVI = (0,45 − 0,04) / (0,45 + 0,04) = 0,41 / 0,49 = **0,84**
- NDRE = (0,45 − 0,12) / (0,45 + 0,12) = 0,33 / 0,57 = **0,58**

**EVI del cultivo sano** (con azul B2 = 0,02):
- EVI = 2,5 × 0,41 / (0,45 + 6 × 0,04 − 7,5 × 0,02 + 1) = 1,025 / 1,54 = **0,67**

Replica la tabla en una planilla y responde: ¿por qué el agua da valores negativos? ¿Por qué el suelo queda tan por debajo del cultivo sano?

---

## 5. Del índice a la variable agronómica

### Biomasa, área foliar (IAF) y saturación

- **Relación positiva pero no lineal:** más biomasa sube el índice, cada vez con menos fuerza.
- **Saturación sobre IAF ~3:** el NDVI deja de distinguir un cultivo bueno de uno muy bueno. El NDRE y el EVI mantienen sensibilidad en canopias más densas.

### Vigor y nitrógeno: compara en relativo

- **Dentro del lote** importa más la comparación *relativa* (por ejemplo, zonas sobre y bajo la mediana) que el valor absoluto. Con el mismo cultivo, suelo, fecha y sensor, las diferencias apuntan a manejo o ambiente.
- **Índice de suficiencia de nitrógeno:** los índices de borde rojo son más sensibles al nitrógeno que el NDVI. Se comparan con una **franja de referencia bien fertilizada**:

$$IS = \frac{\text{NDRE de la zona}}{\text{NDRE de la franja de referencia}}$$

Ejemplo: 0,52 / 0,58 = **0,90**. La zona alcanza el 90 % de la referencia: posible deficiencia de nitrógeno **a verificar en campo**.

### Estrés hídrico: quién avisa primero

1. Comienza el déficit de agua en el suelo.
2. Baja el agua en la hoja: **responden primero los índices con SWIR**, como el NDMI.
3. El estrés se prolonga y la planta pierde turgencia.
4. Aparece daño estructural en el follaje y **recién entonces cae el NDVI**.

**Conclusión:** el NDVI suele reaccionar tarde. Para alertas tempranas de estrés hídrico conviene seguir el NDMI (aunque su respuesta también depende del cultivo y de la etapa).

---

## 6. Cuándo un índice deja de ser confiable

| Situación | Efecto | Qué hacer |
|---|---|---|
| **Suelo desnudo** | Con baja cobertura, el color del suelo altera el valor | Usar SAVI |
| **Nubes, sombras y bruma** | Bajan los valores y simulan estrés | Enmascarar y revisar el color natural |
| **Saturación** | El NDVI pierde sensibilidad sobre IAF ~3 | Usar NDRE o EVI |
| **Malezas** | Suben el índice sin reflejar al cultivo | Contrastar con la fenología esperada y recorrer el lote |

**Correlación no es causa.** Un NDVI bajo dice "algo pasa", no "qué pasa". Orienta el muestreo de campo; no lo reemplaza.

---

## 7. Práctica guiada

1. **Planilla.** Calcula NDVI y NDRE de la tabla de la sección 4.
2. **Dos lotes.** En EO Browser o Copernicus Browser, observa el NDVI de dos lotes con manejo distinto (riego frente a secano, o distinta fecha de siembra).
3. **Paleta de interpretación.** Define criterios de lectura de colores y valores, y anota qué hipótesis de campo surgen de las diferencias.
4. **Detective.** Analiza imágenes con "trampas" y encuentra la causa del valor anómalo.

### Detective: tres trampas frecuentes

| Trampa | Qué se ve | Pista | Cómo confirmarla |
|---|---|---|---|
| **Nube fina** | NDVI bajo y difuso que cruza varios lotes | Velo blanquecino en color natural | Comparar con la fecha anterior y la siguiente |
| **Lote recién cosechado** | Caída brusca en todo el lote, con bordes rectos | Rastrojo o suelo visible; la fecha calza con la cosecha | Consultar los registros del productor |
| **Malezas** | NDVI alto en manchones irregulares o fuera de época | El "verdor" no calza con la fenología | Recorrida a campo |

## 8. Errores frecuentes

| Error | Cómo evitarlo |
|---|---|
| Usar umbrales absolutos universales | Comparar en relativo o contra una franja de referencia |
| Comparar sensores distintos sin armonizar | Armonizar (por ejemplo con productos HLS) o quedarse en un solo sensor |
| Escribir "NDWI" sin la fórmula | Aclarar si es Gao (agua foliar) o McFeeters (agua libre) |
| No documentar la variante de bandas | Indicar si el NDRE o el NDMI usan B8 o B8A |

## Producto esperado

Tabla con NDVI y NDRE de los cuatro píxeles de muestra y una comparación argumentada entre dos lotes con manejo distinto, apoyada en hipótesis de campo.

### Discusión de casos

Para cada diferencia observada, responde:
- ¿Qué hipótesis de campo la explicaría?
- ¿Qué otras causas habría que descartar?
- ¿Qué dato de campo la confirmaría?

**Avance del proyecto:** calcula NDVI y NDRE en tu lote y anota al menos una hipótesis para verificar en terreno.

---

## 9. Ideas clave de cierre

1. Un índice normalizado resume el contraste entre dos bandas y reduce los efectos de la iluminación.
2. Cada índice tiene un uso: NDVI para vigor general, NDRE y EVI para canopias densas, SAVI para baja cobertura, NDMI para agua foliar.
3. "NDWI" nombra dos índices: escribe siempre la fórmula.
4. Los valores de referencia orientan; la comparación relativa informa más.
5. Un índice indica, no diagnostica.

## Referencias

- Rouse, J. W. et al. (1974). *Monitoring vegetation systems in the Great Plains with ERTS*. NASA SP‑351. (NDVI)
- Huete, A. R. (1988). A soil‑adjusted vegetation index (SAVI). *Remote Sensing of Environment*, 25.
- Huete, A. et al. (2002). Overview of the radiometric and biophysical performance of the MODIS vegetation indices. *Remote Sensing of Environment*, 83. (EVI)
- Gitelson, A. et al. (1996). Use of a green channel in remote sensing of global vegetation. *Remote Sensing of Environment*, 58. (GNDVI)
- Gao, B.‑C. (1996). NDWI: a normalized difference water index for remote sensing of vegetation liquid water. *Remote Sensing of Environment*, 58.
- McFeeters, S. K. (1996). The use of the NDWI in the delineation of open water features. *International Journal of Remote Sensing*, 17.
- Barnes, E. M. et al. (2000). Coincident detection of crop water stress, nitrogen status and canopy density. *Proc. 5th Int. Conf. on Precision Agriculture*. (NDRE)

*Tablas y valores: elaboración propia, con datos ilustrativos.*
