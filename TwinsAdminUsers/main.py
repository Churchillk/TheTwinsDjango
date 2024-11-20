import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Savannah.settings')
django.setup()

import json
from models import Provider, InpatientCharges
from django.db import IntegrityError

# Load JSON data from file
with open('C:/Users/Administrator/Desktop/CYN/Savannah/Data/data2/inpatient_2011.json', 'r') as file:
    json_data = json.load(file)

# Loop over each JSON entry and save it to the database
for entry in json_data:
    try:
        provider, created = Provider.objects.get_or_create(
            provider_id=entry["provider_id"],
            defaults={
                "provider_name": entry["provider_name"],
                "provider_street_address": entry["provider_street_address"],
                "provider_city": entry["provider_city"],
                "provider_state": entry["provider_state"],
                "provider_zipcode": int(entry["provider_zipcode"])
            }
        )

        # Create an InpatientCharges record
        InpatientCharges.objects.create(
            provider=provider,
            total_discharges=int(entry["total_discharges"]),
            average_covered_charges=float(entry["average_covered_charges"]),
            average_total_payments=float(entry["average_total_payments"]),
            average_medicare_payments=float(entry["average_medicare_payments"]),
            icd_category=entry["icd_category"],
            year="2011"
        )
        
    except IntegrityError as e:
        print(f"Integrity error for entry {entry['provider_id']}: {e}")
    except KeyError as e:
        print(f"Missing key in entry {entry}: {e}")
    except ValueError as e:
        print(f"Value error in entry {entry}: {e}")

print("Data import completed.")
