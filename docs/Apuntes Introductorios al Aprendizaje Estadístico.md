[← Volver al inicio](index.md)

# Introducción al Aprendizaje Estadístico (*Statistical Learning*)

El aprendizaje estadístico (*statistical learning*) abarca un conjunto amplio de herramientas y enfoques diseñados para dar sentido a conjuntos de datos complejos. Se ha consolidado como un subcampo de la estadística enfocado en el modelado y la predicción, tanto en escenarios supervisados como no supervisados.

---

## 1. El marco matemático básico

Supongamos que observamos una variable de respuesta cuantitativa $Y$ y un conjunto de $p$ predictores (variables independientes) $X = (X_1, X_2, \dots, X_p)$. Se asume que existe una relación entre $Y$ y $X$ que puede expresarse de forma general como:

$$Y = f(X) + \epsilon$$

*   **$f$:** Representa una función fija pero desconocida que contiene la información sistemática que $X$ aporta sobre $Y$. En esencia, el aprendizaje estadístico consiste en desarrollar enfoques para estimar $f$.
*   **$\epsilon$:** Es un término de error aleatorio, independiente de $X$ y con media cero.

---

## 2. ¿Por qué estimamos $f$?

Existen dos razones fundamentales para estimar esta función:

1.  **Predicción:** Cuando las entradas $X$ están disponibles pero la respuesta $Y$ no, buscamos predecir $Y$ mediante $\hat{Y} = \hat{f}(X)$. En este caso, $\hat{f}$ suele tratarse como una «caja negra», priorizando la precisión predictiva por encima de la forma exacta de la función. El error en este escenario se divide en dos componentes:
    *   **Error reducible:** Aquel que podemos minimizar eligiendo la técnica estadística más adecuada para estimar $f$.
    *   **Error irreducible:** La variabilidad asociada al término aleatorio $\epsilon$, el cual impone un límite superior de precisión que ninguna técnica puede eliminar.
2.  **Inferencia:** Cuando el objetivo es comprender la asociación entre $Y$ y los predictores. Aquí, $\hat{f}$ no puede ser una caja negra; necesitamos entender qué variables son importantes, la magnitud y dirección de su impacto, y si la relación es lineal o compleja.

Estimar la función desconocida $f$ a partir de los datos observados es el objetivo central de esta disciplina. A continuación, se detalla el procedimiento de estimación y la distinción entre enfoques paramétricos y no paramétricos.

---

## 3. ¿Cómo estimar $f$?

Para estimar $f$, partimos de un conjunto de $n$ observaciones de entrenamiento:

$$\{(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)\}$$

Donde cada $x_i = (x_{i1}, x_{i2}, \dots, x_{ip})^T$ es un vector de $p$ predictores e $y_i$ es la respuesta observada. El objetivo es aplicar un método estadístico para hallar una función estimada $\hat{f}$ tal que:

$$Y \approx \hat{f}(X)$$

para cualquier observación futura o no observada $(X, Y)$.

### Métodos Paramétricos
Se fundamentan en un enfoque de dos pasos:
1.  **Suposición de la forma funcional:** Se asume una estructura matemática previa para $f$. La más común es la linealidad: 
    $$f(X) = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_p X_p$$ 
    Esto reduce drásticamente el problema: en lugar de buscar una función arbitraria, el desafío se limita a estimar $p+1$ parámetros ($\beta_0, \beta_1, \dots, \beta_p$).
2.  **Ajuste del modelo:** Se emplean los datos de entrenamiento para estimar los coeficientes. El método tradicional es el de **Mínimos Cuadrados Ordinarios (OLS)**, que busca minimizar la suma de residuos al cuadrado (RSS):
    $$\text{RSS} = \sum_{i=1}^n \left( y_i - \hat{\beta}_0 - \sum_{j=1}^p \hat{\beta}_j x_{ij} \right)^2$$
    *(En contextos no lineales o de clasificación, se suele maximizar la verosimilitud).*

*   **Ventajas:** Fácil estimación debido al conjunto acotado de parámetros; alta interpretabilidad; y exigen tamaños de muestra más modestos.
*   **Desventajas:** Restricción fuerte (el modelo rara vez coincide con la verdadera $f$, generando sesgo si la aproximación es deficiente); y riesgo de **sobreajuste (*overfitting*)** si se añaden demasiados términos para ganar flexibilidad.

### Métodos No Paramétricos
No realizan suposiciones estrictas sobre la forma funcional de $f$. Buscan que $\hat{f}$ se ajuste estrechamente a los datos asegurando que la superficie resultante sea suave. Un ejemplo clásico es el algoritmo de **$K$ vecinos más cercanos (KNN)**:
*   Dado un punto $x_0$, identifica las $K$ observaciones de entrenamiento más cercanas ($\mathcal{N}_0$).
*   Estima $f(x_0)$ promediando las respuestas de dichos vecinos:
    $$\hat{f}(x_0) = \frac{1}{K} \sum_{x_i \in \mathcal{N}_0} y_i$$
*   *Otros ejemplos:* Los *splines*, que minimizan la distancia a los puntos sujeta a una penalización por curvatura.

*   **Ventajas:** Capacidad de adaptarse a una inmensa variedad de formas funcionales y capturar relaciones no lineales complejas sin sesgo de especificación previa.
*   **Desventajas:** Requieren volúmenes de datos mucho mayores; sufren la **maldición de la dimensionalidad** (con $p$ grande, las observaciones se dispersan y el error de prueba aumenta); y ofrecen una utilidad casi nula para la inferencia directa.

---

## 4. Equilibrio entre precisión e interpretabilidad

