# Fundamentos espectrales

!!! abstract "Objetivos"
    - Entender qué mide un sensor óptico.
    - Calcular un índice espectral normalizado.

## Conceptos

Cada cobertura refleja la radiación de forma distinta según la longitud de onda: su **firma espectral**. La vegetación sana absorbe el rojo y refleja fuertemente el infrarrojo cercano (NIR).

El **NDVI** aprovecha ese contraste:

\[
\mathrm{NDVI} = \frac{\rho_{\mathrm{NIR}} - \rho_{\mathrm{Rojo}}}{\rho_{\mathrm{NIR}} + \rho_{\mathrm{Rojo}}}
\]

| Banda Sentinel-2 | Región | Longitud de onda central |
| --- | --- | --- |
| B04 | Rojo | 665 nm |
| B08 | NIR | 842 nm |

## Ejercicios

1. ¿Qué valores de NDVI esperas para agua, suelo desnudo y bosque?

## Referencias

- Chuvieco, E. (2020). *Fundamentals of Satellite Remote Sensing*. CRC Press.
