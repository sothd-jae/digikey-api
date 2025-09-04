import os
from pathlib import Path

import digikey
from digikey.v4.productinformation import KeywordRequest
from digikey.v4.productinformation.models import FilterOptionsRequest

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

digikey_logger = logging.getLogger('digikey')
digikey_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
digikey_logger.addHandler(handler)

CACHE_DIR = Path('/workspaces/digikey-api/.digikey_cache')

os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

# Query product number
def query_dkpn(dkpn):
    part = digikey.product_details(dkpn)
    return part

# Search for parts
def search_parts(keywords, limit=10, offset=0):
    search_request = KeywordRequest(keywords=keywords, limit=limit, offset=offset)
    result = digikey.keyword_search(body=search_request)
    return result

def get_dk_info(jae_pn):
# Get digi-key part number, category, and params for JAE p/n
    jae_part_number = jae_pn
    try:
        part_info = search_parts(jae_part_number)
        dkpn = part_info.exact_matches[0].product_variations[0].digi_key_product_number
        category = part_info.exact_matches[0].category
        # Grab most specific category id
        while category.child_categories != []:
            category = category.child_categories[0]
        params = part_info.exact_matches[0].parameters
        # Create stored data structure
        item = {
            'Manufacturer': 'JAE Electronics',
            'Part Number': jae_part_number,
            'Digi-Key Part Number': dkpn,
            'Category': category.category_id,
            'Parameters': params
        }
        # Write to py object
        with open('part_info.py', 'w') as f:
            f.write(f"part_info = {item}")
    except Exception as e:
        logger.error(f"Error querying part number {jae_part_number}: {e}")

def run_get_jae_info():
    # Read from snap_data.csv
    with open('snap_data.csv', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(',')
            if len(parts) >= 2:
                jae_pn = parts[1].strip()
                get_dk_info(jae_pn)

if __name__ == "__main__":
    
    # Example usage
    part_number = "WP10-P002VA10-R15000"
    """ try:
        part_info = query_dkpn(part_number)
        print(f"Part Info for {part_number}: {part_info}")
    except Exception as e:
        logger.error(f"Error querying part number {part_number}: {e}")
 """
    # Example search
    keywords = "resistor"
    """  try:
        search_results = search_parts(keywords)
        print(f"Search Results for '{keywords}': {search_results}")
    except Exception as e:
        logger.error(f"Error searching for '{keywords}': {e}") 
    """
    part_numbers = [
        "WP10-P002VA10-R15000",
        "WP10-S002VA10-R15000"  # Example part number
    ]
    """ try:
        batch_results = search_batch_parts(part_numbers)
        print(f"Batch Results for {part_numbers}: {batch_results}")
    except Exception as e:
        logger.error(f"Error searching batch parts {part_numbers}: {e}")
    Error searching batch parts ['WP10-P002VA10-R15000', 'WP10-S002VA10-R15000']: BatchSearchApi.batch_product_details_with_http_info() got multiple values for argument 'authorization'     """
