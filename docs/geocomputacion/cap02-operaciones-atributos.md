# 2. Operaciones con datos de atributos

La pregunta central de este capítulo es: **¿qué valores tienen mis objetos y cómo puedo organizarlos o resumirlos?**

## Atributos y tablas

**Los atributos son la información no espacial asociada a los objetos geográficos.** Pueden ser nombres, población, superficie, rendimiento, elevación u otras variables descriptivas.

**Un `GeoDataFrame` puede manipularse como una tabla de pandas.** La diferencia esencial respecto de un `DataFrame` ordinario es que contiene una columna geométrica.

## Selección y filtrado

**La selección de filas y columnas se realiza con herramientas como `.loc`, `.iloc` y listas de columnas.** `.iloc` trabaja por posición y `.loc` por etiquetas o condiciones.

**Los filtros booleanos permiten seleccionar registros según condiciones.** Expresiones como `gdf[gdf["area"] < 10000]` generan subconjuntos basados en valores de atributos.

**Las condiciones pueden combinarse con operadores lógicos.** `&` representa AND, `|` representa OR y `~` representa NOT; `.isin()` resulta útil cuando se comparan varios valores posibles.

## Agregación

**La agregación resume muchas observaciones en grupos.** `groupby()` combinado con `sum()`, `mean()`, `count()` u otras funciones reduce los datos según una variable de agrupación.

**`.dissolve()` agrega atributos y geometrías simultáneamente.** Permite, por ejemplo, fusionar países por continente y calcular estadísticas agregadas para cada grupo.

## Uniones y nuevas variables

**Las uniones por atributos necesitan una clave común.** `pd.merge()` conecta tablas o capas utilizando columnas compartidas, como un identificador, código o nombre.

**Se pueden crear nuevas variables a partir de las existentes.** Por ejemplo, densidad de población = población / superficie, o cualquier cálculo derivado de otras columnas.

## Atributos en datos ráster

**Los valores de un ráster también pueden tratarse como atributos.** Mediante NumPy es posible seleccionar, modificar y resumir los valores de las celdas.

!!! note "Idea clave del capítulo"
    Aquí la pregunta central es **"¿qué valores tienen mis objetos y cómo puedo organizarlos o resumirlos?"**
