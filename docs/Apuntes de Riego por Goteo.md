# Apuntes de Riego por Goteo

Nov 8, 2026 · @Javiera Francisca González Mardones

## 1. Diseño agronómico

Determina cuánta agua necesita el cultivo, cómo se reparte con los emisores y cuánto tiempo y con qué frecuencia debe regar el sistema.

### 1.1 Evapotranspiración del cultivo (ETc)

$$
ET_c = ET_o \times K_c
$$

ETc y ETo en mm/día; Kc adimensional.

### 1.2 Demanda bruta (Db)

$$
D_b = \frac{ET_c}{E_a}
$$

Ea = eficiencia de aplicación (0,9 en los apuntes). Se divide porque hay que aplicar más agua que la que consume el cultivo: con Ea = 0,9, Db es mayor que ETc.

### 1.3 Volumen de agua por planta y por hectárea

$$
V_{planta} = D_b \times (DSH \times DEH)
$$

V\_planta en L/planta/día, Db en mm/día, DSH (distancia sobre hilera) y DEH (distancia entre hileras) en m. Esto funciona porque 1 mm sobre 1 m² equivale a 1 L.

$$
V_{ha} = D_b \times 10
$$

V\_ha en m³/ha/día, porque 1 mm = 10 m³/ha.

### 1.4 Número de emisores por planta

$$
n_e = \frac{DSH}{D_e} \times NL
$$

De = distancia entre emisores (m); NL = número de líneas de riego por hilera. Se prueba primero con 1 emisor y se ajusta según el humedecimiento (1.9).

### 1.5 Precipitación del equipo (Pp)

$$
P_p = \frac{q_e \times n_e}{DSH \times DEH}
$$

Pp en mm/h; qe = caudal del emisor (L/h).

### 1.6 Tiempo de riego (TR)

$$
TR = \frac{D_b}{P_p}
$$

TR en h. Más demanda alarga el riego; más Pp lo acorta.

### 1.7 Agua aprovechable y lámina neta

$$
HA = \frac{CC - PMP}{100} \times D_a \times D_z
$$

HA en mm; CC y PMP en % (base peso seco); Da = densidad aparente (g/cm³); Dz = profundidad de raíces (mm).

$$
LN = HA \times UR
$$

UR = umbral de riego, como fracción (por ejemplo 0,4).

### 1.8 Diámetro de humedecimiento (DH)

DH en m, qe en L/h. Depende de la textura del suelo:

| Textura | DH (m) |
| --- | --- |
| Franco-arcilloso | 1,2 + 0,10 · qe |
| Franco | 0,7 + 0,11 · qe |
| Arenoso | 0,3 + 0,12 · qe |

### 1.9 Área y porcentaje de humedecimiento

$$
AH = n_e \times \frac{\pi \, DH^2}{4}
$$

Supone bulbos circulares que no se traslapan. Con goteros muy juntos el área real es una franja continua y esta fórmula la sobrestima.

$$
PH = \frac{100 \times AH}{DSH \times DEH}
$$

Criterio de los apuntes: PH ≥ 40 %. Si no se cumple, se agrega un emisor más por planta y se recalcula desde 1.5.

### 1.10 Frecuencia de riego (FR)

$$
FR = \frac{LN \times PH/100}{ET_c}
$$

PH entra como fracción (PH/100). Calcula PH (1.9) antes que FR. FR se redondea hacia abajo, a días enteros.

### 1.11 Sectores de riego

$$
N_s = \frac{TO}{TR}
$$

TO = tiempo de operación disponible (h/día). Ns se redondea hacia abajo, a un entero.

$$
A_s = \frac{A_{total}}{N_s \times FR}
$$

A\_s en ha: superficie de cada sector. En un día de riego operan Ns sectores, y cada sector se riega una vez cada FR días.

### 1.12 Emisores por sector y caudal del sector

$$
N_{e/s} = \frac{A_s}{D_e \times DEH} \times NL
$$

Usa A\_s (convertida a m²: 1 ha = 10 000 m²), no A\_total.

