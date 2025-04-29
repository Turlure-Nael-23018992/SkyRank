import csv
import os

class CsvExporterImpl:
    def __init__(self, output_path="Results.csv"):
        self.output_path = output_path

    def export(self, app):
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
        Exporte un seul point (cardinality, time) dans la colonne correcte (selon nb d'attributs 3, 6 ou 9).
        Les colonnes non concernées restent vides.
        """
        if attributes not in (3, 6, 9):
            raise ValueError("Unsupported attribute count. Expected 3, 6, or 9.")

        # Prépare une ligne CSV au format : cardinality, time_attr3, time_attr6, time_attr9
        time_attr3 = time if attributes == 3 else ""
        time_attr6 = time if attributes == 6 else ""
        time_attr9 = time if attributes == 9 else ""

        # Si le fichier n'existe pas, on crée l'en-tête
        header = ["cardinality", "time_attr3", "time_attr6", "time_attr9"]
        file_exists = os.path.isfile(self.output_path)

        with open(self.output_path, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(header)
            writer.writerow([cardinality, time_attr3, time_attr6, time_attr9])
