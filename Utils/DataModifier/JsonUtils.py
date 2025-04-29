import json
import sys
import os


def readJson(filePath, asTuple=False):
    """
    Reads a JSON file and returns its content.
    If asTuple is True, converts the values of the dictionary to tuples.
    """
    with open(filePath, 'r') as file:
        data = json.load(file)
        if asTuple:
            # Convert only the values to tuples
            return {key: tuple(value) for key, value in data.items()}
        return data


def writeJson(filePath, data):
    """
    Writes data to a JSON file.
    """
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)

def updateJson(filePath, key, value, type="arr"):
    """
    Updates a specific key in a JSON file.
    """
    data = readJson(filePath)
    data[key] = value
    writeJson(filePath, data)

def prettyPrintTimeData(filePath):
    """
    Pretty prints the time_data from a JSON file in a structured format.
    """
    try:
        data = readJson(filePath)

        print(f"{'Rows':<10} {'3 Columns':<15} {'6 Columns':<15} {'9 Columns':<15}")
        print("-" * 55)

        # Print each row of time_data
        for rows, times in data.get("time_data", {}).items():
            if isinstance(times, list) and len(times) >= 3:
                print(f"{rows:<10} {times[0]:<15.6f} {times[1]:<15.6f} {times[2]:<15.6f}")
            else:
                print(f"{rows:<10} {'Invalid data':<15}")

        # Print max_rows and max_time
        print("\nSummary:")
        print(f"Max Rows: {data.get('max_rows', 'N/A')}")
        print(f"Max Time: {data.get('max_time', 'N/A')}")

    except FileNotFoundError:
        print(f"Error: File not found at {filePath}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")


def toOneColumn(fp, idx, outputFile):
    """
    Converts the time_data in a JSON file to a single column format.
    """
    data = readJson(fp)

    time_data = data.get("time_data", {})
    new_time_data = {}

    for key, value in time_data.items():
        if isinstance(value, list) and len(value) > idx:
            new_time_data[key] = [value[idx]]

    data["time_data"] = new_time_data
    print("New time_data:", [new_time_data])

    writeJson(outputFile, data)


def sortJson(fp):
    """
    Sorts the time_data in a JSON file by the first column.
    """
    data = readJson(fp)

    time_data = data.get("time_data", {})
    sorted_time_data = dict(sorted(time_data.items(), key=lambda item: int(item[0])))

    data["time_data"] = sorted_time_data

    writeJson(fp, data)


def addServerConfigToJson(json_path, config_path):
    """
    Add server configuration into an existing JSON file.

    Args:
        json_path (str): Path to the target JSON file (e.g., "Assets/LatexData/ExecutionCoskySql369.json")
        config_path (str): Path to the server configuration JSON file (e.g., "Assets/ServerConfig/ConfigNael.json")

    Raises:
        FileNotFoundError: If either the json_path or config_path does not exist.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    data = readJson(json_path)
    server_config = readJson(config_path)

    # Add server configuration under the key "server_config"
    data["server_config"] = server_config

    writeJson(json_path, data)
    print(f"[OK] Server configuration added into {json_path}")

if __name__ == "__main__":
    import glob

    # Path to the folder containing all JSON files
    json_folder = "../../Assets/LatexData/OneAlgoData/"
    # Path to the server config to insert (example: ConfigNael.json or ConfigMickael.json)
    config_path = "../../Assets/ServerConfig/ConfigNael.json"

    # Get all JSON files recursively
    json_files = glob.glob(os.path.join(json_folder, "**", "*.json"), recursive=True)

    for json_file in json_files:
        try:
            addServerConfigToJson(json_file, config_path)
        except Exception as e:
            print(f"[ERROR] Could not process {json_file} -> {e}")

    print("[DONE] Server configuration added to all JSON files.")
