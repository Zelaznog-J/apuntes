# 6. Sistemas de referencia y reproyección de datos geográficos

El CRS no es un detalle de metadatos: determina **qué significan las coordenadas y qué operaciones espaciales son válidas**.

## Qué es un CRS

**Un sistema de referencia de coordenadas (CRS/SRC) define cómo deben interpretarse las coordenadas.** Los dos grandes grupos son los CRS geográficos, normalmente expresados en grados, y los proyectados, normalmente en unidades lineales.

**Los identificadores `AUTHORITY:CODE`, como `EPSG:4326`, son la forma práctica de referirse a muchos CRS.** Internamente, definiciones más completas como WKT describen datum, elipsoide, ejes, unidades y otros componentes.

## Asignar y reproyectar

**Consultar y asignar un CRS no es lo mismo que reproyectar.** `.set_crs()` establece o corrige la definición del CRS, pero no modifica las coordenadas de las geometrías.

**Reproyectar significa transformar las coordenadas de un CRS a otro.** En datos vectoriales se utiliza habitualmente `.to_crs()`.

## Precauciones al analizar

**Las operaciones geométricas de GeoPandas/Shapely son esencialmente planas.** Por ello, distancias, áreas y buffers deben calcularse preferentemente en un CRS proyectado apropiado.

**Dos capas deben compartir un CRS compatible antes de compararse espacialmente.** Un desajuste puede generar advertencias y resultados numéricamente válidos pero geográficamente absurdos.

## Elegir una proyección

**No existe una proyección perfecta para todos los objetivos.** Toda proyección introduce algún tipo de distorsión; la elección debe responder a la tarea concreta.

**WGS84 (`EPSG:4326`) es especialmente común para GPS, intercambio de datos y cartografía web.** Sin embargo, no es apropiado para todos los cálculos métricos.

## Reproyección de rásteres

**Los rásteres también pueden reproyectarse, pero requieren remuestreo.** Al cambiar la cuadrícula se deben estimar nuevos valores de píxel; métodos como vecino más cercano o bilinear se eligen según el tipo de variable.

## Proyecciones personalizadas

**También pueden utilizarse proyecciones personalizadas.** Definiciones WKT o cadenas PROJ permiten adaptar un CRS a necesidades particulares de análisis o visualización.

!!! note "Idea clave del capítulo"
    El CRS no es un detalle de metadatos; determina **qué significan las coordenadas y qué operaciones espaciales son válidas**.
