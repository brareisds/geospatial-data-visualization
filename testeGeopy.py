import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
import os

# Carregar dados
df = pd.read_csv('csv/locations_teste.csv')

# Agrupar por mês e país
df_pais = df.groupby(['Mês', 'País']).agg({'Ocorrências': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Mapeamento de nomes de países
mapeamento_paises = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
   
}

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[['name', 'geometry']]


colors = [[255, 204, 204], [255, 153, 153], [255, 102, 102], [255, 51, 51], [255, 0, 0], [204, 0, 0], [153, 0, 0], [204, 0, 0], [51, 0, 0]]
colors_normalized = [[r/255, g/255, b/255] for r, g, b in colors]

print(colors_normalized)

sns.set_palette(colors_normalized)

i = 1

# Itera sobre cada mês no DataFrame
for mes in df_pais['Mês'].unique():
    df_mes = df_pais[df_pais['Mês'] == mes]

    # Atualiza os nomes dos países
    df_mes['País'] = df_mes['País'].map(mapeamento_paises).fillna(df_mes['País'])

    fig, ax = plt.subplots(1, 1, figsize = (10,10))

    patches = []
    ocorrencias = {}
    
    # Itera sobre as linhas do DataFrame para o mês atual
    for index, row_mes in df_mes.iterrows():
        pais = row_mes['País']
        count = row_mes['Ocorrências']

        # Plotar mapa do mundo
        world.boundary.plot(ax=ax, color="black", linewidth=0.5)

        # Calcular a cor com base nas ocorrências
        color_index = int((count / df_mes['Ocorrências'].max()) * (len(colors_normalized) - 1))
        print('color index: ', color_index)
        country_color = plt.cm.colors.to_rgba(colors_normalized[color_index], alpha=1.0)

        # Verificar se o país está presente no dataframe do mundo
        if pais in world["name"].values:
            country = world[world["name"] == pais]
            country.plot(ax=ax, color=country_color, alpha=1.0)

            print(f'{pais} adicionado')

            # generate a patch for the current continent
            # Adicionar patch para a legenda
            if count not in ocorrencias:
                patch = mpatches.Patch(color=country_color, label=f"{count} ocorrências")
                ocorrencias[count] = {'patch': patch, 'country_color': country_color}
        else:
            print('País não encontrado:', pais)

    # Inicializa um dicionário vazio para armazenar as ocorrências por cor
    ocorrencias_por_cor = {}

    # Percorra o dicionário de ocorrências
    for count, info in ocorrencias.items():
        # Acesse a cor associada a cada número de ocorrências
        country_color = info['country_color']
        
        # Adicione o número de ocorrências à lista correspondente à cor no dicionário ocorrencias_por_cor
        if country_color not in ocorrencias_por_cor:
            ocorrencias_por_cor[country_color] = [count]
        else:
            ocorrencias_por_cor[country_color].append(count)

    # Exiba o dicionário ocorrencias_por_cor
    print("Ocorrências por cor:")
    for color, counts in ocorrencias_por_cor.items():
        print(f"Cor: {color}")
        print("Counts:", counts)
        if( len(counts) > 1):
            patch = mpatches.Patch(color=color, label=f"{min(counts)}-{max(counts)} ocorrências")
        else:
            ocorrencia = counts[0]
            print(ocorrencia)
            if ocorrencia == 1:
                patch = mpatches.Patch(color=color, label=f"{ocorrencia} ocorrência")
            else:
                patch = mpatches.Patch(color=color, label=f"{ocorrencia} ocorrências")
        
        patches.append(patch)

    # Adicionar legenda
    # add the patches to the map
    ax.legend(handles=patches, loc="lower left", fontsize='small')
    # Desativar ticks do eixo
    ax.set_xticks([])
    ax.set_yticks([])
    directory = 'images/'
    # Definir título do gráfico
    plt.title(f"Distribuição de srcIP MiscAttack por país - Mês: {mes}")
    # Salvar a figura dentro da pasta com o nome do mês
    plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    i += 1
    # Fechar a figura para liberar memória
    plt.close()

