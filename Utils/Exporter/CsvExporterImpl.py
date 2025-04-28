# Utils/Exporter/CsvExporterImpl.py

from Utils.Exporter.Exporter import Exporter
from Utils.Exporter.CsvExporter import CsvExporter

class CsvExporterImpl(Exporter):
    """
    Adapter to respect the Exporter interface for CSV export.
    """

    def __init__(self, output_path="Results.csv"):
        """
        Initialize the CsvExporterImpl with a specific output path.
        :param output_path: Path to the output CSV file.
        """
        self.csvExporter = CsvExporter(output_path)

    def export(self, app):
        """
        Export the application results to a CSV file.
        :param app: Instance of App
        """
        self.csvExporter.export(app)
