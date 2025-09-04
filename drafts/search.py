
import yaml
import os
import warnings
import digikey
from pathlib import Path
from digikey.v4.productinformation import KeywordRequest, ProductDetails
from digikey.v4.productinformation.models import FilterOptionsRequest, ParameterFilterRequest

CACHE_DIR = Path(os.environ.get('DIGIKEY_CACHE_DIR', '/workspaces/digikey-api/.digikey_cache'))
os.environ['DIGIKEY_STORAGE_PATH'] = str(CACHE_DIR)

TEST_PART_NUMBERS = [
    "WP10-P002VA10-R15000",
    "WP10-S002VA10-R15000"  # Example part number
    # Add more part numbers for broader testing
]



def get_parametric_search(category_id=308, parameters=None):
    """Search for products in category_id with parameters."""
    try:
        # Example values, adjust as needed
        keywords = ""
        limit = 50
        offset = 0
        manufacturer_filter = []
        category_filter = [{"Id": str(category_id)}]
        status_filter = []
        packaging_filter = []
        #marketplace_filter = "NoFilter"
        #tariff_filter = "None"
        series_filter = []
        minimum_quantity_available = 0
        parameter_filters = []
        for i in parameters:
            parameter_filters.append({
                "ParameterId": i.get("id"),
                "FilterValues": [{"Id": str(v)} for v in i.get("values", [])]
            })
        parameter_filter_request = ParameterFilterRequest(
            category_filter={"Id": str(category_id)},
            parameter_filters=parameter_filters
        )
        search_options = []
        sort_options = {"Field": "None", "SortOrder": "Ascending"}

        # Build FilterOptionsRequest
        filter_options_request = FilterOptionsRequest(
            manufacturer_filter=manufacturer_filter,
            category_filter=category_filter,
            status_filter=status_filter,
            packaging_filter=packaging_filter,
            #marketplace_filter=marketplace_filter,
            #tariff_filter=tariff_filter,
            series_filter=series_filter,
            minimum_quantity_available=minimum_quantity_available,
            parameter_filter_request=parameter_filter_request,
            search_options=search_options
        )

        request = KeywordRequest(
            keywords=keywords,
            limit=limit,
            offset=offset,
            filter_options_request=filter_options_request,
            sort_options=sort_options
        )

        response = digikey.v4.api.keyword_search(body=request)
        if response:
            with open("category_308_positions_8_search.yaml", "w") as f:
                yaml.dump(response.to_dict(), f, default_flow_style=False, sort_keys=False)
            print("Saved search results to category_308_positions_8_search.yaml")
            return response
        else:
            print("No search results found for parametric search.")
            return None
    except Exception as e:
        print(f"Error fetching parametric search results: {e}")
        return None

def get_digikey_search(pn):
    """Fetch search from Digikey API v4."""
    try:
        request = ProductDetails(product_number=pn)
        response = digikey.v4.api.product_details(body=request)
        if response:
            # Save the response as a YAML file
            with open(f"{pn}_search.yaml", "w") as f:
                yaml.dump(response.to_dict(), f, default_flow_style=False, sort_keys=False)
            print(f"Category for {pn}: {response.category.name} (ID: {response.category.id})")
            print(f"Saved search results to {pn}_search.yaml")
            return response
        else:
            print(f"No search results found for {pn}.")
            return None
    except Exception as e:
        print(f"Error fetching search results for {pn}: {e}")
        return None


if __name__ == "__main__":
    #warnings.filterwarnings("ignore")
    cat_ids = {}
    for part_number in TEST_PART_NUMBERS:
        print(f"Finding part number: {part_number}")
        dksearch = get_digikey_search(part_number)
        cat_ids[part_number] = dksearch.category.id
        get_parametric_search(category_id=cat_ids[part_number], parameters=[
            {"id": 88, "values": [281474]}
        ])