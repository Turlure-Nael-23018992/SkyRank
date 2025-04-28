# Utils/Exporter/Exporter.py

class Exporter:
    """
    Exporter interface: all exporters must implement the export(app) method.
    """

    def export(self, app):
        """
        Export the application results.

        :param app: Instance of App
        """
        raise NotImplementedError("Exporter must implement export(app) method")
