# gera o arquivo dados_srcIP_paises.csv contendo ip_fake, pais, estado, cidade, latitude, longitude de cada IP do arquivo didentified 

import geoip2.database
import pandas as pd
import csv

caminho_input = 'ips_ficticios.csv'
dbfile = "GeoLite2-City.mmdb"

# Função para obter a localização (cidade, estado, latitude, longitude) de um IP
# Se o IP não é encontrado no banco de dados retorna None
def getLocation(ip):
    with geoip2.database.Reader(dbfile) as reader:
        try:
            return reader.city(ip)
        except:
            return None

ips_invalidos = 0
total_ips = 0
paises_nulos = 0
estados_nulos = 0
cidades_nulas = 0
latitudes_nulas = 0
longitudes_nulas = 0

# Lista para armazenar os IPs nao encontrados no db
invalid_ips = []

print("Processando IPs...")
with open(caminho_input, 'r') as input:
    with open("dados_dstIP.csv", 'w', newline='') as output:
        escritor_csv = csv.writer(output)
        escritor_csv.writerow(['Fake_IP', 'Country', 'State', 'City', 'Latitude', 'Longitude'])

        primeira_linha = True
        for linha in input:
            # Pula a primeira linha 
            if primeira_linha:
                primeira_linha = False
                continue
            
            # Divide a linha em pares
            srcIp, ip_fake = linha.strip().split(';')

            # Retorna as informações geográficas do srcIP
            location = getLocation(srcIp)
            total_ips += 1

            # Verifica se o IP existe no banco de dados
            if not location:
                invalid_ips.append({
                    'IP_Invalido': srcIp
                })
                ips_invalidos += 1
                continue

            pais = location.country.name
            estado = location.subdivisions.most_specific.name
            cidade = location.city.name
            latitude = location.location.latitude
            longitude = location.location.longitude

            # Verifica valores nulos
            if not pais:
                paises_nulos += 1
            if not estado:
                estados_nulos += 1
            if not cidade:
                cidades_nulas += 1
            if not latitude:
                latitudes_nulas += 1
            if not longitude:
                longitudes_nulas += 1

            # Escreve no arquivo CSV se latitude e longitude estiverem presentes
            if latitude and longitude:
                escritor_csv.writerow((ip_fake, pais, estado, cidade, latitude, longitude))
print("IPs processados.")

if(len(invalid_ips) > 0):
    df_erros = pd.DataFrame(invalid_ips)
    output = 'ips_invalidos.csv'
    df_erros.to_csv(output, index=False)

print(f'\nTotal IPs: {total_ips}')
print(f'IPs não encontrados no banco de dados: {ips_invalidos} ({(ips_invalidos / total_ips) * 100:.2f}%)')
print(f'Paises nulos: {paises_nulos} ({(paises_nulos / total_ips) * 100:.2f}%)')
print(f'Estados nulos: {estados_nulos} ({(estados_nulos / total_ips) * 100:.2f}%)')
print(f'Cidades nulas: {cidades_nulas} ({(cidades_nulas / total_ips) * 100:.2f}%)')
print(f'Latitudes nulas: {latitudes_nulas} ({(latitudes_nulas / total_ips) * 100:.2f}%)')
print(f'Longitudes nulas: {longitudes_nulas} ({(longitudes_nulas / total_ips) * 100:.2f}%)')
