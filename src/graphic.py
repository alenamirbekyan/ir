import matplotlib.pyplot as plt
import pandas as pd

# Données (en provenance de stats.py)
results = {
    10: {'Bypass': 4.05, 'Bypass Metropolis': 4.05, 'SDA': 5.7, 'SDA Metropolis': 4.5, 'Visited': 4.15, 'Visited Metropolis': 4.1, 'CSP': 7.45, 'CSP Metropolis': 4.65}, 
    50: {'Bypass': 6.05, 'Bypass Metropolis': 6.0, 'SDA': 19.3, 'SDA Metropolis': 9.15, 'Visited': 6.7, 'Visited Metropolis': 6.1, 'CSP': 24.65, 'CSP Metropolis': 8.95}, 
    100: {'Bypass': 7.2, 'Bypass Metropolis': 7.05, 'SDA': 31.5, 'SDA Metropolis': 10.0, 'Visited': 7.7, 'Visited Metropolis': 7.0, 'CSP': 37.95, 'CSP Metropolis': 7.9}, 
    500: {'Bypass': 9.7, 'Bypass Metropolis': 9.6, 'SDA': 131.4, 'SDA Metropolis': 9.55, 'Visited': 10.3, 'Visited Metropolis': 9.5, 'CSP': 142.1, 'CSP Metropolis': 9.5}
}

# DataFrame
df = pd.DataFrame(results).T

# Couleurs personnalisées par méthode
colors = {
    'Bypass': 'lightgreen',
    'Bypass Metropolis': 'darkgreen',
    'SDA': 'lightskyblue',
    'SDA Metropolis': 'dodgerblue',
    'Visited': 'goldenrod',
    'Visited Metropolis': 'darkgoldenrod',
    'CSP': 'pink',
    'CSP Metropolis': 'deeppink'
}

# Paramètres de style 
font_title = {'fontsize': 16, 'weight': 'bold'}
font_labels = {'fontsize': 13, 'weight': 'normal'}
font_legend = {'fontsize': 13}
font_ticks = 11

# Graphique
plt.figure(figsize=(12, 6))
for method in df.columns:
    plt.plot(df.index, df[method],
             marker='o',
             markersize=2,
             linewidth=0.8,
             label=method,
             color=colors[method])

plt.title("Nombre moyen de slots selon la méthode et la taille du graphe", **font_title)
plt.xlabel("Nombre de nœuds", **font_labels)
plt.ylabel("Nombre moyen de slots", **font_labels)
plt.yticks(range(4, 82, 3), fontsize=font_ticks)
plt.xticks(fontsize=font_ticks)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=font_legend['fontsize'])
plt.tight_layout()
plt.show()
