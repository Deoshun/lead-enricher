import pandas as pd
import os
import json
from lead.lead import Lead

def load_import_config(file_path='column_name_config.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)

def convert_df_to_leads(data):
    import_config = load_import_config()
    name_key = import_config['company_name']
    address_key = import_config['address']
    types_key = import_config['types']
    phone_key = import_config['phone']
    website_key = import_config['website']

    A = [
        Lead(
            getattr(row, name_key),
            getattr(row, address_key), 
            getattr(row, types_key), 
            getattr(row, phone_key),
            getattr(row, website_key)
        ) for row in data.itertuples()
    ]
    return A

def load_leads(path):
    leads = []
    files = os.listdir(path)
    files_excel = [f for f in files if f[-3:] in ['xls', 'ods']]
    files_csv = [f for f in files if f[-3:] == 'csv']
    df = pd.DataFrame()
    for f in files_excel:
        f = path + '/' + f
        data = pd.read_excel(f, 'Sheet1')
        df = pd.concat([df, data], ignore_index=True)

    for f in files_csv:
        f = path + '/' + f
        data = pd.read_csv(f)
        df = pd.concat([df, data], ignore_index=True)

    leads += convert_df_to_leads(df)
    return leads
