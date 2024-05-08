import matplotlib.pyplot as plt
import geopandas as gpd
import imageio
import pandas as pd
import os
import geobr 

from datetime import datetime

# Load data
df = pd.read_csv('locations_info.csv')

df_brazil = df[df['Country'] == "Brazil"]
# Group by month and country
df_state_brazil = df_brazil.groupby(['Month', 'State']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

states = geobr.read_state(year=2020)


# Mapeamento de nomonth de países
# mapeamento_paises = {
#     'United States': 'United States of America',
#     'The Netherlands': 'Netherlands'
# }

colors_hex = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']
# Definir os intervalos de valores e as cores correspondentes
value_intervals = [(1, 11), (11, 100), (101, 1000), (1001, 10000), (10001, 100000), (100001, 1000000), (1000000, float('inf'))]
#colors_hex = ['#67a9cf', '#d1e5f0', '#fddbc7', '#ef8a62', '#b2182b']

#['#b2182b','#ef8a62','#fddbc7','#f7f7f7','#d1e5f0','#67a9cf','#2166ac']
# ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d'] -> cores vermelho


# Adicione uma coluna 'color' ao DataFrame df_state_brazil com a cor correspondente a cada país
def get_color(value):
    for i, (start, end) in enumerate(value_intervals):
        if start <= value < end:
            return colors_hex[i]
    return colors_hex[-1]

df_state_brazil['color'] = df_state_brazil['Occurrences'].apply(lambda x: get_color(x))

images = []
months = []
# Iterar sobre cada mês no DataFrame
for i, month in enumerate(df_state_brazil['Month'].unique(), start=1):
    df_month = df_state_brazil[df_state_brazil['Month'] == month]
    #df_month['State'] = df_month['State'].map(mapeamento_paises).fillna(df_month['State'])
    
    legend_labels = ['1 - 10', '11 - 100','101 - 1000', '1001 - 10.000', '10.001 - 100.000','100.001 - 1.000.000', '1.000.000 +']

    # Plot all Brazilian states
    fig, ax = plt.subplots(figsize=(6,6))

    states.plot(facecolor="lightgrey", edgecolor="black", ax=ax,linewidth=0.5)

    legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors_hex]
    # Definir cor de fundo para cinza claro
    #fig.patch.set_facecolor('#f0f0f0')

    # for state_name in states["name_state"]:
    #     if state_name not in df_month["State"].values:
    #         country = states[states["name_state"] == state_name]
    #         country.plot(ax=ax, color="lightgrey")

    for _, row in df_month.iterrows():
        state = row['State']
        country_color = row['color']

        if state in states["name_state"].values:
            state = states[states["name_state"] == state]
            state.plot(ax=ax, color=country_color)

    ax.legend(legend_patches, legend_labels, loc="lower left", fontsize='small')
    #ax.set_facecolor('Gainsboro')
    ax.set_xticks([])
    ax.set_yticks([])

    #ax.set_title("States", fontsize=20)

    ax.set_title(f'Number of srcIP - MiscAttack in {month}')
    directory = 'gpd-maps-images/brazil-states/'
    # plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    plt.savefig(os.path.join(directory, f'srcIPs_{month}.png'), dpi=150)
    
    months.append(month)

# Custom sorting function to convert month-year string to datetime object
def custom_sort(month_year):
    return datetime.strptime(month_year, "%Y-%m")

# Sort the list
sorted_month_year_list = sorted(months, key=custom_sort)

# Print the sorted list
print(sorted_month_year_list)

# Ordenar as imagens com base nos meses
#images_sorted = [img for _, img in sorted(zip(months, images))]


# Iterar sobre cada mês no DataFrame
for month in sorted_month_year_list:
    images.append(imageio.imread(f'{directory}srcIPs_{month}.png'))


# Ordenar as imagens com base nos meses
#images_sorted = [img for _, img in sorted(zip(months, images))]

# Salvar as imagens ordenadas como GIF
imageio.mimsave(os.path.join(directory, 'srcIPs_states.gif'), images, fps=1)

plt.close()

