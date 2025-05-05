import json
import os


class JsonExporterImpl:
    """
    Exporter implementation that saves execution metadata and Skyline point identifiers in JSON format.
    """

    def __init__(self, output_path="../Assets/Export/JsonFiles/Result.json"):
        """
        :param output_path: Path to the JSON file to export to.
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

        # Handle point extraction: list of tuples or dict {id: tuple}
        points = self._extract_ids_from_result(algo_instance)

        result = {
            "skyline_points": points,
            "execution_time": time,
            "algorithm": algo_name,
            "input_type": input_type,
            "input_file": input_file
        }

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=4)

        print(f"[JSON Exporter] Exported to {self.output_path}")

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