$$
Q_s = N_{e/s} \times q_e
$$

Qs sale en L/h; se divide por 3600 para L/s. Se compara con el caudal máximo disponible Qmáx.

### 1.13 Corrección del área por caudal disponible

Si el caudal del sector (Qs, calculado en 1.12) supera el caudal máximo que entrega la fuente o la bomba (Qmáx), el sector no se puede regar completo: no alcanza el agua para que todos los emisores funcionen a la vez. La solución es achicar el sector hasta que su caudal sea igual a Qmáx.

Para calcular esa área se escribe el caudal del sector en función de su superficie. Plantas en el sector × emisores por planta × caudal de cada emisor, pasado de L/h a L/s:

$$
Q_{m\acute{a}x} = \frac{A_s \times 10\,000}{DSH \times DEH} \times n_e \times \frac{q_e}{3600}
$$

Despejando A\_s (y pasando de m² a ha, dividiendo por 10 000) queda:

$$
A_{s,corr} = \frac{0{,}36 \times DSH \times DEH \times Q_{m\acute{a}x}}{n_e \times q_e}
$$

Variables y unidades:

- A\_s,corr: área corregida del sector (ha).
- DSH y DEH: distancias sobre hilera y entre hileras (m).
- Qmáx: caudal máximo disponible (L/s).
- n\_e: emisores por planta.
- q\_e: caudal de cada emisor (L/h).

El 0,36 sale de 3600 / 10 000: el 3600 convierte L/h a L/s y el 10 000 convierte m² a ha. La fórmula es equivalente a usar N\_e/s de 1.12, porque n\_e = DSH / De × NL.

Ejemplo: DSH = 2 m, DEH = 4 m, De = 0,5 m, NL = 1, qe = 4 L/h, Qmáx = 5 L/s. Entonces n\_e = 2 / 0,5 × 1 = 4 emisores por planta. Supón que de 1.11 salió A\_s = 2 ha (A\_total = 24 ha, Ns = 3, FR = 4 días).

1. Caudal del sector con 2 ha: N\_e/s = 20 000 / (0,5 × 4) = 10 000 emisores. Qs = 10 000 × 4 = 40 000 L/h = 11,1 L/s.
2. Como 11,1 L/s > 5 L/s, hay que corregir.
3. A\_s,corr = 0,36 × 2 × 4 × 5 / (4 × 4) = 0,9 ha.
4. Verificación: 0,9 ha tiene 4 500 emisores, que dan 18 000 L/h = 5 L/s. Cumple.

Consecuencia: cada sector baja de 2 ha a 0,9 ha, así que el área regable es A\_s,corr × Ns × FR = 0,9 × 3 × 4 = 10,8 ha, menos que las 24 ha totales. Para cubrir todo hay que aumentar Qmáx, subir las horas de operación (más sectores) o reducir el caudal instalado (menos emisores por planta o emisores de menor caudal).

### 1.14 Uniformidad de distribución

$$
CU = \frac{Q_{25\%}}{Q_{prom}} \times 100
$$

Q25 % = caudal promedio del 25 % de los emisores con menor caudal; Qprom = caudal promedio de todos los aforados. Criterio: CU > 80 %. Si no se cumple, hay que buscar las causas (obstrucción, presión, filtración). Para el tiempo de riego, usar el caudal promedio aforado y considerar CU.

## 2. Diseño hidráulico

Determina diámetros de tubería, pérdidas de energía y presión necesaria desde la bomba hasta el último emisor.

### 2.1 Pérdida de carga unitaria (Hazen-Williams)

Cuando el agua circula por una tubería pierde energía por roce con las paredes. J es esa pérdida por cada metro de tubería: cuántos metros de columna de agua (m.c.a.) se pierden por metro de largo. Hazen-Williams es la ecuación empírica más usada para agua en tuberías a presión, y relaciona J con el caudal, el diámetro y el material.

La fórmula estándar de Hazen-Williams, en unidades del Sistema Internacional, es:

