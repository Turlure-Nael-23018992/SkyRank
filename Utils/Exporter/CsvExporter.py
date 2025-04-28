# Utils/Exporter/CsvExporter.py

import csv

class CsvExporter:
    """
    Concrete class to export App results into a CSV file.
    """

    def __init__(self, output_path="Results.csv"):
        self.output_path = output_path

    def export(self, app):
        """
        Export the app results to a CSV file.

        :param app: App instance
        """
        headers = ['cardinality', 'tuples', app.algo]
        data = [app.cardinality, app.tuples, getattr(app.algo_instance, 'time', 0)]

        with open(self.output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow(data)
