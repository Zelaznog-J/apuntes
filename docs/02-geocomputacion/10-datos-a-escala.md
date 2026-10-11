# Datos a escala: STAC, xarray y Dask

!!! question "Pregunta guía"
    ¿Cómo paso de un predio y una fecha a una región entera y 25 años de datos sin que el computador se quede sin memoria?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Buscar imágenes en catálogos STAC y cargarlas solo para el área y las fechas necesarias.
2. Trabajar con cubos de datos etiquetados en `xarray` y `rioxarray`.
3. Procesar por bloques con Dask y entender la evaluación diferida.
4. Agregar en el tiempo y en el espacio (climatologías, anomalías, estadísticas por zona).
5. Reconocer qué conceptos del capítulo 1 se mantienen al escalar.

## Esquema del capítulo

**1. Del archivo al catálogo**

- STAC: colecciones, ítems y activos.
- `odc.stac.load` y lectura parcial de COG.

**2. Cubos de datos con xarray**

- Dimensiones, coordenadas y `rioxarray`.
- Máscaras de calidad (SCL) con `.where()`.

**3. Dask**

- Bloques (*chunks*) y evaluación diferida.
- Cuándo conviene y cuándo no.

**4. Agregaciones**

- `groupby` temporal, `resample`, anomalías.
- Estadísticas zonales sobre cubos.

**5. Errores frecuentes**

- Cargar todo a memoria con `.values`.
- Mezclar CRS entre escenas.

## Ejemplo agronómico previsto

Calcular la anomalía de precipitación anual por región de Chile con ERA5 (2000–2025) y estimar el área quemada en Penco con dNBR de Sentinel-2.

!!! example "Caso aplicado"
    [Área quemada del incendio Penco–Lirquén](https://zelaznog-j.github.io/proyectos/incendio-penco/) · [Precipitación en Chile con ERA5](https://zelaznog-j.github.io/proyectos/precipitacion-era5/) · [Temperatura en Chile con ERA5](https://zelaznog-j.github.io/proyectos/temperatura-era5/)

## Material base

- Sección 11 del [capítulo 1](01-panorama.md).
- Proyectos del portafolio: incendio Penco–Lirquén (Sentinel-2) y precipitación y temperatura ERA5.
- Capítulos 5 a 7 de [Teledetección](../03-teledeteccion/index.md).

## Referencias

1. [xarray: guía de usuario](https://docs.xarray.dev/en/stable/user-guide/index.html).
2. [Dask: arreglos](https://docs.dask.org/en/stable/array.html).
3. [STAC](https://stacspec.org/).
4. [odc-stac](https://odc-stac.readthedocs.io/).
