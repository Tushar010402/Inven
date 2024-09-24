import json

def load_and_print_data():
    try:
        with open('cans_data.json', 'r') as file:
            data = json.load(file)
            print("Sample Data for Cans:")
            print(json.dumps(data, indent=2))
            print(f"\nTotal number of can types: {len(data['cans'])}")

            for can in data['cans']:
                print(f"\nProduct: {can['product_name']}")
                print(f"Category: {can['category']}")
                print(f"Inventory Count: {can['inventory_count']}")
                print(f"Unit: {can['unit']}")
    except FileNotFoundError:
        print("Error: cans_data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in cans_data.json.")
    except KeyError:
        print("Error: Unexpected data structure in cans_data.json.")

if __name__ == "__main__":
    load_and_print_data()
