from PIL import Image
import imageio
import pandas as pd
import os
from datetime import datetime

# Load data
df = pd.read_csv('csv/locations_srcIP_info.csv')

df_brazil = df[df['Country'] == "Brazil"]
# Group by month and country
df_state_brazil = df_brazil.groupby(['Month', 'State']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()

# Diretórios dos GIFs
src_ips_gif_dir = 'gpd-maps-images/srcIPs/brazil-states/'
dst_ips_gif_dir = 'gpd-maps-images/dstIPs/brazil-states/'

# Diretório para salvar o GIF combinado
combined_gif_dir = 'gpd-maps-images/combined/'

# Criar o diretório se não existir
os.makedirs(combined_gif_dir, exist_ok=True)

months = []
# Iterar sobre cada mês no DataFrame
for _, month in enumerate(df_state_brazil['Month'].unique(), start=1):
    months.append(month)

# Custom sorting function to convert month-year string to datetime object
def custom_sort(month_year):
    return datetime.strptime(month_year, "%Y-%m")

# Sort the list
sorted_month_year_list = sorted(months, key=custom_sort)


# Iterar sobre cada mês
for month in sorted_month_year_list:
    # Abrir as imagens correspondentes para srcIPs e dstIPs
    src_ips_image = Image.open(os.path.join(src_ips_gif_dir, f'state_srcIPs_{month}.png'))
    dst_ips_image = Image.open(os.path.join(dst_ips_gif_dir, f'state_dstIPs_{month}.png'))

    # Cria uma nova imagem vazia com a largura total sendo a soma das larguras das imagens src_ips_image e dst_ips_image combinando as imagens horizontalmente 
    combined_image = Image.new('RGB', (src_ips_image.width + dst_ips_image.width, src_ips_image.height))
    # Cola a imagem src_ips_image na imagem combinada (combined_image) na posição (0, 0), que é o canto superior esquerdo.
    combined_image.paste(src_ips_image, (0, 0))
    # Cola a imagem dst_ips_image na imagem combinada (combined_image) na posição (src_ips_image.width, 0), ou seja, exatamente ao lado direito da imagem src_ips_image
    combined_image.paste(dst_ips_image, (src_ips_image.width, 0))

    # Salvar a imagem combinada
    combined_image.save(os.path.join(combined_gif_dir, f'combined_{month}.png'))

# Criar o GIF combinado
images_combined = [imageio.imread(os.path.join(combined_gif_dir, f'combined_{month}.png')) for month in sorted_month_year_list]
imageio.mimsave(os.path.join(combined_gif_dir, 'combined.gif'), images_combined, fps=1)


