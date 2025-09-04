def get_parametric_search(category_id=308, parameters=[]):
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
                "ParameterId": i.get("parameter_id"),
                "FilterValues": [{"Id": str(v)} for v in i.get("values", [])]
            })
        parameter_filter_request = {
            "CategoryFilter": {"Id": str(category_id)},
            "ParameterFilters": parameter_filters
        }
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