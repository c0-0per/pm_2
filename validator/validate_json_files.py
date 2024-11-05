import json
import datetime
import sys
import os

def validate_items(data, expected_types, unique_fields=[], allowed_values={}, date_fields=[]):
    errors = []
    uniques = {field: set() for field in unique_fields}

    for idx, item in enumerate(data):
        for field, expected_type in expected_types.items():
            if field not in item:
                errors.append(f"Item {idx + 1}: Missing field '{field}'.")
                continue
            if not isinstance(item[field], expected_type):
                errors.append(
                    f"Item {idx + 1}: Field '{field}' is not of type {expected_type.__name__}."
                )
        
        for field in unique_fields:
            value = item.get(field)
            if value in uniques[field]:
                errors.append(f"Item {idx + 1}: Duplicate '{field}' '{value}'.")
            else:
                uniques[field].add(value)

        for field, allowed in allowed_values.items():
            value = item.get(field)
            if isinstance(value, list):
                for v in value:
                    if v not in allowed:
                        errors.append(
                            f"Item {idx + 1}: Invalid value '{v}' for field '{field}'."
                        )
            else:
                if value not in allowed:
                    errors.append(
                        f"Item {idx + 1}: Invalid value '{value}' for field '{field}'."
                    )

        for date_field in date_fields:
            date_str = item.get(date_field, "")
            if date_str:
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    errors.append(
                        f"Item {idx + 1}: Field '{date_field}' does not match 'YYYY-MM-DD' format."
                    )
    return errors

def main():
    files_to_validate = {
        "startups.json": {
            "expected_types": {
                "startup_name": str,
                "last_updated": str,
                "founded_date": str,
                "industry": list,
                "founders": str,
                "funding_round": str,
                "amount_raised": str,
                "date_of_funding": str,
                "tags": str,
                "website": str,
                "country": str,
                "data_sources": list,
                "investors": list,
                "tracking_reports": list,
                "record_id": str,
            },
            "unique_fields": ["startup_name"],
            "allowed_values": {
                "industry": [
                    "Artificial Intelligence",
                    "Renewable Energy",
                    "Educational Technology",
                    "Healthcare",
                    "Fashion Technology",
                    "Fintech",
                    "Other"
                ],
            },
            "date_fields": ["last_updated", "founded_date", "date_of_funding"],
        },
        "data_sources.json": {
            "expected_types": {
                "source_name": str,
                "source_url": str,
                "data_type": list,
                "collection_frequency": str,
                "last_updated": str,
                "associated_countries": list,
                "related_tracking_reports": list,
                "startups": list,
                "record_id": str,
            },
            "unique_fields": ["source_name"],
            "allowed_values": {
                "collection_frequency": ["Daily", "Weekly", "Monthly"],
                "data_type": ["Fundraising Activities", "Startups", "Investors", "Other"],
            },
            "date_fields": ["last_updated"],
        },
        "tracking_reports.json": {
            "expected_types": {
                "report_id": str,
                "data_source": str,
                "report_date": str,
                "summary": str,
                "startups_covered": list,
                "countries": list,
                "generated_by": str,
                "record_id": str,
            },
            "unique_fields": ["report_id"],
            "date_fields": ["report_date"],
        },
        "countries.json": {
            "expected_types": {
                "country": str,
                "number_of_startups": int,
                "primary_language": str,
                "currency_used": str,
                "startups": list,
                "tracking_reports": list,
                "data_sources": list,
                "record_id": str,
            },
            "unique_fields": ["country", "record_id"],
        },
        "investors.json": {
            "expected_types": {
                "investor_name": str,
                "investor_type": str,
                "investment_amount": str,
                "contact_information": str,  
                "associated_startups": list,
                "record_id": str,
            },
            "unique_fields": ["investor_name", "record_id"],
            "allowed_values": {
                "investor_type": ["Individual", "Organization"]
            },
        },
    }

    all_errors = False
    for filename, params in files_to_validate.items():
        path_to_filename = "../json_files/" + filename
        print(f"Validating {path_to_filename}...")
        if not os.path.exists(path_to_filename):
            print(f"Error: '{path_to_filename}' file not found.")
            continue
        try:
            with open(path_to_filename, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in '{path_to_filename}': {e}")
            continue

        data_list = data
        if not isinstance(data_list, list):
            print(f"Error: Expected a list in '{path_to_filename}'.")
            continue

        errors = validate_items(
            data_list,
            params["expected_types"],
            params.get("unique_fields", []),
            params.get("allowed_values", {}),
            params.get("date_fields", [])
        )

        if errors:
            all_errors = True
            print(f"Validation errors found in '{path_to_filename}':")
            for error in errors:
                print(error)
        else:
            print(f"All items in '{path_to_filename}' passed validation.\n")
    if all_errors:
        sys.exit(1)
    else:
        print("All files passed validation.")

if __name__ == "__main__":
    main()
