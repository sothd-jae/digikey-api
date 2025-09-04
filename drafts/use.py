import os
from pathlib import Path
CACHE_DIR = Path('/workspaces/digikey-api/.digikey_cache')
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

import digikey
from digikey.v3.productinformation import KeywordSearchRequest
from digikey.v3.batchproductdetails import BatchProductDetailsRequest

# Query product number
dkpn = '296-6501-1-ND'
part = digikey.product_details(dkpn)
print(part)

# Search for parts
search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
#result = digikey.keyword_search(body=search_request)

# Only if BatchProductDetails endpoint is explicitly enabled
# Search for Batch of Parts/Product
mpn_list = ["0ZCK0050FF2E", "LR1F1K0"] #Length upto 50
batch_request = BatchProductDetailsRequest(products=mpn_list)
#part_results = digikey.batch_product_details(body=batch_request)