import csv
import os

class CsvExporterImpl:
    """
    Exporter implementation that saves execution metadata and Skyline point identifiers in CSV format.
    """

    def __init__(self, output_path="../Assets/Export/CSVFiles/Result.csv"):
        """
        :param output_path: Path to the CSV file to export to.
        """
        self.output_path = output_path

    def export(self, app):
        """
        Export Skyline result information from the given App instance.

        :param app: The App instance with algorithm results.
        """
        algo_instance = app.algo_instance
        algo_name = app.algo
        time = getattr(algo_instance, "time", 0)
        input_type = app.input_type
        input_file = app.input_file or "generated"

        # Extract only the identifiers of the Skyline points
        points = self._extract_ids_from_result(algo_instance)

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["algorithm", "input_type", "input_file", "execution_time", "skyline_points"])
            writer.writerow([algo_name, input_type, input_file, time, ";".join(map(str, points))])

        print(f"[CSV Exporter] Exported to {self.output_path}")

    def _extract_ids_from_result(self, algo_instance):
        """
        Determine which attribute contains the Skyline points and extract only the IDs.
        """
        for attr in ['result', 'score', 's', 'rows_res']:
            if hasattr(algo_instance, attr):
                data = getattr(algo_instance, attr)
                if isinstance(data, dict):
                    return list(data.keys())
                elif isinstance(data, list):
                    return [item[0] if isinstance(item, (list, tuple)) and len(item) > 0 else item for item in data]
        return []
