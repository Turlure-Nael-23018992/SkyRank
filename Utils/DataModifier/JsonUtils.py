import json
import sys
import os


def readJson(filePath, asTuple=False):
    """
    Reads a JSON file and returns its content.

    :param filePath: Path to the JSON file.
    :param asTuple: If True, converts dictionary values to tuples.
    :return: The parsed JSON data as a dictionary.
    """
    with open(filePath, 'r') as file:
        data = json.load(file)
        if asTuple:
            return {key: tuple(value) for key, value in data.items()}
        return data


def writeJson(filePath, data):
    """
    Writes data to a JSON file.

    :param filePath: Path where the JSON file will be saved.
    :param data: Data to write (dictionary).
    """
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)


def updateJson(filePath, key, value, type="arr"):
    """
    Updates or adds a key in a JSON file.

    :param filePath: Path to the JSON file.
    :param key: Key to update or add.
    :param value: Value to set for the given key.
    :param type: (Unused for now) Type of data. Default is "arr".
    """
    data = readJson(filePath)
    data[key] = value
    writeJson(filePath, data)


def prettyPrintTimeData(filePath):
    """
    Pretty-prints the time_data section of a JSON file in a table format.

    :param filePath: Path to the JSON file.
    """
    try:
        data = readJson(filePath)

        print(f"{'Rows':<10} {'3 Columns':<15} {'6 Columns':<15} {'9 Columns':<15}")
        print("-" * 55)

        for rows, times in data.get("time_data", {}).items():
            if isinstance(times, list) and len(times) >= 3:
                print(f"{rows:<10} {times[0]:<15.6f} {times[1]:<15.6f} {times[2]:<15.6f}")
            else:
                print(f"{rows:<10} {'Invalid data':<15}")

        print("\nSummary:")
        print(f"Max Rows: {data.get('max_rows', 'N/A')}")
        print(f"Max Time: {data.get('max_time', 'N/A')}")

    except FileNotFoundError:
        print(f"Error: File not found at {filePath}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")


def toOneColumn(fp, idx, outputFile):
    """
    Converts time_data to keep only one column (3, 6, or 9 attributes).

    :param fp: Input JSON file path.
    :param idx: Index of the column to keep (0 for 3 cols, 1 for 6 cols, 2 for 9 cols).
    :param outputFile: Output file path to save the transformed data.
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
    Sorts the time_data dictionary inside a JSON file by ascending number of rows.

    :param fp: Path to the JSON file to sort.
    """
    data = readJson(fp)

    time_data = data.get("time_data", {})
    sorted_time_data = dict(sorted(time_data.items(), key=lambda item: int(item[0])))

    data["time_data"] = sorted_time_data

    writeJson(fp, data)


def addServerConfigToJson(json_path, config_path):
    """
    Adds server configuration into an existing JSON file.

    :param json_path: Path to the JSON file where configuration will be inserted.
    :param config_path: Path to the server configuration JSON file.
    :raises FileNotFoundError: If json_path or config_path does not exist.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    data = readJson(json_path)
    server_config = readJson(config_path)

    data["server_config"] = server_config

    writeJson(json_path, data)
    print(f"[OK] Server configuration added into {json_path}")


if __name__ == "__main__":
    import glob

    json_folder = "../../Assets/LatexData/OneAlgoData/"
    config_path = "../../Assets/ServerConfig/ConfigNael.json"

    json_files = glob.glob(os.path.join(json_folder, "**", "*.json"), recursive=True)

    for json_file in json_files:
        try:
            addServerConfigToJson(json_file, config_path)
        except Exception as e:
            print(f"[ERROR] Could not process {json_file} -> {e}")

    print("[DONE] Server configuration added to all JSON files.")
