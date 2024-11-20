import os
import json
import django
from pathlib import Path

# Set up the base directory and configure Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Twins.settings')
django.setup()

from Home.models import Drinks

# Function to load data from JSON file
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print("SUCCESSFULLY LOADED DRINKS DATA")
    return data

# Function to generate the abbreviation (abv) for a drink
def generate_abv(brand_name):
    # Split the brand name into parts
    parts = brand_name.split()
    if len(parts) > 1:
        # First part is usually the brand, second part could be size
        brand_abv = ''.join([part[0].upper() for part in parts[:-1]])  # First letters of all words except size
        size = parts[-1]  # The size is typically the last word
        if size == "250ml":
            size_abv = "1/4"
        elif size == "350ml":
            size_abv = "1/2"
        elif size == "750ml":
            size_abv = "3/4"
        else:
            size_abv = ""
        return f"{brand_abv}{size_abv}"
    return brand_name[:3].upper()  # Default abbreviation for unknown names

# Function to add or update drinks in the database
def add_or_update_drinks(data_list):
    for item in data_list:
        # Unpack data for each drink, setting a default value if any field is missing
        name = item.get("brand")
        abv = generate_abv(name)  # Generate the abbreviation for the drink
        wholesale = item.get("buy", 0)  # Use 'buy' for the wholesale field
        cost = item.get("sell", 100)    # Default cost to 100 if 'sell' is missing
        opening_stock = item.get("opening_stock", 0)
        added_stock = item.get("added_stock", 0)
        sold_stock = item.get("sold_stock", 0)

        # Create or update the drink record
        drink, created = Drinks.objects.update_or_create(
            name=name,
            defaults={
                "abv": abv,  # Set the abbreviation
                "wholesale": wholesale,
                "cost": cost,
                "opening_stock": opening_stock,
                "added_stock": added_stock,
                "sold_stock": sold_stock,
                # `closing_stock` will be calculated automatically in the save() method
            }
        )

        if created:
            print(f"{name} added to the database.")
        else:
            print(f"{name} updated in the database.")

# Path to the JSON file
file_path = BASE_DIR / 'TheTwinsDjango-main' / 'drinks.json'

# Load data and populate the database
data = load_data_from_json(file_path)
add_or_update_drinks(data)
