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


def process_files(directory_path):
    data_structure = {}

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('_traffic_incidents.csv'):
            read_and_store_content(file_path, data_structure)

    return data_structure

# Get the directory path relative to the script
script_dir = os.path.dirname(os.path.abspath(__file__))
relative_directory_path = './out'
directory_path = os.path.join(script_dir, relative_directory_path)

result_data_structure = process_files(directory_path)

json_output_file = 'out/processed/processed_data.json'
json_output = json.dumps(result_data_structure, indent=2, sort_keys=True)

with open(json_output_file, 'w') as json_file:
    json_file.write(json_output)

print(result_data_structure)