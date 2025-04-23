import json
import sys


def readJson(filePath):
    """
    Reads a JSON file and returns its content.
    """
    with open(filePath, 'r') as file:
        return json.load(file)

def writeJson(filePath, data):
    """
    Writes data to a JSON file.
    """
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)

def updateJson(filePath, key, value):
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



if __name__ == "__main__":
    #("../Assets/LatexDatas/OneAlgoDatas/ExecutionAncienRankSky369.json")
    #toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionDpIdpDh369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionDpIdpDh3.json")
    #toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskyAlgo369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionCoskyAlgo3.json")
    #toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskySql369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionCoskySql310^9.json")
    #toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionRankSky369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionRankSky3.json")
    toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionSkyIR369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionSkyIR3.json")
    #toOneColumn("../Assets/LatexDatas/OneAlgoDatas/ExecutionCoskySql369.json", 0, "../Assets/LatexDatas/OneAlgoDatas/OneColumnData/ExecutionCoskySql3.json")
    pass