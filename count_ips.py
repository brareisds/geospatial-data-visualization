import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt

parquet_file = 'deidentified.parquet'

# Carregar o arquivo parquet para um DataFrame
df = pd.read_parquet(parquet_file)
print("Arquivo lido")

# Converte a coluna 'date(mmddyyyy)' para o formato de data do pandas (datetime64). strfrime (String format time)
df['date(mmddyyyy)'] = pd.to_datetime(df['date(mmddyyyy)'], format='%m%d%Y')
df['Month'] = df['date(mmddyyyy)'].apply(lambda x: str(x.year) + "-" + str(x.month))
print("Coluna 'date(mmddyyyy)' convertida para o formato de data do pandas ")

df = df.query('Classification == "MiscAttack"')
qntd_ips_unicos = df['srcIP'].nunique()
print(f'Quantidade de srcIP unicos:', qntd_ips_unicos)

#df_filtrado = df[['srcIP', 'Month']]
num_meses = df['Month'].nunique()
print("Número de meses únicos:", num_meses)

# Agrupe os dados por 'Month'
grouped = df.groupby('Month')

# Use a função nunique() em cada grupo para contar a quantidade de endereços IP únicos
quantidade_ips_por_mes = grouped['srcIP'].count()

# Obter os meses e a quantidade de IPs
meses = quantidade_ips_por_mes.index
quantidade_ips = quantidade_ips_por_mes.values

plt.figure(figsize=(10, 6)) 

# Plot 1: Linha
#plt.subplot(2, 1, 1)  
plt.plot(meses, quantidade_ips, marker='o', linestyle='-', color='blue', label='Quantidade de IPs Únicos')
plt.title('Quantidade de Endereços IP Únicos por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de IPs Únicos')
plt.xticks(rotation=45)
plt.grid(True)  
plt.legend()
plt.savefig('grafico_linha_ips_unicos.png', format='png')
plt.show()

# Plot 2: Barra
#plt.subplot(2, 1, 2)
plt.figure(figsize=(10, 6)) 
plt.bar(meses, quantidade_ips, color='skyblue', label='Quantidade de IPs Únicos')
plt.title('Quantidade de Endereços IP Únicos por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de IPs Únicos')
plt.xticks(rotation=45)
plt.grid(axis='y')  
plt.legend()

plt.tight_layout()  
plt.savefig('grafico_barra_ips_unicos.png', format='png')
plt.show()
