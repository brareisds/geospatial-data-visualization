import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import time

def csv_to_parquet(input_csv, output_parquet):
    # Carregar arquivo CSV para um DataFrame
    df = pd.read_csv(input_csv, sep=';')
    #Salvar o DataFrame como arquivo Parquet
    df.to_parquet(output_parquet, index=False)
    print("arquivo convertido com sucesso!")

csv_input_file = 'deidentified.csv'
parquet_output_file = 'deidentified.parquet'

def read_and_display_parquet(parquet_file):
    # Carregar o arquivo parquet para um DataFrame
    s_time_parquet = time.time()
    df = pd.read_parquet(parquet_file)
    e_time_parquet = time.time()

    # print("Lendo arquivo parquet: ", (e_time_parquet-s_time_parquet), "segundos")
    # print()

    # s_time_csv = time.time()
    # df = pd.read_csv('deidentified.csv', delimiter=';')
    # e_time_csv = time.time()

    # print("Lendo arquivo csv: ", (e_time_csv-s_time_csv), "segundos")
    # print()

    df['date(mmddyyyy)'] = pd.to_datetime(df['date(mmddyyyy)'], format='%m%d%Y')
    df = df.rename(columns={'date(mmddyyyy)': 'date(yyyy-mm-dd)'})
   
    #Exibir o conteúdo do data frame
    print("Conteúdo do arquivo parquet: ")
    print(df)

parquet_file = 'deidentified.parquet'

# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":
    # Se estiver sendo executado como o programa principal, o código abaixo será executado
    csv_to_parquet(csv_input_file,parquet_output_file)
    #read_and_display_parquet(parquet_file)
    #process_parquet(parquet_file)