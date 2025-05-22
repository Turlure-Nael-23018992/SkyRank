import os
import json
from Utils.Latex.UniversalLatexMaker import UniversalLatexGenerator
from Utils.Latex.AlgoEnum import AlgoEnum
from Utils.Latex.AlgoCalculator import AlgoCalculator
from Utils.Preference import Preference


class LatexMain:
    def __init__(self):
        self.generator = UniversalLatexGenerator()
        self.base_path = "Assets/LatexFiles/"

    def ask_user_inputs(self):
        print("Welcome to the LaTeX Chart Generator!")
        n_algos = int(input("How many algorithms do you want to compare? (1-5): "))

        algos = []
        json_paths = []
        warning_algos = []

        print("Do you want to use pre-existing execution data (y/n)?")
        use_existing = input().strip().lower() == 'y'

        for i in range(n_algos):
            print(f"\n--- Algorithm #{i + 1} ---")
            algo_name = input("Enter the enum name (CoskySql, CoskyAlgorithme, RankSky, DpIdpDh, SkyIR etc.): ").strip()
            try:
                algo_enum = AlgoEnum[algo_name]
                algos.append(algo_enum)

                if use_existing:
                    json_file = f"Assets/LatexData/OneAlgoData/{algo_enum.name}/ThreeColumnsData/Execution{algo_enum.name}369.json"
                else:
                    json_file = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), "..", "Assets", "AlgoExecution", "ExecutionTime",
                                     f"{algo_enum.name}.json"))
                    self.calculate_execution_time(algo_enum, json_file)

                json_paths.append(json_file)
                print(f"✅ JSON path added: {json_file}")

                if algo_enum.name in ["DpIdpDh", "SkyIR"]:
                    warning_algos.append(algo_enum.name)

            except KeyError:
                print(f"❌ Error: {algo_name} is not a valid AlgoEnum value.")
                return None

        if warning_algos:
            print("\n⚠️  Warning:")
            print("Some algorithms have limited benchmark data (especially DpIdpDh and SkyIR).")
            print("Their execution time curves might be incomplete or not comparable on large inputs.")

        max_entries = input("\nMax data points to plot? Leave empty for full range: ")
        max_entries = int(max_entries) if max_entries.strip() else None

        scale_type = input("Scale type? (LinX/LinY, LogX/LogY, LinX/LogY, etc.): ").strip() or "LinX/LinY"
        print("n_algos:", n_algos)
        print("algos:", algos)
        print("json_paths:", json_paths)
        print("max_entries:", max_entries)
        print("scale_type:", scale_type)
        return n_algos, algos, json_paths, max_entries, scale_type

    def calculate_execution_time(self, algo_enum, output_path):
        calculator = AlgoCalculator("../Assets/Databases/cosky_db_C3_R1000.db")
        pref_map = {
            3: [Preference.MIN] * 3,
            6: [Preference.MIN] * 6,
            9: [Preference.MIN] * 9,
        }

        algo_class = algo_enum.get_algo_class()
        for col in [3, 6, 9]:
            calculator.compareExecutionTime(
                algo_class,
                output_path,
                cols=[col],
                rows=[10, 20, 50, 100, 500, 1000],
                pref=pref_map[col]
            )

    def load_data(self, paths):
        time_dicts = []
        for path in paths:
            with open(path, "r") as f:
                data = json.load(f)

            time_dict = {}
            for k, v in data["time_data"].items():
                try:
                    key = int(k)
                    values = [
                        float(val) if isinstance(val, (int, float)) or (
                            isinstance(val, str) and val.replace('.', '', 1).isdigit())
                        else None for val in v
                    ]
                    time_dict[key] = values
                except Exception as e:
                    print(f"⚠️ Error processing key {k} in {path}: {e}")
            time_dicts.append(time_dict)
        return time_dicts

    def compute_max_rows(self, time_dicts, attributes=[3, 6, 9]):
        max_rows_list = []
        for i in range(len(attributes)):
            max_row = 0
            for d in time_dicts:
                for k in d:
                    val = d[k][i] if i < len(d[k]) else None
                    if isinstance(val, (int, float)):
                        max_row = max(max_row, int(k))
            max_rows_list.append(max_row)
        return max_rows_list

    def compute_max_times(self, time_dicts, attributes=[3, 6, 9]):
        max_time_list = []
        for i in range(len(attributes)):
            max_val = 0
            for d in time_dicts:
                for k in d:
                    val = d[k][i] if i < len(d[k]) else None
                    if isinstance(val, (int, float)) and val > max_val:
                        max_val = val
            max_time_list.append(max_val)
        return max_time_list

    def build_output_path(self, algo_names, count, scale_type):
        folder_map = {
            1: "OneAlgoComparaison",
            2: "TwoAlgosComparaison",
            3: "ThreeAlgosComparaison",
            4: "FourAlgosComparaison",
            5: "FiveAlgosComparaison"
        }
        folder = folder_map[count]
        base = "_".join(algo_names)
        scale_type = scale_type.replace("/", "_").replace("\\", "_")
        base += scale_type
        return os.path.join(folder, base + ".tex")

    def run(self):
        user_input = self.ask_user_inputs()
        if user_input is None:
            return

        n_algos, algos, json_paths, max_entries, scale_type = user_input

        time_dicts = self.load_data(json_paths)
        if max_entries:
            time_dicts = self.generator.normalizeTimeDicts(time_dicts, max_entries=max_entries)

        max_rows_list = self.compute_max_rows(time_dicts)
        max_time_list = self.compute_max_times(time_dicts)

        algo_names = [a.name for a in algos]
        output_rel_path = self.build_output_path(algo_names, n_algos, scale_type)

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        output_abs_path = os.path.join(root_dir, 'Assets', 'LatexFiles', output_rel_path)

        output_dir = os.path.dirname(output_abs_path)
        if not os.path.exists(output_dir):
            print(f"❌ Error: Output directory does not exist: {output_dir}")
            return

        # Génération du fichier LaTeX
        generator = UniversalLatexGenerator(output_path=output_abs_path)
        generator.generate_latex(
            time_dicts,
            max_rows_list,
            max_time_list,
            algos,
            scaleType=scale_type
        )

        print(f"✅ LaTeX chart successfully generated at: {output_abs_path}")


def main():
    runner = LatexMain()
    runner.run()


if __name__ == "__main__":
    main()
