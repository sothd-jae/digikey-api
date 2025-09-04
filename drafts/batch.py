import os
from pathlib import Path

import yaml

import digikey
from digikey.v4.productinformation import KeywordRequest
from digikey.v4.batchproductdetails import BatchProductDetailsRequest

CACHE_DIR = Path('path/to/cache/dir')
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

# Only if BatchProductDetails endpoint is explicitly enabled
# Search for Batch of Parts/Product
mpn_list = ["WP10-P002VA10-R15000",
"WP10-S002VA10-R15000",
"WP10-P004VA10-R15000",
"WP10-S004VA10-R15000",
"WP12-P006VA1-R15000",
"WP12-S006VA1-R15000",
"WP26DK-P010VA3-R15000",
"WP26DK-P016VA3-R15000",
"WP26DK-P024VA3-R15000",
"WP26DK-P030VA3-R15000",
"WP26DK-P034VA3-R15000",
"WP26DK-P040VA3-R15000",
"WP26DK-P050VA3-R15000",
"WP26DK-S010VA3-R15000",
"WP26DK-S016VA3-R15000",
"WP26DK-S024VA3-R15000",
"WP26DK-S030VA3-R15000",
"WP26DK-S034VA3-R15000",
"WP26DK-S040VA3-R15000",
"WP26DK-S050VA3-R15000",
"WP27D-P050VA3-R15000",
"WP55DK-P006VA1-R20000",
"WP55DK-P008VA1-R20000",
"WP55DK-P010VA1-R20000",
"WP55DK-P022VA1-R20000",
"WP55DK-S006VA1-R20000",
"WP55DK-S008VA1-R20000",
"WP55DK-S010VA1-R20000",
"WP55DK-S022VA1-R20000",
"WP56MS-P050VA1-R20000",
"WP56MS-S050VA1-R20000",
"WP66DK-P006VA1-R15000",
"WP66DK-S006VA1-R15000",
"WP86SD-P080VA1-R20000",
"WP86SD-S080VA1-R20000",
"WR-120S-VF-N1-R1500",
] #Length upto 50


def get_batch_product_details(part_numbers):
    """Fetch batch product details for a list of part numbers."""
    try:
        batch_request = BatchProductDetailsRequest(products=part_numbers)
        response = digikey.batch_product_details(body=batch_request)
        return response
    except Exception as e:
        print(f"Error fetching batch product details: {e}")
        return None
    

if __name__ == "__main__":
    batch_results = get_batch_product_details(["WP10-P002VA10-R15000", "WP10-S002VA10-R15000"])
    for i in batch_results:
        dkpn = i.part_number
        print(f"Part Number: {dkpn}")
        if i.description:
            print(f"Description: {i.description}")
        if i.manufacturer:
            print(f"Manufacturer: {i.manufacturer.name} (ID: {i.manufacturer.id})")
        with open(f"{dkpn}_search.yaml", "w") as f:
            yaml.dump(i.to_dict(), f, default_flow_style=False, sort_keys=False)
        print(f"Saved search results to {dkpn}_search.yaml")