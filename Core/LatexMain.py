import os
from Utils.Latex.UniversalLatexMaker import UniversalLatexGenerator
from Utils.Latex.AlgoEnum import AlgoEnum
import json

class LatexMain:
    def __init__(self):
        self.generator = UniversalLatexGenerator()
        self.base_path = "Assets/LatexFiles/"
        self.data_path = ""

    def ask_user_inputs(self):
        print("Welcome to the LaTeX Chart Generator!")
        n_algos = int(input("How many algorithms do you want to compare? (1-5): "))

        algos = []
        json_paths = []
        warning_algos = []

        for i in range(n_algos):
            print(f"\n--- Algorithm #{i + 1} ---")
            algo_name = input("Enter the enum name (CoskySql, CoskyAlgorithme, RankSky, DpIdpDh, SkyIR etc.): ").strip()
            try:
                algo_enum = AlgoEnum[algo_name]
                algos.append(algo_enum)
                json_file = f"{algo_enum.value[1]}"
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

        return n_algos, algos, json_paths, max_entries, scale_type

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
                            isinstance(val, str) and val.replace('.', '', 1).isdigit()
                        ) else None for val in v
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
        output_abs_path = os.path.join(self.base_path, output_rel_path)

        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)

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