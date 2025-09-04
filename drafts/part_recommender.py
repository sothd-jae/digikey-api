import os
from pathlib import Path
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

CACHE_DIR = Path('/workspaces/digikey-api/.digikey_cache')
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)


def get_part_schemas(dkpn):
    """Fetch part schemas from Digikey API."""
    part = digikey.product_details(dkpn)
    
    
    return part


def get_part_details(dkpn):
    """Fetch part details from Digikey API."""
    part = digikey.product_details(dkpn)
    print("Fetched part details:")
    print(part)
    return part


def extract_key_attributes(part):
    """Parse part data and extract key attributes for similarity search."""
    attributes = {}
    # Example: category, manufacturer, part type, value, tolerance, package, voltage, current
    attributes['category'] = getattr(part, 'category', None)
    attributes['manufacturer'] = getattr(part, 'manufacturer', None)
    attributes['part_type'] = getattr(part, 'type', None)
    # Try to extract value (resistance, capacitance, etc.)
    for key in ['resistance', 'capacitance', 'inductance', 'value']:
        if hasattr(part, key):
            attributes[key] = getattr(part, key)
            break
    # Tolerance
    if hasattr(part, 'tolerance'):
        attributes['tolerance'] = part.tolerance
    # Package
    for key in ['package', 'case', 'mounting_type']:
        if hasattr(part, key):
            attributes[key] = getattr(part, key)
            break
    # Voltage
    if hasattr(part, 'voltage_rating'):
        attributes['voltage_rating'] = part.voltage_rating
    # Current
    if hasattr(part, 'current_rating'):
        attributes['current_rating'] = part.current_rating
    # Print extracted attributes
    print("Extracted key attributes for similarity:")
    for k, v in attributes.items():
        print(f"  {k}: {v}")
    return attributes


def find_similar_parts(attributes):
    """Search for similar parts using Digikey API."""
    # Build a keyword search from attributes
    keywords = ' '.join(str(v) for v in attributes.values() if v)
    search_request = KeywordSearchRequest(keywords=keywords, record_count=10)
    result = digikey.keyword_search(body=search_request)
    print("Found similar parts:")
    for idx, part in enumerate(result.parts[:5]):
        print(f"{idx+1}. {part.manufacturer_part_number} - Popularity: {getattr(part, 'popularity', 'N/A')}")
    return result.parts[:5]


def main():
    dkpn = '670-2962-2-ND'
    part = get_part_details(dkpn)
    attributes = extract_key_attributes(part)
    similar_parts = find_similar_parts(attributes)
    print("\nReasoning:")
    print(f"Selected attributes: {attributes}")
    print("Parts ranked by popularity (if available in API data).")

if __name__ == "__main__":
    main()
