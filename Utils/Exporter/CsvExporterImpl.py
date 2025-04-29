import csv
import os

class CsvExporterImpl:
    """
    Concrete implementation to export the execution time results into a CSV file
    for different numbers of attributes (3, 6, 9).
    """

    def __init__(self, output_path="Results.csv"):
        """
        Constructor of CsvExporterImpl.

        :param output_path: The path where the CSV file will be saved (default is "Results.csv").
        """
        self.output_path = output_path

    def export(self, app):
        """
        Export the time information from the App instance into the CSV file.

        :param app: The App instance containing the algorithm execution results.
        """
        algo_instance = app.algo_instance
        algo_name = app.algo

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        if hasattr(algo_instance, "time"):
            self.exportTimePoint(
                cardinality=app.tuples,
                time=algo_instance.time,
                attributes=app.cardinality
            )
            print(f"[CSV Exporter] Time point exported to {self.output_path}")
        else:
            print(f"[CSV Exporter] Warning: no time data found in {algo_name}")

    def exportTimePoint(self, cardinality, time, attributes):
        """
        Export a single point (cardinality, execution time) to the appropriate column
        based on the number of attributes (3, 6, or 9). Other columns are left empty.

        :param cardinality: The number of tuples in the dataset.
        :param time: The execution time in seconds.
        :param attributes: The number of attributes (must be 3, 6, or 9).
        :raises ValueError: If the number of attributes is not 3, 6, or 9.
        """
        if attributes not in (3, 6, 9):
            raise ValueError("Unsupported attribute count. Expected 3, 6, or 9.")

        # Prepare a CSV row: cardinality, time_attr3, time_attr6, time_attr9
        time_attr3 = time if attributes == 3 else ""
        time_attr6 = time if attributes == 6 else ""
        time_attr9 = time if attributes == 9 else ""

        header = ["cardinality", "time_attr3", "time_attr6", "time_attr9"]
        file_exists = os.path.isfile(self.output_path)

        with open(self.output_path, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(header)
            writer.writerow([cardinality, time_attr3, time_attr6, time_attr9])
