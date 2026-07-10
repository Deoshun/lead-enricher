import json
import os
import sys
from lead.importer import load_leads
from qualify.qualifier import Qualify
from enrich.lead_enrich import Enrich
from enrich.utils import categorise_enriched_leads
from data_exporter.exporter import DataExporter

def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)

def load_ui_config(config):
    import tkinter as tk
    from tkinter import messagebox, filedialog
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Step 1: Select Leads Folder", "In the next window, please locate the folder containg leads.")
    config['raw_leads_dir'] = filedialog.askdirectory(title="Select raw leads")
    
    messagebox.showinfo("Step 2: Select Example Qualified Leads Folder", "To automate lead qualification, please locate the folder containg example qualified leads.")
    config['example_qualified_leads_dir'] = filedialog.askdirectory(title="Select example qualified leads")
    
    messagebox.showinfo("Step 3: Select Example Unqualified Leads Folder", "To automate lead qualification, please locate the folder containg example unqualified leads.")
    config['example_unqualified_leads_dir'] = filedialog.askdirectory(title="Select example unqualified")

    return config

def main():
    config = load_config()
    leads_config = '' 
    if config['interactive'] == 'True':
        config = load_ui_config(config)

    exporter = DataExporter(output_dir='exports')

    raw = load_leads(config['raw_leads_dir'])
    example_qualified = load_leads(config['example_qualified_leads_dir'])
    example_unqualified = load_leads(config['example_unqualified_leads_dir'])

    qualifier = Qualify({ 'good': example_qualified, 'bad': example_unqualified })
    
    qualified, unqualified = qualifier.qualify(raw, threshold=float(config['threshold']))

    print('Leads Qualified')
    print('Raw Leads')
    print(len(raw))
    print('Qualified Leads')
    print(len(qualified))
    print('Unqualified Leads')
    print(len(unqualified))

    enricher = Enrich()
    enriched_leads = enricher.enrich_leads(qualified)

    categorised_leads = categorise_enriched_leads(enriched_leads)

    for category in categorised_leads.keys():
        exporter.save(category, categorised_leads[category])

    exporter.save('unqualified', [x.to_dict() for x in unqualified])

if __name__ == "__main__":
    main()
