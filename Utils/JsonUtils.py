import json

def read_json(filePath):
    """Reads a JSON file and returns its content."""
    with open(filePath, 'r') as file:
        return json.load(file)

def write_json(filePath, data):
    """Writes data to a JSON file."""
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)

def update_json(filePath, key, value):
    """Updates a specific key in a JSON file."""
    data = read_json(filePath)
    data[key] = value
    write_json(filePath, data)

def prettyPrintTimeData(filePath):
    """
    Pretty prints the time_data from a JSON file in a structured format.
    """
    try:
        data = read_json(filePath)

        print(f"{'Rows':<10} {'3 Columns':<15} {'6 Columns':<15} {'9 Columns':<15}")
        print("-" * 55)

        # Print each row of time_data
        for rows, times in data.items():
            print(f"{rows:<10} {times[0]:<15.6f} {times[1]:<15.6f} {times[2]:<15.6f}")

        # Print max_rows and max_time
        print("\nSummary:")
        print(f"Max Rows: {data.get('max_rows', 'N/A')}")
        print(f"Max Time: {data.get('max_time', 'N/A'):.6f}")

    except FileNotFoundError:
        print(f"Error: File not found at {filePath}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")


def sortJson(fp):
    data = read_json(fp)

    time_data = data.get("time_data", {})
    sorted_time_data = dict(sorted(time_data.items(), key=lambda item: int(item[0])))

    data["time_data"] = sorted_time_data

    write_json(fp, data)



if __name__ == "__main__":
    # Example usage
    pass