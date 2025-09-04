import os
import json
from pathlib import Path
import digikey
import warnings
import sys
import atexit

CACHE_DIR = Path('/workspaces/digikey-api/.digikey_cache')
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

TEST_PART_NUMBERS = [
    '670-2962-2-ND',  # Example part number
    # Add more part numbers for broader testing
]


def get_digikey_substitutions(dkpn):
    """Fetch part substitutions from Digikey API v4."""
    try:
        response = digikey.product_substitute(dkpn)
        if response:
            print(f"Substitutions for {dkpn}:")
            for suggestion in response.get('RecommendedProducts', []):
                print(f"- {suggestion.get('ProductDescription', 'No description available')}")
                print(f"  Product Number: {suggestion.get('DigiKeyProductNumber', 'N/A')}")
                print(f"  Manufacturer: {suggestion.get('ManufacturerName', 'N/A')}")
            return response
        else:
            print(f"No recommendations found for {dkpn}.")
            return None
    except Exception as e:
        print(f"Error fetching recommendations for {dkpn}: {e}")
        return None

def suppress_exit_errors():
    if sys.exc_info()[0] is not None:
        return
    warnings.filterwarnings("ignore")
atexit.register(suppress_exit_errors)

if __name__ == "__main__":
    for part_number in TEST_PART_NUMBERS:
        print(f"Testing part number: {part_number}")
        get_digikey_substitutions(part_number)