$$
J = \frac{10{,}67 \times Q^{1{,}852}}{C^{1{,}852} \times D^{4{,}87}}
$$

con Q en m³/s, D en m y J en m/m. Vale para agua a temperatura ambiente en flujo turbulento.

Variables y unidades:

- J: pérdida de carga unitaria (m/m, es decir m.c.a. por metro de tubería).
- Q: caudal que circula por ese tramo (m³/s).
- D: diámetro interno de la tubería (m), no el nominal. Se obtiene con Di = De − 2e (2.9).
- C: coeficiente de rugosidad del material (2.2).

Cómo leerla, con tres efectos:

- **Caudal:** el exponente 1,852 hace que la pérdida crezca más que el caudal. Al duplicar Q, J se multiplica por 2^1,852 ≈ 3,6.
- **Diámetro:** el exponente 4,87 hace que un pequeño aumento de D reduzca mucho la pérdida. Subir D un 10 % baja J cerca de un 37 %. Por eso el diámetro es la principal herramienta para controlar las pérdidas.
- **Material:** a igual Q y D, una tubería de acero soldado (C = 120) pierde cerca de 1,5 veces más que una de PVC (C = 150).

Ejemplo: tubería de PVC (C = 150), Q = 10 m³/h = 0,00278 m³/s, diámetro interno D = 63 mm = 0,063 m.

1. Q^1,852 = 0,00278^1,852 ≈ 1,84 × 10⁻⁵; D^4,87 = 0,063^4,87 ≈ 1,42 × 10⁻⁶; C^1,852 = 150^1,852 ≈ 10 700.
2. J = 10,67 × 1,84 × 10⁻⁵ / (10 700 × 1,42 × 10⁻⁶) ≈ 0,0129 m/m, es decir 1,29 m por cada 100 m de tubería.
3. Con L = 100 m, la pérdida por fricción en ese tramo es J × L ≈ 1,3 m.c.a.
4. Si la misma tubería fuera de acero soldado (C = 120), J pasa a 0,0129 × (150/120)^1,852 ≈ 0,0195 m/m.

Ese J se usa después en cada tramo: en el lateral y el port se multiplica por L y por FSM (2.4 y 2.5), y en la matriz solo por L (2.6).

### 2.2 Coeficiente de rugosidad (C)

Un C mayor significa menos fricción. Verificar valores.

| Material | C (apuntes) |
| --- | --- |
| Hierro fundido usado | 90 |
| Acero fundido | 135 |
| Acero galvanizado | 125 |
| Acero remachado | 110 |
| Acero soldado y concreto común | 120 |
| Aluminio | 120 |
| Asbesto-cemento | 145 |
| Cobre y latón | 130 |
| Concreto con acabado liso | 100 |
| PVC y layflat | 150 |

### 2.3 Factor de salidas múltiples (FSM)

$$
FSM = \frac{1}{\beta + 1} + \frac{1}{2n} + \frac{\sqrt{\beta - 1}}{6 n^2}
$$

n = número de salidas (emisores o laterales). β es el exponente de Q en la fórmula de pérdidas: con Hazen-Williams es 1,852. El FSM reduce la pérdida porque el caudal disminuye a lo largo de la tubería.

### 2.4 Lateral

$$
H_{f,lateral} = J \times L \times FSM
$$

$$
P_{in,lateral} = P_{op} + H_{f,lateral} \pm \Delta Z
$$

L en m. Pop = presión de operación del emisor más crítico (el más desfavorable hidráulicamente, normalmente el último del lateral). ΔZ es la diferencia de cota entre la entrada y el final del lateral: suma si el lateral sube, resta si baja. Como Pop es la presión del emisor más crítico, Pop + Hf garantiza que ese emisor reciba al menos la presión de diseño.

### 2.5 Port lateral (tubería terciaria)

$$
H_{f,port} = J \times L \times FSM
$$

$$
P_{in,port} = P_{in,lateral} + H_{f,port} \pm \Delta Z
$$

Alimenta a los laterales, por eso también lleva FSM (n = número de laterales).

### 2.6 Tubería matriz