El equilibrio entre precisión predictiva e interpretabilidad (*trade-off*) es un principio rector del aprendizaje estadístico: a medida que aumenta la flexibilidad de un modelo, su interpretabilidad suele disminuir.

*   **Modelos de baja flexibilidad y alta interpretabilidad:** Regresión lineal, *Lasso* y selección de subconjuntos. Ideales cuando se requiere transparencia y análisis de coeficientes.
*   **Flexibilidad e interpretabilidad intermedias:** Modelos Aditivos Generalizados (GAMs) y árboles de decisión individuales.
*   **Alta flexibilidad y baja interpretabilidad («cajas negras»):** Métodos de ensamble (*Bagging*, *Boosting*, *Random Forests*), Máquinas de Soporte Vectorial (SVM) con núcleos no lineales y Redes Neuronales Profundas.

**¿Por qué no usar siempre el modelo más flexible?** 
Principalmente por dos razones: cuando el objetivo prioritario es la **inferencia** (explicar relaciones causa-efecto o significancia) y para evitar la **paradoja del sobreajuste**, donde modelos hipersensibles memorizan el ruido aleatorio de los datos de entrenamiento y pierden capacidad de generalización en datos nuevos.

---

## 5. Paradigmas Supervisado y No Supervisado

### Aprendizaje Supervisado
Para cada observación disponemos de predictores $X$ y una respuesta asociada $Y$. Su objetivo es predecir respuestas futuras o inferir la relación entre variables. Se divide en:
*   **Regresión:** Cuando $Y$ es cuantitativa continua (ej. predecir salarios).
*   **Clasificación:** Cuando $Y$ es cualitativa o categórica (ej. diagnóstico médico, detección de morosidad).

### Aprendizaje No Supervisado
Solo se dispone de las características de entrada $X$, sin una variable de respuesta $Y$ que guíe el entrenamiento. Su naturaleza es exploratoria e incluye:
*   **Análisis de conglomerados (*Clustering*):** Segmentación de observaciones en grupos homogéneos (ej. K-Means, Clustering Jerárquico).
*   **Reducción de dimensionalidad:** PCA (Análisis de Componentes Principales) para resumir alta dimensionalidad en espacios menores.
*   **Imputación de matrices:** Reconstrucción de valores faltantes (sistemas de recomendación).

*(Nota: Existe el **aprendizaje semisupervisado**, donde solo un subconjunto de los datos cuenta con etiquetas $Y$, útil cuando etiquetar resulta costoso o complejo).*

---

## 6. Evaluación de la Precisión del Modelo

Como no existe un único método universal (*no free lunch*), evaluar el desempeño es indispensable.

### Entorno de Regresión: Error Cuadrático Medio (MSE)
El estándar cuantitativo es el MSE:
$$\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{f}(x_i))^2$$
El **dilema sesgo-varianza** explica la curva en U del MSE de prueba en función de la flexibilidad:
$$\mathbb{E}(y_0 - \hat{f}(x_0))^2 = \text{Var}(\hat{f}(x_0)) + [\text{Bias}(\hat{f}(x_0))]^2 + \text{Var}(\epsilon)$$

### Entorno de Clasificación
Se evalúa mediante la **tasa de error** y métricas derivadas:
$$\text{Tasa de error} = \frac{1}{n} \sum_{i=1}^n I(y_i \neq \hat{y}_i)$$
Apoyándose en herramientas como la matriz de confusión, sensibilidad, especificidad, curvas ROC y el área bajo la curva (AUC).

### Estimación del error de prueba en la práctica:
1.  **Ajustes analíticos:** Criterios teóricos que penalizan la complejidad (AIC, BIC, $C_p$ de Mallows, $R^2$ ajustado).
2.  **Métodos de remuestreo:** Validación cruzada y conjuntos de validación.

---

## 7. Validación Cruzada (*Cross-Validation*)

Su propósito es estimar el error de prueba utilizando únicamente los datos de entrenamiento disponibles, sirviendo tanto para evaluar modelos como para seleccionar hiperparámetros.

*   **Enfoque del conjunto de validación:** Divide los datos en entrenamiento y validación de forma aleatoria. Presenta alta variabilidad y puede sobreestimar el error al entrenar con una fracción reducida de los datos.
*   **LOOCV (*Leave-One-Out Cross-Validation*):** Utiliza una sola observación para validar y las $n-1$ restantes para entrenar, repitiendo el proceso $n$ veces:
    $$\text{CV}_{(n)} = \frac{1}{n} \sum_{i=1}^n \left( \frac{y_i - \hat{y}_i}{1 - h_i} \right)^2$$
    *(Presenta un sesgo casi nulo, pero una alta varianza computacional).*
*   **Validación cruzada en $K$ pliegues ($k$-Fold CV):** Divide los datos en $k$ grupos (típicamente $5$ o $10$):
    $$\text{CV}_{(k)} = \frac{1}{k} \sum_{i=1}^k \text{MSE}_i$$
    Ofrece el mejor compromiso empírico al equilibrar adecuadamente el sesgo y la varianza en comparación con LOOCV. En clasificación, el MSE se reemplaza por la proporción de elementos mal clasificados.

---

## Paradigmas del Aprendizaje Estadístico

![Infografía de los paradigmas de aprendizaje estadístico: supervisado, no supervisado y semisupervisado](paradigmas-aprendizaje-estadistico.png)
																								*Fuente: Elaboración propia (2026).*

---

## Referencia bibliográfica

James, G., Witten, D., Hastie, T., Tibshirani, R. y Taylor, J. (2023). *An Introduction to Statistical Learning: With Applications in Python*. Springer. [https://www.statlearning.com/](https://www.statlearning.com/)