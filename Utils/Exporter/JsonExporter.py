import json
import os


class JsonExporter:
    """
    Simple JSON exporter to save algorithm results from an App instance into a JSON file.
    """

    def __init__(self, output_path="Results.json"):
        """
        :param output_path: The path where the JSON file will be saved.
        """
        self.output_path = output_path

    def export(self, app):
        """
        Export basic execution info to a JSON file.

        :param app: The App instance to export.
        """
        data = {
            "cardinality": app.tuples,
            "attributes": app.cardinality,
            "algorithm": app.algo,
            "execution_time": getattr(app.algo_instance, "time", 0)
        }

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"[JSON Exporter] Exported to {self.output_path}")