$$
H_{f,matriz} = J \times L
$$

$$
P_{in,matriz} = P_{in,port} + H_{f,matriz} \pm \Delta Z
$$

Sin FSM, porque transporta el caudal completo en todo su largo.

### 2.7 Singularidades y pérdida total

$$
H_s = 0{,}2 \times H_f
$$

$$
H_f = H_{f,lateral} + H_{f,port} + H_{f,matriz}
$$

Hs = pérdidas por codos, válvulas, uniones y cambios de sección; los apuntes usan 20 % de Hf.

### 2.8 Carga dinámica total (CDT)

$$
CDT = H_g + P_{op} + H_f + H_s + H_{cab}
$$

- Hg: altura geométrica (succión + impulsión).
- Pop: presión de operación del emisor más crítico.
- Hf: pérdidas de carga por fricción (lateral + port + matriz).
- Hs: pérdidas por singularidades.
- Hcab: pérdidas en el cabezal (filtros, válvulas, venturi).

Todo en m.c.a. (1 bar ≈ 10,2 m.c.a.). La CDT y el caudal Qs definen la bomba.

### 2.9 Velocidad del agua

$$
V = \frac{Q}{A} = \frac{4\,Q}{\pi \, D_i^2}
$$

$$
D_i = D_e - 2e
$$

V en m/s; Q en m³/s; Di = diámetro interno (m); De = diámetro exterior; e = espesor de pared. Criterio de diseño: 0,5 a 2 m/s, y en PVC conviene no pasar de unos 1,5 m/s.

## 3. Resumen de fórmulas y criterios

Orden de cálculo del diseño agronómico:

1. ETo → ETc → Db.
2. HA → LN.
3. Emisores (n\_e), Pp y TR.
4. DH → AH → PH (si PH < 40 %, agregar un emisor y volver al paso 3).
5. FR, Ns y A\_s.
6. N\_e/s, Qs y, si hace falta, A\_s corregida.
7. Uniformidad (CU).

| Variable | Fórmula | Unidades |
| --- | --- | --- |
| ETc | ETo × Kc | mm/día |
| Db | ETc / Ea | mm/día |
| V\_planta | Db × DSH × DEH | L/planta/día |
| V\_ha | Db × 10 | m³/ha/día |
| n\_e | DSH / De × NL | emisores/planta |
| Pp | qe × n\_e / (DSH × DEH) | mm/h |
| TR | Db / Pp | h |
| HA | (CC − PMP)/100 × Da × Dz | mm |
| LN | HA × UR | mm |
| AH | n\_e × π DH² / 4 | m² |
| PH | 100 × AH / (DSH × DEH) | % |
| FR | LN × (PH/100) / ETc | días |
| Ns | TO / TR | sectores |
| A\_s | A\_total / (Ns × FR) | ha |
| N\_e/s | A\_s / (De × DEH) × NL | emisores |
| Qs | N\_e/s × qe | L/h (÷ 3600 = L/s) |
| A\_s,corr | 0,36 × DSH × DEH × Qmáx / (n\_e × qe) | ha |
| CU | Q25% / Qprom × 100 | % |
| J | 105 190 × Q^1,852 / D^4,87 × (150/C)^1,852 | m/m |
| FSM | 1/(β+1) + 1/(2n) + √(β−1)/(6n²) | adimensional |
| Hf lateral y port | J × L × FSM | m |
| Hf matriz | J × L | m |
| Hs | 0,2 × Hf | m |
| CDT | Hg + Pop + Hf + Hs + Hcab | m.c.a. |
| V | 4Q / (π Di²) | m/s |

Criterios de diseño:

| Criterio | Valor |
| --- | --- |
| Porcentaje de humedecimiento | PH ≥ 40 % (apuntes) |
| Uniformidad | CU > 80 % |
| Velocidad en tuberías | 0,5 a 2 m/s (PVC ≤ \~1,5 m/s) |
| Redondeo de FR y Ns | hacia abajo, a enteros |
| Variación máxima aceptable de caudal entre emisores | 10 % |
