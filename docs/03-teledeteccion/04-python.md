# Introducción a Python para datos geoespaciales

!!! question "Pregunta guía"
    ¿Por qué programar si puedo ver las imágenes en el navegador?

> **Cómo leer este capítulo.** Es tu primer contacto con la programación y no se asume experiencia previa. Cada idea se introduce con un ejemplo agronómico corto. El [notebook guía](04-python-notebook.ipynb) que acompaña este capítulo trae todo el código listo para ejecutar y modificar.

---

## Objetivos

Al terminar, podrás:

1. **Moverte** con soltura en Google Colab.
2. **Entender** las estructuras básicas de Python: variables, tipos, listas y diccionarios.
3. **Usar** numpy, pandas y matplotlib para leer, procesar y graficar datos de un lote.

---

## 0. Motivación: ¿para qué programar?

Si ya puedes ver el NDVI en Copernicus Browser, ¿por qué escribir código? Por tres razones:

- **Automatización.** Repetir un análisis en decenas de lotes o fechas, a mano, no es viable. Con código se escribe una vez y se reutiliza.
- **Reproducibilidad.** Un notebook deja registrado qué datos y parámetros usaste. Un clic en una interfaz no deja registro.
- **Escala.** Un visor muestra una imagen a la vez. Analizar una campaña completa, varios lotes o varias temporadas requiere un programa.

Estas razones conectan con los capítulos 5 a 9, que se apoyan en lo que aprendes aquí.

## 1. El entorno: Google Colab

**Google Colab** es un cuaderno (*notebook*) de Python que funciona en el navegador, es gratuito y no requiere instalar nada.

- **Celdas de código y de texto.** Combinas código ejecutable con explicaciones. Sirve para analizar y también para documentar.
- **Ejecución de celdas.** Cada celda recuerda lo que hicieron las anteriores. **El orden de ejecución importa** y puede ser distinto del orden en pantalla.
- **Reiniciar el entorno.** Si el estado se enreda, usa *Entorno de ejecución → Reiniciar* y vuelve a ejecutar todo desde el inicio. Es la forma más confiable de depurar.
- **Instalar librerías.** Con `!pip install <paquete>`. El signo `!` indica que es un comando del sistema, no de Python.
- **Conectar Google Drive.** Permite leer y guardar tus archivos (el contorno del lote, un CSV).
- **Jupyter local.** Es la alternativa si prefieres no depender de la nube; funciona igual.

## 2. Fundamentos del lenguaje

### Variables y tipos

| Tipo | Qué es | Ejemplo agronómico |
|---|---|---|
| `int` | Número entero | Hectáreas redondeadas |
| `float` | Número decimal | Reflectancias, valores de índices |
| `str` | Texto | Nombre del lote, fecha escrita como texto |
| `bool` | Verdadero o falso | ¿El NDVI es mayor que 0,5? |

### Listas y diccionarios

- **Lista:** colección ordenada, por ejemplo los NDVI de una campaña.
- **Diccionario:** pares clave–valor, por ejemplo los atributos de un lote.

```python
lote = {"nombre": "Lote 3", "cultivo": "trigo", "ha": 42}
print(lote["cultivo"])  # trigo
```

### Condicionales y bucles

Los usarás para clasificar valores de NDVI según rangos (los mismos del [capítulo 3](03-indices-vegetacion.md)):

```python
for valor in ndvi_serie:
    if valor < 0.2:
        clase = "suelo desnudo"
    elif valor < 0.4:
        clase = "cultivo en implantación"
    elif valor < 0.6:
        clase = "cobertura intermedia"
    else:
        clase = "cultivo en pleno desarrollo"
    print(f"NDVI = {valor:.2f} -> {clase}")
```

### Funciones

Una función encapsula un cálculo para reutilizarlo. La primera será el NDVI:

```python
def ndvi(nir, red):
    return (nir - red) / (nir + red)

print(ndvi(0.45, 0.06))  # 0.76
```

La misma idea se usará en los próximos capítulos, pero aplicada a imágenes completas.

### Leer los mensajes de error

