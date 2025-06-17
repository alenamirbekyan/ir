import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Définir les chemins vers les fichiers CSV
CSV_DIR = Path("method/experiments/results")
files = {
    7: CSV_DIR / "results_7.csv",
    10: CSV_DIR / "results_10.csv",
    20: CSV_DIR / "results_20.csv",
    50: CSV_DIR / "results_50.csv",
    100: CSV_DIR / "results_100.csv",
    200: CSV_DIR / "results_200.csv",
    500: CSV_DIR / "results_500.csv",
    1000: CSV_DIR / "results_1000.csv",
}

# Charger les données
all_data = []
for size, path in files.items():
    if path.exists():
        df = pd.read_csv(path)
        df["graph_size"] = size
        all_data.append(df)
    else:
        print(f"Fichier introuvable: {path}")

# Fusionner toutes les données en un seul DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Calcul des moyennes par taille de graphe
summary = combined_df.groupby("graph_size").agg({
    "initial_latency": "mean",
    "final_latency": "mean",
    "execution_time": "mean",
    "iterations": "mean"
}).reset_index()

# Tracer le graphique des latences moyennes
plt.figure(figsize=(10, 6))
plt.plot(summary["graph_size"], summary["initial_latency"], marker="o", label="Initial latency")
plt.plot(summary["graph_size"], summary["final_latency"], marker="o", label="Final latency")
plt.xlabel("Taille du graphe (nombre de nœuds)")
plt.ylabel("Latence moyenne")
plt.title("Latence moyenne initiale vs finale - Algorithme de Metropolis")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
