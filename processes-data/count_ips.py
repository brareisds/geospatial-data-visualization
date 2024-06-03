import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import ScalarFormatter
import os

df_srcIP = pd.read_csv('csv/locations_srcIP_info.csv')
df_dstIP = pd.read_csv('csv/locations_dstIP_info.csv')

df_srcIP = df_srcIP.groupby(['Month', 'Country']).agg({'Occurrences': 'sum'}).reset_index()
df_dstIP = df_dstIP.groupby(['Month', 'Country']).agg({'Occurrences': 'sum'}).reset_index()

# Agrupar os dados por 'Month' e somar as ocorrências
ocorrencias_por_mes_srcIP = df_srcIP.groupby('Month')['Occurrences'].sum()
ocorrencias_por_mes_dstIP = df_dstIP.groupby('Month')['Occurrences'].sum()

# Obter os meses e o número de ocorrências
months_srcIP = ocorrencias_por_mes_srcIP.index.tolist()
months_dstIP = ocorrencias_por_mes_dstIP.index.tolist()
quantidade_ocorrencias_srcIP = ocorrencias_por_mes_srcIP.values.tolist()
quantidade_ocorrencias_dstIP = ocorrencias_por_mes_dstIP.values.tolist()

# Custom sorting function to convert month-year string to datetime object
def custom_sort(month_year):
    return datetime.strptime(month_year, "%Y-%m")

# Sort the lists
sorted_month_year_list_srcIP = sorted(months_srcIP, key=custom_sort)
sorted_month_year_list_dstIP = sorted(months_dstIP, key=custom_sort)
sorted_quantidade_ocorrencias_srcIP = [quantidade_ocorrencias_srcIP[months_srcIP.index(month)] for month in sorted_month_year_list_srcIP]
sorted_quantidade_ocorrencias_dstIP = [quantidade_ocorrencias_dstIP[months_dstIP.index(month)] for month in sorted_month_year_list_dstIP]

# Criar subplots com proporções de altura especificadas
fig, ax = plt.subplots(1,1, figsize=(10, 6))



# # Plot para srcIP
# axes[0].bar(sorted_month_year_list_srcIP, sorted_quantidade_ocorrencias_srcIP, color='#FF7F7F', label='Total de Ocorrências srcIP por mês')
# axes[0].set_title('Total de Ocorrências srcIP por mês')
# axes[0].set_xlabel('Mês')
# axes[0].set_ylabel('Total de Ocorrências srcIP')
# axes[0].set_xticklabels(sorted_month_year_list_srcIP, rotation=45)
# axes[0].grid(axis='y')
# axes[0].legend()

# # Plot para dstIP
# axes[1].bar(sorted_month_year_list_dstIP, sorted_quantidade_ocorrencias_dstIP, color='skyblue', label='Total de Ocorrências dstIP por mês')
# axes[1].set_title('Total de Ocorrências dstIP por mês')
# axes[1].set_xlabel('Mês')
# axes[1].set_ylabel('Total de Ocorrências dstIP')
# axes[1].set_xticklabels(sorted_month_year_list_dstIP, rotation=45)
# axes[1].grid(axis='y')
# axes[1].legend()

# Plot para srcIP e dstIP juntos
ax.plot(sorted_month_year_list_srcIP, sorted_quantidade_ocorrencias_srcIP, color='#FF7F7F', label='Source IP Occurrences')
ax.plot(sorted_month_year_list_dstIP, sorted_quantidade_ocorrencias_dstIP, color='skyblue', label='Destination IP Occurrences')
ax.set_xlabel('Month')
ax.set_ylabel('Occurrences')
ax.set_title('Occurrences per Month')
ax.legend()
ax.grid(axis='y')
ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.set_xticklabels(sorted_month_year_list_srcIP, rotation=45)


ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
ax.yaxis.get_major_formatter().set_scientific(False)
ax.yaxis.get_major_formatter().set_useOffset(False)
custom_y_labels = [f'{int(y):,}' for y in ax.get_yticks()]
ax.set_yticklabels(custom_y_labels)

# Ajustar o layout
plt.tight_layout()

# Criar o diretório se ele não existir
output_dir = 'gpd-maps-images'
os.makedirs(output_dir, exist_ok=True)

# Caminho completo do arquivo
output_file = os.path.join(output_dir, 'combine_IPs_occurrences_per_month.png')

# Salvar o gráfico
plt.savefig(output_file)

# Mostrar o gráfico
plt.show()

