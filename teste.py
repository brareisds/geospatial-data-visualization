import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd
import numpy as np
import pandas as pd
import imageio
import os

# Load data
df = pd.read_csv('locations_info.csv')

# Group by month and country
df_country = df.groupby(['Month', 'Country']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Load world map
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Country name mapping
country_mapping = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
}

# Definir os intervalos de valores e as cores correspondentes
value_intervals = [(1, 10000), (10000, 50000), (50000, 100000), (100000, 250000), (250000, 500000), (500000, float('inf'))]

colors_rgba = [
    [1.0, 0.96078431, 0.92156863, 1.0],  # Cor para 1 a 10 mil
    [0.99551821, 0.88963585, 0.78319328, 1.0],  # Cor para 10 mil a 50 mil
    [0.99215686, 0.77759104, 0.57366947, 1.0],  # Cor para 50 mil a 100 mil
    [0.99215686, 0.62689076, 0.34061625, 1.0],  # Cor para 100 mil a 250 mil
    [0.96526611, 0.47226891, 0.14341737, 1.0],  # Cor para 250 mil a 500 mil
    [0.87787115, 0.31932773, 0.02408964, 1.0]   # Cor para acima de 500 mil
]

legend_labels = [('1 - 10 mil'), ('10 mil - 50 mil'), ('50 mil - 100 mil'),('100 mil - 250 mil'),('250 mil - 500 mil'),('Acima de 500 mil')]

def get_color(value):
    for i, (start, end) in enumerate(value_intervals):
        if start <= value < end:
            return colors_rgba[i]
    return colors_rgba[-1]  # Retorna a última cor para valores maiores que o último intervalo

# Adicione uma coluna 'color' ao DataFrame df_country com a cor correspondente a cada país
df_country['color'] = df_country['Occurrences'].apply(lambda x: get_color(x))

# Merge com o DataFrame world
world = pd.merge(world, df_country[['Country', 'color']], left_on='name', right_on='Country', how='left')

# Preencher os valores ausentes com uma cor padrão
world['color'] = world['color'].fillna('gray')
#print(world.head(5))

images = []
# Plotar o mapa usando as cores definidas
for month in df_country['Month'].unique():
    df_month = df_country[df_country['Month'] == month]
    df_month['Country'] = df_month['Country'].map(country_mapping).fillna(df_month['Country'])
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # merged_df = pd.merge(world, df_month, left_on='name', right_on='Country', how='left')
    # print(merged_df.head(5))
    print(world.head(5))
    # world['occurrences'] = merged_df['Occurrences'].fillna(0)
    # world['color'] = merged_df['color']
    world.drop(columns=['Country', 'Month', 'Latitude', 'Longitude'], inplace=True, errors='ignore')
    
    world.plot(ax=ax, color=world['color'], legend=True, scheme="quantiles", legend_kwds={"loc": "upper right", "fmt": "{:.0f}", "title": "Occurrences", 'labels':legend_labels, 'facecolor': 'DarkGray'}, edgecolor='black', linewidth=0.1)
    
    ax.set_facecolor('Gainsboro')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'Number of srcIP - MiscAttack in {month}')
    
    directory = 'teste-dict/'
    plt.savefig(os.path.join(directory, f'srcIPs_{month}.png'), dpi=150)
    plt.close()
    
    images.append(imageio.imread(f'teste-dict/srcIPs_{month}.png'))

imageio.mimsave(os.path.join(directory, 'srcIPs.gif'), images, fps=1)


