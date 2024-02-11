import os
import csv
import json
from datetime import datetime

def parse_file_name(file_name):
    parts = file_name.split('_')
    date_str, time_str = parts[0], parts[1]
    date_time_str = f"{date_str}_{time_str}"
    date_time = datetime.strptime(date_time_str, '%Y%m%d_%H%M')
    return date_time

def parse_csv_content(content):
    desired_columns = ['codEle', 'alias', 'provincia', 'poblacion']

    parsed_data = []
    reader = csv.DictReader(content.splitlines())
    
    for row in reader:
        parsed_row = {col: row[col] for col in desired_columns}
        parsed_data.append(parsed_row)

    return parsed_data

def parse_csv_content_graphext(content):
    desired_columns = ['codEle', 'alias', 'autonomia', 'provincia', 'poblacion', 'fecha', 'hora', 'sentido', 'descripcion', 'fechaFin', 'lng', 'lat', 'pkIni', 'pkFinal', 'causa', 'carretera', 'estado', 'tipo' ]
    
    parsed_data = []
    reader = csv.DictReader(content.splitlines())
    
    for row in reader:
        parsed_row = {col: row[col] for col in desired_columns}
        parsed_data.append(parsed_row)
    
    return parsed_data

def read_and_store_content(file_path, data_structure):
    with open(file_path, 'r') as file:
        content = file.read()

    parsed_data = parse_csv_content(content)
    
    date_time = parse_file_name(os.path.basename(file_path))
    date_key = date_time.strftime('%Y%m%d')
    hour_key = date_time.strftime('%H')

    if date_key not in data_structure:
        data_structure[date_key] = {}
    
    if hour_key not in data_structure[date_key]:
        data_structure[date_key][hour_key] = []

    data_structure[date_key][hour_key].extend(parsed_data)

def read_and_store_content_graphext(file_path, data_structure_graphext):
    with open(file_path, 'r') as file:
        content = file.read()

    parsed_data_graphext = parse_csv_content_graphext(content)

    # Filter out elements from the new list that are already present in the original list
    filtered_new_list = [item for item in parsed_data_graphext if item['codEle'] not in {obj['codEle'] for obj in data_structure_graphext}]

    data_structure_graphext.extend(filtered_new_list)


def process_files(directory_path):
    data_structure = {}

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('_traffic_incidents.csv'):
            read_and_store_content(file_path, data_structure)

    return data_structure

def process_files_graphext(directory_path):
    data_structure_graphext = []

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('_traffic_incidents.csv'):
            read_and_store_content_graphext(file_path, data_structure_graphext)

    return data_structure_graphext

script_dir = os.path.dirname(os.path.abspath(__file__))
relative_directory_path = './out/all'
directory_path = os.path.join(script_dir, relative_directory_path)

result_data_structure = process_files(directory_path)
json_output_file = 'out/processed/processed_data.json'
json_output = json.dumps(result_data_structure, indent=2, sort_keys=True)
with open(json_output_file, 'w') as json_file:
    json_file.write(json_output)

result_data_structure_graphext = process_files_graphext(directory_path)
json_output_file_graphext = 'out/processed/processed_data_graphext.json'
json_output_graphext = json.dumps(result_data_structure_graphext, indent=2, sort_keys=True)
with open(json_output_file_graphext, 'w') as json_file:
    json_file.write(json_output_graphext)

print(result_data_structure)