import matplotlib.pyplot as plt
import geopandas as gpd
import imageio
import pandas as pd
import os

from datetime import datetime

# Carrega os dados
df = pd.read_csv('csv/locations_srcIP_info.csv')

# Agrupa por mes e paises somando as ocorrencias
df_country = df.groupby(['Month', 'Country']).agg({'Occurrences': 'sum'}).reset_index()

# Mapeamento de nome dos países para que correspondam aos nomes do df geopandas
mapeamento_paises = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
}

# Define os intervalos de valores e as cores correspondentes
value_intervals = [(1, 11), (11, 100), (101, 1000), (1001, 10000), (10001, 100000), (100001, 1000000), (1000000, float('inf'))]
colors_hex = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']

#colors_hex = ['#67a9cf', '#d1e5f0', '#fddbc7', '#ef8a62', '#b2182b']
# ['#b2182b','#ef8a62','#fddbc7','#f7f7f7','#d1e5f0','#67a9cf','#2166ac']
# ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d'] -> cores vermelho


# Adiciona uma coluna 'color' ao DataFrame df_country com a cor correspondente a cada país
def get_color(value):
    for i, (start, end) in enumerate(value_intervals):
        if start <= value < end:
            return colors_hex[i]
    return colors_hex[-1]

df_country['color'] = df_country['Occurrences'].apply(lambda x: get_color(x))

# Carrega os dados do mundo
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

images = []
months = []
# Itera sobre cada mês no DataFrame
for i, month in enumerate(df_country['Month'].unique(), start=1):

    df_month = df_country[df_country['Month'] == month]
    df_month['Country'] = df_month['Country'].map(mapeamento_paises).fillna(df_month['Country'])

    legend_labels = ['1 - 10', '11 - 100','101 - 1000', '1001 - 10.000', '10.001 - 100.000','100.001 - 1.000.000', '1.000.000 +']

    fig, ax = plt.subplots(figsize=(10, 10))
    legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors_hex]

    # Define a cor de fundo para cinza claro
    #fig.patch.set_facecolor('#f0f0f0')

    world.boundary.plot(ax=ax, color="black", linewidth=0.3)

    for country_name in world["name"]:
        if country_name not in df_month["Country"].values:
            country = world[world["name"] == country_name]
            country.plot(ax=ax, color="lightgrey")

    for _, row in df_month.iterrows():
        pais = row['Country']
        country_color = row['color']

        if pais in world["name"].values:
            country = world[world["name"] == pais]
            country.plot(ax=ax, color=country_color)

    ax.legend(legend_patches, legend_labels, loc="lower left", fontsize='small')
    #ax.set_facecolor('Gainsboro')
    ax.set_xticks([])
    ax.set_yticks([])

    directory = 'teste-dict/'

    ax.set_title(f'Number of srcIP - MiscAttack in {month}')
    directory = 'gpd-maps-images/global-comp/'
    # plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    plt.savefig(os.path.join(directory, f'srcIPs_{month}.png'), dpi=150)
    
    months.append(month)

# Converte month-year string para um objeto do tipo datetime
def custom_sort(month_year):
    return datetime.strptime(month_year, "%Y-%m")

# Ordena a lista de meses
sorted_month_year_list = sorted(months, key=custom_sort)
#print(sorted_month_year_list)

# Itera sobre cada mês no DataFrame de meses ordenado
for month in sorted_month_year_list:
    images.append(imageio.imread(f'{directory}srcIPs_{month}.png'))

# Salva as imagens ordenadas como GIF
imageio.mimsave(os.path.join(directory, 'srcIPs.gif'), images, fps=1)
plt.close()

