
# -*- coding: utf-8 -*-
# Script : plot_all_methods_dashboard.py
# Affiche 4 graphiques dans une seule figure

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des résultats
df = pd.read_csv("method/experiments/results/all_methods.csv")

# Style
sns.set(style="whitegrid")

# Création d'une figure avec 2x2 sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Analyse comparative des méthodes d'agrégation", fontsize=16)

# 1. Latence finale
sns.lineplot(data=df, x="num_nodes", y="final_latency", hue="method", marker="o", ax=axes[0, 0])
axes[0, 0].set_title("Latence finale par méthode")
axes[0, 0].set_xlabel("Nombre de nœuds")
axes[0, 0].set_ylabel("Latence finale")

# 2. Nombre de slots
sns.lineplot(data=df, x="num_nodes", y="nb_slots", hue="method", marker="o", ax=axes[0, 1])
axes[0, 1].set_title("Nombre de slots par méthode")
axes[0, 1].set_xlabel("Nombre de nœuds")
axes[0, 1].set_ylabel("Nb de slots")

# 3. Temps d'exécution
sns.lineplot(data=df, x="num_nodes", y="execution_time", hue="method", marker="o", ax=axes[1, 0])
axes[1, 0].set_title("Temps d'exécution par méthode")
axes[1, 0].set_xlabel("Nombre de nœuds")
axes[1, 0].set_ylabel("Temps (s)")

# 4. Gain en latence
gain_df = df.pivot_table(index=["num_nodes"], columns="method", values="final_latency").reset_index()
gain_df["SDA_gain"] = ((gain_df["SDA"] - gain_df["SDA+Recuit"]) / gain_df["SDA"]) * 100
gain_df["Heuristic_gain"] = ((gain_df["Heuristic"] - gain_df["Heuristic+Recuit"]) / gain_df["Heuristic"]) * 100
sns.lineplot(data=gain_df, x="num_nodes", y="SDA_gain", label="Gain SDA (%)", marker="o", ax=axes[1, 1])
sns.lineplot(data=gain_df, x="num_nodes", y="Heuristic_gain", label="Gain Heuristic (%)", marker="o", ax=axes[1, 1])
axes[1, 1].set_title("Gain en latence avec Recuit")
axes[1, 1].set_xlabel("Nombre de nœuds")
axes[1, 1].set_ylabel("Gain (%)")

# Ajustements
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
