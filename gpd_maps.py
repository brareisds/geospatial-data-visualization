import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import geopandas as gpd
import numpy as np
import pandas as pd
import imageio
import os

# Load data
df = pd.read_csv('csv/locations_info.csv')

# Group by month and country
df_country = df.groupby(['Month', 'Country']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Load world map
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Country name mapping
country_mapping = {
    'United States': 'United States of America',
    'The Netherlands': 'Netherlands'
}

colors_rgba = [
    [       1.0, 0.96078431, 0.92156863, 1.0],
    [0.99551821, 0.88963585, 0.78319328, 1.0],
    [0.99215686, 0.77759104, 0.57366947, 1.0],
    [0.99215686, 0.62689076, 0.34061625, 1.0],
    [0.96526611, 0.47226891, 0.14341737, 1.0],
    [0.87787115, 0.31932773, 0.02408964, 1.0],
    [0.67955182, 0.22184874, 0.01064426, 1.0],
    [0.49803922, 0.15294118, 0.01568627, 1.0]
]
# Crie uma paleta de cores personalizada usando as cores RGBA
custom_cmap = ListedColormap(colors_rgba)



# Create the images for each month
images = []

# Iterate over each month in the DataFrame
for month in df_country['Month'].unique():
    df_month = df_country[df_country['Month'] == month]

    # Update country names
    df_month['Country'] = df_month['Country'].map(country_mapping).fillna(df_month['Country'])

    fig, ax = plt.subplots(figsize=(10, 10))

    # Merge the world and df_month DataFrames based on the country name
    merged_df = pd.merge(world, df_month, left_on='name', right_on='Country', how='left')

    # Fill NaN values in the 'occurrences' column with corresponding values from the merged_df DataFrame
    world['occurrences'] = merged_df['Occurrences'].fillna(0)
    # Remove unnecessary columns from the world DataFrame
    world.drop(columns=['Country', 'Month', 'Latitude', 'Longitude'], inplace=True, errors='ignore')

    if( world['occurrences'].max() < 100):
        # Group the occurrences into bins for legend
        bins = np.linspace(world['occurrences'].min(), world['occurrences'].max(), 3)  # Define 5 bins
        world['occurrences_group'] = np.digitize(world['occurrences'], bins, right=True)
        k = 2
    elif( world['occurrences'].max() < 200):
        # Group the occurrences into bins for legend
        bins = np.linspace(world['occurrences'].min(), world['occurrences'].max(), 4)  # Define 5 bins
        world['occurrences_group'] = np.digitize(world['occurrences'], bins, right=True)
        k = 3
    elif( world['occurrences'].max() < 300):
        # Group the occurrences into bins for legend
        bins = np.linspace(world['occurrences'].min(), world['occurrences'].max(), 5)  # Define 5 bins
        world['occurrences_group'] = np.digitize(world['occurrences'], bins, right=True)
        k = 4
    else:
        # Group the occurrences into bins for legend
        bins = np.linspace(world['occurrences'].min(), world['occurrences'].max(), 6)  # Define 5 bins
        world['occurrences_group'] = np.digitize(world['occurrences'], bins, right=True)
        k = 5

    #Plot the map
    # Configurar a legenda manualmente com os limites dos bins
    legend_labels = []
    for i in range(len(bins)-1):
        legend_labels.append(f"{bins[i]:.0f} - {bins[i+1]:.0f}")

    #print(legend_labels) #saida: ['0 - 7736', '7736 - 15473', '15473 - 23209', '23209 - 30946', '30946 - 38682']

    world.plot(ax=ax, column='occurrences', missing_kwds={'color': 'lightgrey'}, legend=True, scheme="quantiles", legend_kwds={"loc": "lower left", "fmt": "{:.0f}", "title": "Occurrences", 'labels':legend_labels, 'facecolor': 'DarkGray'}, cmap=custom_cmap, edgecolor='black', linewidth=0.1, k=k)
    ax.set_facecolor('Gainsboro')

    # Remover a última entrada da legenda
    
    #leg = ax.get_legend()

    #leg.set_bbox_to_anchor((1.17,0.5))
    #ax.set_axis_off()

    # Turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(f'Number of srcIP - MiscAttack in {month}')
    # ax.set_axis_off()
    # plt.tight_layout()
    directory = 'gpd-maps-images/'
    # plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
    plt.savefig(os.path.join(directory, f'srcIPs_{month}.png'), dpi=150)
    plt.close()

    images.append(imageio.imread(f'gpd-maps-images/srcIPs_{month}.png'))

# Save the images as a gif
imageio.mimsave(os.path.join(directory, 'srcIPs.gif'), images, fps=1)

