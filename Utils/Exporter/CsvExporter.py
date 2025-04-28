import csv

class CsvExporter:
    """
    Class to export benchmarking results into a normalized CSV file.
    """

    def __init__(self, output_path="benchmark_results.csv"):
        self.output_path = output_path

    def normalize(self, values, scale=300):
        """
        Normalize a list of values to a given scale.

        :param values: List of values to normalize.
        :param scale: Maximum value after normalization.
        :return: List of normalized integer values.
        """
        max_val = max(values)
        if max_val == 0:
            return [0 for _ in values]
        return [int((v / max_val) * scale) for v in values]

    def export(self, app_instances):
        """
        Export a list of App instances into a CSV file.

        :param app_instances: List of App instances containing algorithm results.
        """
        rows = []
        for app in app_instances:
            rows.append({
                "cardinality": app.cardinality,
                "tuples": app.tuples,
                app.algo_instance.__class__.__name__: app.algo_instance.time
            })

        grouped = {}
        for row in rows:
            key = (row["cardinality"], row["tuples"])
            if key not in grouped:
                grouped[key] = {}
            grouped[key].update(row)

        all_times = [v for g in grouped.values() for k, v in g.items() if isinstance(v, (int, float))]
        normalized = self.normalize(all_times)

        idx = 0
        for g in grouped.values():
            for k, v in g.items():
                if isinstance(v, (int, float)):
                    g[k] = normalized[idx]
                    idx += 1

        with open(self.output_path, "w", newline="") as csvfile:
            algo_names = list({k for g in grouped.values() for k in g.keys() if k not in ["cardinality", "tuples"]})
            fieldnames = ["cardinality", "tuples"] + sorted(algo_names)

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for (card, tup), g in grouped.items():
                row = {"cardinality": card, "tuples": tup}
                for algo in algo_names:
                    row[algo] = g.get(algo, "")
                writer.writerow(row)

        print(f"\n✅ CSV export completed: {self.output_path}")
