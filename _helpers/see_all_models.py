"""
This script lists all models available in the llmware Model Catalog
and exports the output to a CSV file. It also opens the file directly in
the Numbers application on a Mac for easy viewing.

Output:
- models_list.csv: A file containing all model details.
"""

import csv
import subprocess
from llmware.models import ModelCatalog

# Initialize Model Catalog instance
mc = ModelCatalog().list_all_models()

# Define the output file
output_file = "models_list.csv"

# Prepare data for export
# Assumes each model entry in `mc` is a dictionary or object with key attributes
with open(output_file, mode="w", newline='') as file:
    writer = csv.writer(file)
    
    # Write headers based on the first model's attributes
    headers = mc[0].keys() if isinstance(mc[0], dict) else ["model_name", "model_details"]
    writer.writerow(headers)
    
    # Write model details
    for model in mc:
        if isinstance(model, dict):
            writer.writerow(model.values())
        else:
            writer.writerow([model.name, model.details])

print(f"Model catalog exported to {output_file}")

# Open the CSV file in Numbers
subprocess.run(["open", "-a", "Numbers", output_file])
