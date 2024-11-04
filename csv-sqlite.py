import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Savannah.settings')  # Replace 'yourproject' with your project name
django.setup()

import csv
from django.core.exceptions import ObjectDoesNotExist
import random, string
from Home.models import Drinks  # Replace 'yourapp' with your actual app name

# File path to the CSV file
file_path = 'E:\thebag\mine\Twins\sheet.csv'  # Replace with the actual path to your CSV file

# Helper function to generate a random alphanumeric provider ID
def generate_unique_provider_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Open the CSV file and read each row
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    print("CSV Headers:", reader.fieldnames)  # This will print the headers
    for row in reader:
        print(row)
        HospitalGeneralInfo.objects.create(
            provider=provider_id,
            hospital_name=row['hospital_name'],
            street_address=row['address'],
            city=row['city'],
            state=row['state'],
            zipcode=int(row['zip_code']),
            mortality_group_measure_count=(row['mortality_group_measure_count']),
            facility_mortality_measures_count=row['facility_mortaility_measures_count'],
        )

        print(f"Successfully added {row['hospital_name']} with Provider ID {provider_id}")

print("Data import complete.")