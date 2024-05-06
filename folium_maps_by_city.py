import pandas as pd
import folium
import os

# Load the CSV file
df = pd.read_csv("csv/locations_info.csv")
#print(df)

center_latitude = 38.311646
center_longitude = 10.326697

# Iterate over each month in the DataFrame
for month in df['Month'].unique():
    df_month = df[df['Month'] == month]
    print(f'month: {month}')
    # Create a map for each month 
    map_center = [center_latitude, center_longitude]
    world_map = folium.Map(location=map_center, zoom_start=2, control_scale=True, tiles="cartodbpositron")

    # Iterate over each row of the DataFrame for the current month
    for index, row_month in df_month.iterrows():
        
        latitude = row_month['Latitude']
        longitude = row_month['Longitude']
        city = row_month['City']
        state = row_month['State']
        count = row_month['Occurrences']

        # Check if latitude, longitude, city, and state exist
        if not pd.isnull(latitude) and not pd.isnull(longitude) and city and state:
            circle_size = count 
            # Dynamic adjustment of circle size
            circle_size = max(min(circle_size, 50), 10)  # Limit circle size between 10 and 50
            # Add circle marker for each city
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=circle_size,
                fill=True,
                color='red',
                fill_color='red',
                fill_opacity=0.5,
                opacity=0.5,
                #tooltip=f'{city}: {count} IPs'  # Add city name and IP count as tooltip
            ).add_to(world_map)

            # Add the number of occurrences inside the circle
            folium.Marker(
                location=[latitude, longitude],
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(4,10),
                    html=f'<div style="font-size: 10pt; color : white; font-weight: bold">{count}</div>'
                )
            ).add_to(world_map)

            # Add the name of the city next to the circle
            folium.Marker(
                location=[latitude, longitude],  # Position next to the circle
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(-20,10),  # Adjustment to position next to the circle
                    html=f'<div style="font-size: 10pt; color : black; font-weight: bold">{city}</div>'
                )
            ).add_to(world_map)

    directory = 'folium-html/city/'
    # Save the map for each month
    world_map.save(os.path.join(directory, f"map{month}.html"))
