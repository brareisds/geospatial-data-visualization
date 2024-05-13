import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import geopandas as gpd
import pandas as pd
import imageio
import os
from datetime import datetime
import matplotlib.patches as mpatches

# Load data
df = pd.read_csv('csv/locations_dstIP_info.csv')

# Group by month and country
df_country = df.groupby(['Month', 'Country']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Load world map
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Country name mapping
country_mapping = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
}
#paleta de cores dstIP
colors_hex = ['#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b']

# paleta de cores srcIP
# colors_hex = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']
# Crie uma paleta de cores personalizada usando as cores RGBA
custom_cmap = ListedColormap(colors_hex)

# Create the images for each month
images = []
months = []

# Iterate over each month in the DataFrame
for month in df_country['Month'].unique():
    df_month = df_country[df_country['Month'] == month]
  
    
    # Update country names
    df_month['Country'] = df_month['Country'].map(country_mapping).fillna(df_month['Country'])

    fig, ax = plt.subplots(figsize=(20, 15))

    # Merge the world and df_month DataFrames based on the country name
    merged_df = pd.merge(world, df_month, left_on='name', right_on='Country', how='left')

    # Fill NaN values in the 'occurrences' column with corresponding values from the merged_df DataFrame
    world['occurrences'] = merged_df['Occurrences']

    # Remove unnecessary columns from the world DataFrame
    world.drop(columns=['Country', 'Month', 'Latitude', 'Longitude'], inplace=True, errors='ignore')

    ax = world.plot(column='occurrences', missing_kwds={'color': 'lightgrey'}, legend=True, cmap=custom_cmap, edgecolor='white',legend_kwds= {'shrink': 0.5}, ax=ax, linewidth=0.1, k = 7)
    #ax.set_facecolor('Gainsboro')
    ax.set_axis_off()
    fig = ax.figure
    cb_ax = fig.axes[1] 
    cb_ax.tick_params(labelsize=15, left=False, labelleft=False, bottom=False)
    

    NaN = mpatches.Patch(color='lightgrey', label='No occurrences')
    plt.legend(handles=[NaN], fontsize=15,bbox_to_anchor=(1, 1))
    leg2 = plt.legend(handles=[NaN], 
                  fontsize=15,   # set font size
                  mode="expand",      # allow `bbox_to_anchor` to set position/size
                  bbox_to_anchor=(0.15, 0.80, 0.75, 0.2))
    # fontsize: 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    # bbox_to_anchor: (x, y, width, height)

    # make use of the legend's handle, leg2
    leg2.get_frame().set_edgecolor('none')  # remove edge line

    # Mostre o gráfico
    #plt.colorbar(ax=ax, orientation='vertical', fraction=0.04, pad=0.02)
    
    
    
    # Mostre o gráfico
    # legend = ax.get_legend()
    # legend.set_bbox_to_anchor((1, 1))  # ajuste as coordenadas conforme necessário
    # legend.set_title('Occurrences')
    #leg.set_fontsize(16)
    # Set font size for legend

    # Turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)

    ax.set_title(f'Number of dstIP in {month}', fontsize=20)
    
    # ax.set_axis_off()
    # plt.tight_layout()
    directory = 'gpd-maps-images/dstIPs/comp_by_month/'
    # plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    plt.savefig(os.path.join(directory, f'dstIPs_{month}.png'), dpi=150)
    plt.close()

    months.append(month)

# Custom sorting function to convert month-year string to datetime object
def custom_sort(month_year):
    return datetime.strptime(month_year, "%Y-%m")

# Sort the list
sorted_month_year_list = sorted(months, key=custom_sort)

# Iterar sobre cada mês no DataFrame
for month in sorted_month_year_list:
    images.append(imageio.imread(f'{directory}dstIPs_{month}.png'))

# Salvar as imagens ordenadas como GIF
imageio.mimsave(os.path.join(directory, 'dstIPs_comp_month.gif'), images, fps=1)

