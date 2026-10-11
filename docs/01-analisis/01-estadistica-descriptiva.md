# Estadística descriptiva

!!! abstract "Objetivos"
    - Distinguir medidas de tendencia central y de dispersión.
    - Calcularlas e interpretarlas sobre una variable climática.

## Conceptos

La **media** de \(n\) observaciones \(x_1, \dots, x_n\) es

\[
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
\]

y la **desviación estándar muestral**

\[
s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2}
\]

## Ejemplo

```python
import numpy as np

precipitacion = np.array([12.0, 0.0, 3.5, 40.2, 8.1])
precipitacion.mean(), precipitacion.std(ddof=1)
```

## Ejercicios

1. ¿Por qué la mediana describe mejor la precipitación diaria que la media?

## Referencias

- Wilks, D. S. (2019). *Statistical Methods in the Atmospheric Sciences*. Elsevier.
