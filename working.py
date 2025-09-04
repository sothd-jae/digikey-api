import os
from pathlib import Path

import digikey
from digikey.v4.productinformation import KeywordRequest
from digikey.v4.productinformation.models import FilterOptionsRequest, ParameterFilterRequest

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
os.environ['DIGIKEY_REDIRECT_URI'] ='https://urban-invention-q7xg6p774p6vhx5j-8139.app.github.dev/digikey_callback'

'''
1. Get part information by part number
2. Use category to get parameters
3. Select parameters by category
4. Search parts using parameters
5. Record results
'''

def cat_search(part_info,keys=None,lim=10,offs=0,fil=None,sort=None):
    parameter_filters = []
    for i in part_info['Parameters']:
        if i.get("parameter_id") in PARAMS_BY_CAT.get(part_info['Category']['category_id'], []):
            parameter_filters.append({
                "ParameterId": i.get("parameter_id"),
                "FilterValues": [{"Id":i.get("value_id")}]
            })
    fil = FilterOptionsRequest(
        parameter_filter_request=ParameterFilterRequest(
            category_filter={"Id": str(part_info['Category']['category_id'])},
            parameter_filters=parameter_filters
        )
    )
    search_request = KeywordRequest(keywords=keys, limit=lim, offset=offs, filter_options_request=fil, sort_options=sort)
    result = digikey.keyword_search(body=search_request)
    return result

PARAMS_BY_CAT = {308: [88]} # Number of pins for rectangular connectors

if __name__ == "__main__":
    import part_info
    cat = cat_search(part_info.part_info)
    for p in cat.products:
        print(p.manufacturer_product_number)

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