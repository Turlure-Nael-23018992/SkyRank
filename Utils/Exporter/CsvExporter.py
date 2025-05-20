import csv
import os

class CsvExporter:
    """
    Simple CSV exporter to save basic App results to a CSV file.
    """

    def __init__(self, output_path="Results.csv"):
        """
        :param output_path: The path where the CSV file will be saved.
        """
        self.output_path = output_path

    def export(self, app):
        """
        Export the algorithm name, cardinality, number of tuples, and execution time into a CSV file.

        :param app: The App instance containing the results.
        """
        algo_instance = app.algo_instance
        algo_name = app.algo
        time = getattr(algo_instance, 'time', 0)

        headers = ['algorithm', 'cardinality', 'tuples', 'execution_time']
        data = [algo_name, app.cardinality, app.tuples, time]

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow(data)

        print(f"[CSV Exporter] Exported summary to {self.output_path}")
