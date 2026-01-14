import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Lectura Excel

df = pd.read_excel("menores.xlsx")

# Columnas numéricas 

for col in ["ve", "pbl", "pblniva", "importeadjudicacion", "importeadjudicacioniva"]:
    df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors="coerce")

# Columna fecha

df["fechaacuerdo"] = pd.to_datetime(
    pd.to_numeric(df["fechaacuerdo"], errors="coerce")
    .astype("float64"), origin="1899-12-30", unit="D")



# Franjas VE

bins = [0,2500,5000,7500,10000,12500,15000]
labels=["Menos de 2.500 €", "2.500 € - 5.000 €", "5.000 €- 7.500 €", "7.500 € - 10.000 €", "10.000 € - 12.500 €","12.500 € - 15.000 €"]

bins2 = list(range(0,16000,1000))
labels2 = [
    "0 - 1.000 €",
    "1.001 € - 2.000 €",
    "2.001 € - 3.000 €",
    "3.001 € - 4.000 €",
    "4.001 € - 5.000 €",
    "5.001 € - 6.000 €",
    "6.001 € - 7.000 €",
    "7.001 € - 8.000 €",
    "8.001 € - 9.000 €",
    "9.001 € - 10.000 €",
    "10.001 € - 11.000 €",
    "11.001 € - 12.000 €",
    "12.001 € - 13.000 €",
    "13.001 € - 14.000 €",
    "14.001 € - 15.000 €"
]


# Creo columna con franjas

df["franja_ve"] = pd.cut(df["ve"], bins=bins2, labels=labels2, include_lowest=True)

# Filtro por servicios y suministros

df_ss = df[df["tipocontrato"].str.lower().isin(["servicios", "suministros"])]
df_ss = df_ss[df_ss["ve"] < 15000].copy()

estadisticas = (
    df_ss
    .groupby("franja_ve")
    .size()
    .reset_index(name="num_contratos")
    
)

estadisticas["Porcentaje"] = round((estadisticas["num_contratos"] / sum(estadisticas["num_contratos"]))*100,2)

print(estadisticas)

# Gráfico barras

plt.figure(figsize=(12,6))
sns.barplot(
    data=estadisticas,
    x="franja_ve",
    y = "num_contratos", 
    palette="Blues_d"
)
plt.xticks(rotation=45, ha = "right")
plt.xlabel("Franjas VE")
plt.ylabel("Número de contratos")
plt.title("Distribución de contratos por valor estimado")

plt.tight_layout()
plt.show()

