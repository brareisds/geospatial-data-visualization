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
# Create a custom color map using the RGBA colors
custom_cmap = ListedColormap(colors_rgba)

# Determine bins for all months
max_occurrences = df_country['Occurrences'].max()
if max_occurrences < 100:
    num_bins = 3
elif max_occurrences < 200:
    num_bins = 4
elif max_occurrences < 300:
    num_bins = 5
else:
    num_bins = 6

bins = np.linspace(0, max_occurrences, num_bins + 1)

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

    # Group the occurrences into bins for legend
    world['occurrences_group'] = np.digitize(world['occurrences'], bins, right=True)

    # Plot the map
    world.plot(ax=ax, column='occurrences', missing_kwds={'color': 'lightgrey'}, legend=True, scheme="quantiles", legend_kwds={"loc": "lower left", "fmt": "{:.0f}", "title": "Occurrences", 'facecolor': 'DarkGray'}, cmap=custom_cmap, edgecolor='black', linewidth=0.1, k=num_bins)
    ax.set_facecolor('Gainsboro')

    # Turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(f'Number of srcIP - MiscAttack in {month}')

    directory = 'gpd-maps-images/'
    plt.savefig(os.path.join(directory, f'srcIPs_{month}.png'), dpi=150)
    plt.close()

    images.append(imageio.imread(f'gpd-maps-images/srcIPs_{month}.png'))

# Save the images as a gif
imageio.mimsave(os.path.join(directory, 'srcIPs.gif'), images, fps=1)
