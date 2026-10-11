import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, KFold, cross_val_predict
from sklearn.metrics import classification_report, accuracy_score

rng = np.random.default_rng(42)
fechas = ["ndvi_oct", "ndvi_nov", "ndvi_ene"]
perfiles = {                      # NDVI medio esperado en cada fecha (valores ilustrativos)
    "trigo":   [0.55, 0.72, 0.30],
    "maiz":    [0.25, 0.40, 0.75],
    "pradera": [0.50, 0.55, 0.50],
    "suelo":   [0.15, 0.17, 0.16],
}
filas = []
id_lote = 0
for cultivo, perfil in perfiles.items():
    for _ in range(10):                                   # 10 lotes por clase
        id_lote += 1
        desfase = rng.normal(0, 0.12, len(perfil))        # lo que distingue a un lote de otro
        for _ in range(40):                               # 40 píxeles por lote
            ndvi = np.array(perfil) + desfase + rng.normal(0, 0.02, len(perfil))
            filas.append([id_lote, cultivo, *ndvi.clip(0, 0.95)])
df = pd.DataFrame(filas, columns=["id_lote", "cultivo", *fechas])
X, y, grupos = df[fechas], df["cultivo"], df["id_lote"]
rf = RandomForestClassifier(n_estimators=300, random_state=42)
p_azar = cross_val_predict(rf, X, y, cv=KFold(5, shuffle=True, random_state=0))
p_lote = cross_val_predict(rf, X, y, groups=grupos, cv=GroupKFold(n_splits=5))
print("exactitud validación al azar:", round(accuracy_score(y, p_azar), 3))
print("exactitud validación por lote:", round(accuracy_score(y, p_lote), 3))
print(classification_report(y, p_lote, digits=2))
rf.fit(X, y)
print(dict(zip(fechas, rf.feature_importances_.round(2))))
df.to_csv("muestras_cultivos.csv", index=False)
