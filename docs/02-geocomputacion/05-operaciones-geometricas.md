# Operaciones geométricas

!!! question "Pregunta guía"
    ¿Cómo creo franjas de protección, simplifico deslindes o cambio la resolución de un ráster sin distorsionar el resultado?

!!! warning "Capítulo en preparación"
    Esta página muestra el esquema del capítulo: qué preguntas responderá, qué secciones tendrá y de qué material se escribirá. Mientras tanto, el [panorama (capítulo 1)](01-panorama.md) cubre lo esencial del tema.

## Objetivos

Al terminar, podrás:

1. Simplificar geometrías y reconocer cuándo se pierde topología.
2. Calcular centroides, puntos representativos y buffers en metros.
3. Aplicar transformaciones afines (desplazar, escalar, rotar).
4. Recortar, unir y disolver geometrías.
5. Remuestrear y alinear rásteres eligiendo el método según la variable.

## Esquema del capítulo

**1. Operaciones geométricas con vectores**

- Simplificación (`simplify`, preservar topología).
- Centroides frente a `representative_point`.
- Buffers positivos y negativos.
- Transformaciones afines.
- Recorte, unión y conversión entre tipos de geometría.

**2. Operaciones geométricas con rásteres**

- Intersecciones geométricas.
- Extensión y origen.
- Agregación y desagregación.
- Remuestreo: vecino más cercano, bilineal, promedio, moda.

**3. Errores frecuentes**

- Buffers en grados.
- Remuestrear clases con interpolación bilineal.

## Ejemplo agronómico previsto

Trazar una franja de 10 m junto a un curso de agua, descontarla de la superficie cultivable y llevar un DEM de 30 m a la grilla de 10 m de Sentinel-2.

## Material base

- Capítulo 4 de *Geocomputation with Python* (no está en los PDF del curso).
- Secciones 4.4 y 4.5 del [capítulo 1](01-panorama.md).

## Referencias

1. Lovelace, R., Nowosad, J. y Muenchow, J. *Geocomputation with Python*. Libro abierto: [py.geocompx.org](https://py.geocompx.org/). Capítulo 5.
2. [Shapely: manual de usuario](https://shapely.readthedocs.io/en/stable/manual.html).
3. [Rasterio: documentación](https://rasterio.readthedocs.io/en/stable/).
