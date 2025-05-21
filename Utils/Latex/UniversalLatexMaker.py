import math
import json
import os
from Utils.Latex.AlgoEnum import AlgoEnum

class UniversalLatexGenerator:
    def __init__(self, output_path="../../Assets/LatexFiles/UniversalLatexOutput.tex"):
        self.colors = ["skyblue", "cyan", "brightmaroon", "SQLCodeGreen", "SQLcodegray"]
        self.output_path = output_path

    def get_rgb_value(self, color_name):
        color_map = {
            "brightmaroon": ("195,33,72", "RGB"),
            "cyan": ("0,255,255", "RGB"),
            "skyblue": ("135,206,235", "RGB"),
            "SQLCodeGreen": ("0,100,0", "RGB"),
            "SQLcodegray": ("127,127,127", "RGB"),
        }
        return color_map.get(color_name, ("0,0,0", "RGB"))

    def round_to_axis(self, value):
        if value == 0:
            return 10
        magnitude = 10 ** (len(str(int(value))) - 1)
        return ((int(value) // magnitude) + 1) * magnitude

    def format_tick_label(self, value):
        if value <= 0:
            return "$0$"
        exponent = int(math.log10(value)) if value > 0 else 0
        base = int(value / (10 ** exponent)) if exponent > 0 else int(value)
        return f"${base} \\times 10^{{{exponent}}}$" if exponent >= 3 else f"${int(value)}$"

    def generate_latex(self, timeDicts, maxRowsList, maxTimeList, algos, attributes=[3, 6, 9],
                       scaleX=280, scaleY=280, scaleType="LinX/LinY"):
        is_log_x = "LogX" in scaleType
        is_log_y = "LogY" in scaleType

        lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            r"\begin{document}"
        ]

        for i, color in enumerate(self.colors[:len(algos)]):
            rgb, mode = self.get_rgb_value(color)
            lines.append(f"\\definecolor{{{color}}}{{{mode}}}{{{rgb}}}")
            lines.append(
                f"\\tikzset{{small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, "
                f"minimum size=4pt, inner sep=0pt}}}}"
            )

        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]
            maxTime = self.round_to_axis(maxTimeList[i])
            ratioX = scaleX / math.log(maxRows + 1) if is_log_x else scaleX / maxRows
            ratioY = (scaleY * 0.8) / math.log(maxTime + 1) if is_log_y else (scaleY * 0.8) / maxTime

            graph = [f"% Graph for {attr} attributes", r"\begin{tikzpicture}[line join=bevel]"]

            graph.append(f"\\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};")
            graph.append(f"\\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time (s)}};")

            # X-axis ticks
            graph.append("        \\foreach \\x/\\xtext in {")
            for s in range(6):
                frac = s / 5
                if is_log_x:
                    log_val = math.log(maxRows + 1) * frac
                    raw_val = int(math.exp(log_val)) - 1
                    pos = int(log_val * ratioX)
                else:
                    raw_val = int(maxRows * frac)
                    pos = int(scaleX * frac)
                label = self.format_tick_label(raw_val)
                graph.append(f"            {pos}pt/{label},")
            graph[-1] = graph[-1].rstrip(",") + "} {"
            graph.append("            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};")
            graph.append("        }")

            # Y-axis ticks
            graph.append("        \\foreach \\y/\\ytext in {")
            for s in range(6):
                frac = s / 5
                if is_log_y:
                    log_val = math.log(maxTime + 1) * frac
                    raw_val = int(math.exp(log_val)) - 1
                    pos = int(log_val * ratioY)
                else:
                    raw_val = maxTime * frac
                    pos = int((scaleY * 0.8) * frac)
                label = self.format_tick_label(raw_val)
                graph.append(f"            {pos}pt/{label},")
            graph[-1] = graph[-1].rstrip(",") + "} {"
            graph.append("            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};")
            graph.append("        }")

            # Lines and points
            for j, timeDict in enumerate(timeDicts):
                color = self.colors[j]
                line = f"        \\draw[{color}, line width=2pt]"
                points = []
                for k in sorted(timeDict.keys(), key=lambda x: int(x)):
                    y_raw = timeDict[k][i] if i < len(timeDict[k]) else None
                    if y_raw is None or not isinstance(y_raw, (int, float)):
                        continue
                    xval = math.log(int(k) + 1) if is_log_x else int(k)
                    yval = math.log(y_raw + 1) if is_log_y else y_raw
                    x = int(round(xval * ratioX))
                    y = int(round(yval * ratioY))
                    line += f" ({x}pt, {y}pt) --"
                    points.append(f"        \\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);")

                graph.append(line.rstrip(" --") + ";")
                graph.extend(points)

            # Legend
            graph.append(r"        \matrix [left=0cm of current bounding box.north east] at (current bounding box.north east) {")
            for j, algo in enumerate(algos):
                name = algo.value[0] if hasattr(algo, "value") else str(algo)
                graph.append(f"            \\node [small{self.colors[j]}node, label=right:{name} with {attr} attributes] {{}}; \\\\")
            graph.append(r"        };")
            graph.append(r"\end{tikzpicture}")
            graph.append(r"\clearpage")
            lines.extend(graph)

        lines.append(r"\end{document}")

        with open(self.output_path, "w") as f:
            f.write("\n".join(lines))

    def normalizeTimeDicts(self, timeDicts, max_entries=None):
        """
        Normalize a list of timeDicts so they all have the same keys.

        :param timeDicts: List of timeDicts (each a dict {int: [float, float, float]}).
        :param max_entries: Optional maximum number of entries to keep (sorted by key).
        :return: Normalized list of timeDicts (same keys, same length).
        """
        # Find common keys
        key_sets = [set(map(int, td.keys())) for td in timeDicts]
        common_keys = set.intersection(*key_sets)

        # Sort the common keys
        sorted_common_keys = sorted(common_keys)
        if max_entries is not None:
            sorted_common_keys = sorted_common_keys[:max_entries]

        # Filter all dicts to only those keys
        normalized = []
        for td in timeDicts:
            new_td = {int(k): td[int(k)] for k in sorted_common_keys}
            normalized.append(new_td)

        return normalized


