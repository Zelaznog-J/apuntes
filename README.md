# Apuntes de Geociencia de Datos

🔗 Disponible en: **https://zelaznog-j.github.io/apuntes/**

Libro de apuntes de Análisis, GeoComputación con Python y Teledetección, hecho con MkDocs Material y mkdocs-jupyter.

## Estructura

```
docs/
├── index.md                 # portada
├── 01-analisis/             # una carpeta por parte
│   ├── index.md             # intro de la parte
│   └── 01-*.md | 01-*.ipynb # un archivo por capítulo
├── 02-geocomputacion/
│   ├── NN-*.md | NN-*.ipynb
│   ├── img/                 # figuras de los capítulos (NN-nombre.png)
│   └── 09-curvas-de-nivel/  # capítulo con subpáginas: index.md + páginas + datos/
└── 03-teledeteccion/
```

## Agregar un capítulo

1. Crear `docs/<parte>/NN-nombre.md` o `.ipynb`. Los notebooks se publican con sus salidas guardadas, sin volver a ejecutarse: córrelos completos antes de hacer commit.
2. Añadirlo al `nav` de `mkdocs.yml` y a la lista del `index.md` de la parte.
3. Plantilla: pregunta guía → objetivos → conceptos → ejemplo → errores frecuentes → ejercicios → referencias.
4. Un capítulo con varias páginas va en su propia carpeta (`NN-nombre/index.md` + subpáginas), como `02-geocomputacion/09-curvas-de-nivel/`.
5. Nombres en minúsculas, sin tildes ni espacios. No subir salidas generadas por los notebooks (ver `.gitignore`).
6. Los capítulos en preparación llevan el aviso `!!! warning "Capítulo en preparación"`; al terminarlos, quitar el aviso y actualizar la columna *Estado* del `index.md` de la parte.

## Uso local

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000/apuntes/
mkdocs build --strict
```

Cada push a `main` publica el sitio con GitHub Actions (`.github/workflows/deploy.yml`).