**Un error es una pista, no un fracaso.** `TypeError`, `KeyError` o `ZeroDivisionError` dicen qué falló y dónde. Aprender a leerlos es tan importante como escribir código correcto.

## 3. Librerías clave

- **numpy:** arreglos y operaciones aplicadas de una vez a todos los valores. Idea central: **una banda satelital es una matriz de números**.
- **pandas:** tablas (`DataFrame`), lectura de CSV con `read_csv`, filtros, fechas con `pd.to_datetime` y agrupamientos (por ejemplo, promedio por mes).
- **matplotlib:** gráficos de líneas (series de tiempo), de dispersión e imágenes (`imshow`, con barra de color).

## 4. Primer contacto con un raster

Un **raster** no es solo una imagen: es una **matriz de valores con metadatos**: sistema de coordenadas (CRS), tamaño de píxel y extensión geográfica.

Aquí lo verás de forma simple: una banda como matriz que se muestra con `imshow`. El [capítulo 6](06-procesamiento-raster.md) profundiza con `rasterio` y `rioxarray`.

---

## Práctica guiada

1. **Cargar** el CSV `lote_reflectancias_v2.csv` (fechas, NIR y rojo medios del lote).
2. **Calcular el NDVI** en una columna nueva, sin bucles.
3. **Filtrar** fechas con datos inválidos.
4. **Graficar** la serie con título, ejes y fechas legibles.
5. **Visualizar** una banda y su NDVI con `imshow` (raster de muestra simulado).

### Sobre los datos de la práctica

El CSV simula un lote de trigo entre septiembre y enero. Sus valores son coherentes con el [capítulo 3](03-indices-vegetacion.md): el suelo al inicio da NDVI de ~0,1–0,2 y el cultivo en pleno desarrollo supera 0,8. Incluye **dos filas "sucias" a propósito**:

| Fecha | Problema | Qué pasa al calcular |
|---|---|---|
| 22‑sep‑2024 | NIR = 0 y rojo = 0 (dato faltante) | 0/0 da `NaN` |
| 10‑nov‑2024 | NIR = −0,05 (reflectancia negativa, imposible) | NDVI ≈ −5, fuera de rango |

### Cómo filtrar

```python
invalidas = (
    df["nir"].le(0) | df["red"].le(0)        # reflectancia nula o negativa
    | ~df["ndvi"].between(-1, 1)             # NDVI fuera del rango posible (también atrapa los NaN)
)
df_limpio = df[~invalidas].copy()
```

El criterio mira la **reflectancia** y el **rango físico**. No descarta NDVI negativos por sí solos: en un lote anegado o con agua visible pueden ser reales. Los NDVI bajo 0 se marcan como *sospechosos* y se revisan, no se eliminan en automático.

**División por cero:** en Python "puro" lanza `ZeroDivisionError`. En numpy y pandas **no** lanza error: devuelve `inf` o `NaN`. Por eso hay que revisar el resultado.

## Producto esperado

Un notebook ejecutado de principio a fin, con celdas de texto que expliquen cada paso. Es el primer producto reproducible del libro.

## Errores frecuentes

- Ejecutar celdas fuera de orden.
- Fechas leídas como texto (usa `parse_dates` o `pd.to_datetime`).
- No revisar `NaN` e `inf` tras dividir en numpy o pandas.
- Confundir `/` (división) con `//` (división entera, descarta decimales).

## Ideas clave de cierre

1. Programar no reemplaza a los visores: los complementa en automatización, reproducibilidad y escala.
2. Variables, listas, diccionarios y funciones bastan para pasar de "ver una imagen" a "procesar datos".
3. numpy, pandas y matplotlib te acompañarán en el resto del libro.
4. Un raster es una matriz con metadatos geoespaciales.
5. Un mensaje de error es información: léelo.

**Avance del proyecto:** sube el contorno de tu lote a Google Drive y crea un **proyecto de Google Cloud registrado para Earth Engine** (de uso no comercial). Déjalo listo antes del [capítulo 5](05-acceso-imagenes.md), donde la autenticación suele ser el primer obstáculo.
