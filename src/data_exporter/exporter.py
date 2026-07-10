import csv
import os

class DataExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, query, leads):
        """Saves leads as CSV file."""
        if not leads:
            print(f"No leads found for {query}. Skipping export.")
            return

        tag = f"{query.replace(' ', '_')}"
        file_path = os.path.join(self.output_dir, f"{tag}_output.csv")

        print(f"Saving {len(leads)} items to {file_path}")
        with open(file_path, "w", newline="", encoding="utf-8") as f:  
            title = leads[0].keys()
            cw = csv.DictWriter(f, title, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            cw.writeheader()
            cw.writerows(leads)
