from argparse import ArgumentParser
import pandas as pd
import os
from data_processing import load_dataframe, process_groups, load_locations, generate_locations_dataframe

def main():
    parser = ArgumentParser()
    parser.add_argument('--filename', required=True)
    parser.add_argument('--print_result', action='store_true')
    args = parser.parse_args()
    
    filename = args.filename
    print_result = args.print_result
    
    print("Loading file...")
    df = load_dataframe(filename)
    print("File loaded.")
    
    data_file = 'csv/dados_srcIP_paises.csv'
    locations = load_locations(data_file)
    print("File used: ", data_file)
    
    print("\nProcessing groups...")
    locations_per_month = process_groups(df, locations)
    print("Groups processed.\n")

    df_locations = generate_locations_dataframe(locations_per_month)
    
    directory = 'csv/'
    output = 'locations_info.csv'
    df_locations.to_csv(os.path.join(directory, output), index=False)
    print("file ", output + " generated\n")
    
    if print_result:
        pd.set_option('display.max_columns', None)
        print(df_locations.head(5))
  
if __name__ == '__main__':
    main()
    # File created
    df_countries = pd.read_csv("csv/locations_info.csv")
    # Group by month and country, summing the number of occurrences and keeping the coordinates of the first city
    df_countries = df_countries.groupby(['Month', 'Country']).agg({'Occurrences': 'sum', 'Latitude': 'first', 'Longitude': 'first'}).reset_index()
    print(df_countries.head(10))
