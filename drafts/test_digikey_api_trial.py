import os
import json
from pathlib import Path
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

CACHE_DIR = Path('/workspaces/digikey-api/.digikey_cache')
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

TEST_PART_NUMBERS = [
    '670-2962-2-ND',  # Example part number
    # Add more part numbers for broader testing
]

def get_deepest_child_category(category):
    """Recursively find the deepest child category with a name."""
    while category.get('child_categories'):
        category = category['child_categories'][0]
    return category.get('name')

def get_filter_parameters(part, param_names):
    """Extract parameter values from the part's parameters list."""
    params = {}
    for param in getattr(part, 'parameters', []):
        if param.get('parameter_text') in param_names:
            params[param['parameter_text']] = param.get('value_text')
    return params

def test_part_details(dkpn):
    print(f"\nTesting part details for: {dkpn}")
    try:
        part = digikey.product_details(dkpn)
    except Exception as e:
        print(f"Error fetching part details: {e}")
        return None
    # Example: get deepest child category and filter parameters
    category = getattr(part, 'category', None)
    if category:
        deepest_category = get_deepest_child_category(category)
        print("Deepest child category:", deepest_category)
    else:
        deepest_category = None
    filter_params = get_filter_parameters(part, ['Connector Type', 'Pitch', 'Mounting Type'])
    print("Filter parameters:", filter_params)
    # Optionally, build a search string and call keyword search
    if deepest_category:
        keywords = deepest_category + ' ' + ' '.join(filter_params.values())
        print("Search keywords:", keywords)
        search_request = KeywordSearchRequest(keywords=keywords, record_count=5)
        try:
            result = digikey.keyword_search(body=search_request)
            print("Found similar parts:")
            for idx, part in enumerate(result.parts):
                print(f"{idx+1}. {getattr(part, 'manufacturer_part_number', 'N/A')} - Popularity: {getattr(part, 'popularity', 'N/A')}")
            return part
        except Exception as e:
            print(f"Error in keyword search: {e}")
    return part

def extract_category_and_parameters(part):
    """Find and print categories and parameters matching user criteria."""
    categories = getattr(part, '_child_categories', [])
    for cat in categories:
        name = cat.get('_name')
        if name == "Arrays, Edge Type, Mezzanine (Board to Board)":
            print(f"Matched category: {name}")
            parameters = cat.get('_parameters', [])
            for param in parameters:
                if param.get('_parameter_text') == "Connector Type" and param.get('_value_text') == "Receptacle, Center Strip Contacts":
                    print(f"Matched parameter: {param}")

def test_keyword_search(attributes):
    print("\nTesting keyword search with attributes:")
    print(attributes)
    keywords = ' '.join(str(v) for v in attributes.values() if v)
    search_request = KeywordSearchRequest(keywords=keywords, record_count=5)
    try:
        result = digikey.keyword_search(body=search_request)
        print("Found similar parts:")
        for idx, part in enumerate(result.parts):
            print(f"{idx+1}. {getattr(part, 'manufacturer_part_number', 'N/A')} - Popularity: {getattr(part, 'popularity', 'N/A')}")
        return result.parts
    except Exception as e:
        print(f"Error in keyword search: {e}")
        return []

def extract_key_attributes(part):
    attributes = {}
    attributes['category'] = getattr(part, 'category', None)
    attributes['manufacturer'] = getattr(part, 'manufacturer', None)
    attributes['part_type'] = getattr(part, 'type', None)
    for key in ['resistance', 'capacitance', 'inductance', 'value']:
        if hasattr(part, key):
            attributes[key] = getattr(part, key)
            break
    if hasattr(part, 'tolerance'):
        attributes['tolerance'] = part.tolerance
    for key in ['package', 'case', 'mounting_type']:
        if hasattr(part, key):
            attributes[key] = getattr(part, key)
            break
    if hasattr(part, 'voltage_rating'):
        attributes['voltage_rating'] = part.voltage_rating
    if hasattr(part, 'current_rating'):
        attributes['current_rating'] = part.current_rating
    return attributes

def run_tests():
    for dkpn in TEST_PART_NUMBERS:
        part = test_part_details(dkpn)
        #if part:
            #attributes = extract_key_attributes(part)
            #test_keyword_search(attributes)

if __name__ == "__main__":
    run_tests()
