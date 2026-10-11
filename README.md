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
└── 03-teledeteccion/
```

## Agregar un capítulo

1. Crear `docs/<parte>/NN-nombre.md` o `.ipynb`. Los notebooks se publican con sus salidas guardadas, sin volver a ejecutarse: córrelos completos antes de hacer commit.
2. Añadirlo al `nav` de `mkdocs.yml` y a la lista del `index.md` de la parte.
3. Plantilla: objetivos → conceptos → ejemplo → ejercicios → referencias.

## Uso local

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000/apuntes/
mkdocs build --strict
```

Cada push a `main` publica el sitio con GitHub Actions (`.github/workflows/deploy.yml`).
