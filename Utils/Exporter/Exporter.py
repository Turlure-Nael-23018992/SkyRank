class Exporter:
    """
    Abstract base class for exporters.

    Any concrete exporter must implement the 'export' method.
    """

    def export(self, app):
        """
        Export the results of the given App instance.

        :param app: Instance of App containing the results to export.
        :raises NotImplementedError: Always, unless overridden in a subclass.
        """
        raise NotImplementedError("Exporter must implement the export(app) method")