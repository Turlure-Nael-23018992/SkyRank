# Utils/Exporter/CsvExporter.py

import csv

class CsvExporter:
    """
    Concrete class to export the results of an App instance into a CSV file.
    """

    def __init__(self, output_path="Results.csv"):
        """
        Constructor of CsvExporter.

        :param output_path: The path where the CSV file will be saved (default is "Results.csv").
        """
        self.output_path = output_path

    def export(self, app):
        """
        Exports the App's results (cardinality, number of tuples, execution time) into a CSV file.

        :param app: The App instance containing the results to export.
        """
        headers = ['cardinality', 'tuples', app.algo]
        data = [app.cardinality, app.tuples, getattr(app.algo_instance, 'time', 0)]

        with open(self.output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow(data)