def load_json_data(paths, attributes=[3, 6, 9], max_entries=None):
    timeDicts = []
    for path in paths:
        with open(path, "r") as file:
            data = json.load(file)
        time_dict = {int(k): v for k, v in data["time_data"].items()}
        timeDicts.append(time_dict)

    # Normalisation si demandée
    if max_entries:
        generator = UniversalLatexGenerator()
        timeDicts = generator.normalizeTimeDicts(timeDicts, max_entries=max_entries)

    maxRowsList = [max(td.keys()) for td in timeDicts] * len(attributes)
    maxTimeList = [
        max(td[k][i] for td in timeDicts for k in td)
        for i in range(len(attributes))
    ]
    return timeDicts, maxRowsList, maxTimeList



if __name__ == "__main__":
    generator = UniversalLatexGenerator()
    json_paths = [
        "../../Assets/LatexData/OneAlgoData/CoskyAlgo/ThreeColumnsData/ExecutionCoskyAlgo369.json",
        "../../Assets/LatexData/OneAlgoData/RankSky/ThreeColumnsData/ExecutionRankSky369.json"
    ]
    algos = [AlgoEnum.CoskyAlgorithme, AlgoEnum.RankSky]
    timeDicts, maxRowsList, maxTimeList = load_json_data(json_paths, max_entries=16)

    generator.generate_latex(
        timeDicts,
        maxRowsList,
        maxTimeList,
        algos,
        attributes=[3, 6, 9],
        scaleX=280,
        scaleY=280,
        scaleType="LinX/LinY"
    )

    print(timeDicts[0])
    print(timeDicts[1])


