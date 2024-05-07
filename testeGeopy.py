import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
import os

# Load data
df = pd.read_csv('locations_info.csv')

# Group by month and country
df_country = df.groupby(['Month', 'Country']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Mapeamento de nomes de Countryes
mapeamento_paises = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
   
}

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[['name', 'geometry']]

# Definir os intervalos de valores e as cores correspondentes
value_intervals = [(1, 500), (500, 1000), (1000, 50000), (50000, 100000), (100000, 500000), (500000, float('inf'))]

colors_rgba = [
    [1.0, 0.96078431, 0.92156863, 1.0],  # Cor para 1 a 10 mil
    [0.99551821, 0.88963585, 0.78319328, 1.0],  # Cor para 10 mil a 50 mil
    [0.99215686, 0.77759104, 0.57366947, 1.0],  # Cor para 50 mil a 100 mil
    [0.99215686, 0.62689076, 0.34061625, 1.0],  # Cor para 100 mil a 250 mil
    [0.96526611, 0.47226891, 0.14341737, 1.0],  # Cor para 250 mil a 500 mil
    [0.87787115, 0.31932773, 0.02408964, 1.0]   # Cor para acima de 500 mil
]

legend_labels = [('1 - 500'), ('500 - 1 mil'), ('1 mil - 50 mil'),('50 mil - 100 mil'),('100 mil - 500 mil'),('Acima de 500 mil')]

def get_color(value):
    for i, (start, end) in enumerate(value_intervals):
        print('start: ', start)
        print('end: ', end)
        print('value: ', value)
        if start <= value < end:
            print('retornou: ', colors_rgba[i])
            return colors_rgba[i]
    return colors_rgba[-1]  # Retorna a última cor para valores maiores que o último intervalo

# Adicione uma coluna 'color' ao DataFrame df_country com a cor correspondente a cada país
df_country['color'] = df_country['Occurrences'].apply(lambda x: get_color(x))
print(df_country.head(5))

# Merge com o DataFrame world
world = pd.merge(world, df_country[['Country', 'color']], left_on='name', right_on='Country', how='left')

# Preencher os valores ausentes com uma cor padrão
world['color'] = world['color'].fillna('gray')
print(world.head(5))

i = 1
images = []
# Itera sobre cada Month no DataFrame
for mes in df_country['Month'].unique():
    df_mes = df_country[df_country['Month'] == mes]
    print('\nMês: ', mes)

    # Atualiza os nomes dos Countryes
    df_mes['Country'] = df_mes['Country'].map(mapeamento_paises).fillna(df_mes['Country'])

    fig, ax = plt.subplots(1, 1, figsize = (10,10))

    # Itera sobre as linhas do DataFrame para o Month atual
    for index, row_mes in df_mes.iterrows():
        pais = row_mes['Country']
        count = row_mes['Occurrences']
        country_color = row_mes['color']

        # Plotar mapa do mundo
        world.boundary.plot(ax=ax, color="black", linewidth=0.5)

        # Calcular a cor com base nas Occurrences
        # color_index = int((count / df_mes['Occurrences'].max()) * (len(colors_normalized) - 1))
        # print('color index: ', color_index)
        # country_color = plt.cm.colors.to_rgba(colors_normalized[color_index], alpha=1.0)

        # Verificar se o Country está presente no dataframe do mundo
        if pais in world["name"].values:
            country = world[world["name"] == pais]
            print('country color: ',country_color)
            country.plot(ax=ax, color=country_color)
            #print(f'{pais} adicionado')

    # Adicionar legenda
    # add the patches to the map
    #ax.legend(handles=patches, loc="lower left", fontsize='small')
    # Desativar ticks do eixo
    ax.set_xticks([])
    ax.set_yticks([])
    directory = 'teste-dict/'
    # Definir título do gráfico
    plt.title(f"Distribuição de srcIP MiscAttack por Country - Month: {mes}")
    # Salvar a figura dentro da pasta com o nome do Month
    plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    i += 1
    # Fechar a figura para liberar memória
    plt.close()
