import json

from Utils.DisplayHelpers import print_red
from Utils.Latex.AlgoEnum import AlgoEnum
import math

class LatexMaker:
    """
    Class responsible for generating LaTeX documents from algorithm execution results.
    """

    def __init__(self):
        """
        Initialize the LatexMaker instance with default colors and path.
        """
        self.latexCode = ""
        self.latexFinal = ""
        self.colors = ["skyblue", "cyan", "brightmaroon", "SQLCodeGreen", "SQLcodegray", "SQLCodePurple"]
        self.path = "../../Assets/LatexFiles/"
        self.defineColor = """\\definecolor{skyblue}{rgb}{0.53, 0.81, 0.92}
                                \\definecolor{brightmaroon}{rgb}{0.95, 0.82, 0.85}
                                \\definecolor{SQLCodeGreen}{rgb}{0,0.6,0}
                                \\definecolor{SQLcodegray}{rgb}{0.5,0.5,0.5}
                                \\definecolor{SQLCodePurple}{HTML}{C42043}"""

    def addLatexCode(self, latexCode):
        """
        Add generated LaTeX code to the final document.

        :param latexCode: The LaTeX code to add.
        """
        self.latexFinal += latexCode

    def render(self):
        """
        Save the final LaTeX code to a file.
        """
        print(self.path)
        with open(self.path, 'w') as file:
            file.write(self.latexCode)

    def getData(self, path):
        """
        Read and parse a JSON file containing execution time data.

        :param path: Path to the JSON file.
        :return: Tuple (timeDict, maxRows, maxTime)
        """
        with open(path, 'r') as file:
            data = json.load(file)
        timeDict = data.get("time_data", {})
        maxRows = data.get("max_rows", 0)
        maxTime = data.get("max_time", 0)
        return timeDict, maxRows, maxTime

    def get_rgb_value(self, color_name):
        """
        Return the RGB or HTML value for a given color name.

        :param color_name: Name of the color.
        :return: Tuple (color value, color format).
        """
        color_map = {
            "brightmaroon": ("195,33,72", "RGB"),
            "cyan": ("0,255,255", "RGB"),
            "skyblue": ("135,206,235", "RGB"),
            "SQLCodeGreen": ("006400", "HTML"),
            "SQLcodegray": ("7F7F7F", "HTML"),
            "SQLCodePurple": ("C42043", "HTML"),
        }
        return color_map.get(color_name, ("0,0,0", "RGB"))

    def prepareComparisonData(self, jsonPaths, attributes=[3, 6, 9]):
        """
        Prepare time data for comparison plots.

        :param jsonPaths: List of paths to JSON files.
        :param attributes: List of attributes to consider (default [3, 6, 9]).
        :return: (timeDicts, maxRowsList, maxTimeList)
        """
        timeDicts = []
        all_max_rows = []
        all_times_per_attr = [[] for _ in attributes]

        for path in jsonPaths:
            timeDict, maxRows, _ = self.getData(path)
            timeDict = {int(k): v for k, v in timeDict.items()}
            timeDicts.append(timeDict)
            all_max_rows.append(max(timeDict.keys()))

            for i in range(len(attributes)):
                print(len(attributes))
                all_times_per_attr[i].extend(
                    timeDict[k][i] for k in timeDict
                )

        maxRowsList = [max(all_max_rows)] * len(attributes)
        maxTimeList = [max(times) for times in all_times_per_attr]

        return timeDicts, maxRowsList, maxTimeList

    def roundToNearestN(value, n):
        """
        Round the given value to the nearest multiple of (n-1).

        :param value: The value to round.
        :param n: The reference number; rounding is done to a multiple of (n-1).
        :return: The rounded value.
        """
        if value == 0:
            return 0
        return round(value / (n - 1)) * (n - 1)

    def twoAlgoComparaison369Latex(self, timeDict1, timeDict2, maxRowsList, maxTimeList, algo1, algo2,
                                   latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9]):
        """
        Generate clean and well-indented LaTeX code to compare two algorithms across multiple attributes
        (typically for 3, 6, and 9 attributes), with linear scaling for axes.

        :param timeDict1: Time dictionary for the first algorithm.
        :param timeDict2: Time dictionary for the second algorithm.
        :param maxRowsList: List containing the maximum cardinality for each attribute configuration.
        :param maxTimeList: List containing the maximum execution time for each attribute configuration.
        :param algo1: Enum member (AlgoEnum) representing the first algorithm to compare.
        :param algo2: Enum member (AlgoEnum) representing the second algorithm to compare.
        :param latexFilePath: Path to save the generated LaTeX file (relative or absolute).
        :param scaleX: Width of the graph in points (default is 280pt).
        :param scaleY: Height of the graph in points (default is 280pt).
        :param attributes: List of attribute counts to compare (default is [3, 6, 9]).
        """
        self.path += latexFilePath
        algo1_name = algo1.value[0]
        algo2_name = algo2.value[0]

        # Define color styles
        color_styles = []
        for i, color in enumerate(self.colors[:2]):
            rgb = self.get_rgb_value(color)
            color_styles.append(f"\\definecolor{{{color}}}{{RGB}}{{{rgb}}}")
            color_styles.append(
                f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},"
                f"\nsmall{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}"
            )

        latex_lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            *color_styles,
            r"\begin{document}"
        ]

        for i in range(len(attributes)):
            maxTime = roundtoNearestThousand(maxTimeList[i])  # Round maxTime to nearest thousand
            print(maxTime)

            ratioX = scaleX / maxRowsList[i]
            ratioY = scaleY / maxTime

            # Algo 1 line and points
            line1 = f"\\draw[{self.colors[0]}, line width=2pt]"
            points1 = []
            for k in sorted(timeDict1.keys()):
                x = int(round(k * ratioX))
                y = int(round(timeDict1[k][i] * ratioY * 0.8))
                line1 += f"({x}pt, {y}pt) -- "
                points1.append(f"\\filldraw[color=black, fill={self.colors[0]}] ({x}pt, {y}pt) circle (2pt);")
            line1 = line1.rstrip(" -- ") + ";"

            # Algo 2 line and points
            line2 = f"\\draw[{self.colors[1]}, line width=2pt]"
            points2 = []
            for k in sorted(timeDict2.keys()):
                x = int(round(k * ratioX))
                y = int(round(timeDict2[k][i] * ratioY * 0.8))
                line2 += f"({x}pt, {y}pt) -- "
                points2.append(f"\\filldraw[color=black, fill={self.colors[1]}] ({x}pt, {y}pt) circle (2pt);")
            line2 = line2.rstrip(" -- ") + ";"

            # Axes graduations
            x_axis = "        \\foreach \\x/\\xtext in {\n"
            for step in [scaleX * s / 5 for s in range(6)]:
                value = roundtoNearestTen(maxRowsList[i] * (step / scaleX))
                x_axis += f"            {roundtoNearestTen(step)}pt/${value}$, \n"
            x_axis = (x_axis.rstrip(", \n")
                      + "} {\n"
                      + "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n"
                      + "        }")

            y_axis = "        \\foreach \\y/\\ytext in {\n"
            for step in [scaleY * s / 5 for s in range(5)]:
                adjusted_value = roundtoNearestTen(maxTime * (step / (scaleY * 0.8)))
                y_axis += f"            {roundtoNearestTen(step)}pt/${adjusted_value}$, \n"
            y_axis = (y_axis.rstrip(", \n")
                      + "} {\n"
                      + "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n"
                      + "        }")

            tikz_block = [
                f"    % Graph for {attributes[i]} attributes",
                r"    \begin{tikzpicture}[",
                f"        line join=bevel,",
                f"        big{self.colors[0]}node/.style={{shape=circle, fill={self.colors[0]}, draw=black, line width=1pt}},",
                f"        big{self.colors[1]}node/.style={{shape=circle, fill={self.colors[1]}, draw=black, line width=1pt}},",
                f"        small{self.colors[0]}node/.style={{circle, fill={self.colors[0]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},",
                f"        small{self.colors[1]}node/.style={{circle, fill={self.colors[1]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}",
                r"    ]",
                r"        % Axes",
                f"        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west] {{Cardinality}};",
                f"        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};",
                r"        % Axis graduation",
                x_axis,
                y_axis,
                r"        % Lines",
                f"        {line1}",
                f"        {line2}",
                r"        % Points",
                *["        " + pt for pt in points1],
                *["        " + pt for pt in points2],
                r"        % Caption",
                r"        \matrix [below left] at (current bounding box.north east) {",
                f"            \\node [small{self.colors[0]}node, label=right:{algo1_name} with {attributes[i]} attributes] {{}}; \\\\",
                f"            \\node [small{self.colors[1]}node, label=right:{algo2_name} with {attributes[i]} attributes] {{}}; \\\\",
                r"        };",
                r"    \end{tikzpicture}"
            ]

            latex_lines.extend(tikz_block)

        latex_lines.append(r"\end{document}")
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        self.render()

    def twoAlgoComparaison369LatexLog(self, timeDict1, timeDict2, maxRowsList, maxTimeList, algo1, algo2,
                                      latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9],
                                      scaleType="LinX/LinY"):
        """
        Generate LaTeX code to compare two algorithms across multiple attributes (3, 6, 9),
        with optional logarithmic or linear scaling on the X and/or Y axes.

        :param timeDict1: Time dictionary for the first algorithm.
        :param timeDict2: Time dictionary for the second algorithm.
        :param maxRowsList: List of maximum cardinalities (number of rows) for each attribute.
        :param maxTimeList: List of maximum execution times for each attribute.
        :param algo1: Enum value (AlgoEnum) corresponding to the first algorithm.
        :param algo2: Enum value (AlgoEnum) corresponding to the second algorithm.
        :param latexFilePath: Path where the LaTeX output file will be saved.
        :param scaleX: Width of the plot in points (default 280).
        :param scaleY: Height of the plot in points (default 280).
        :param attributes: List of attributes (typically [3, 6, 9]) to generate the plots for.
        :param scaleType: Scaling type for axes, can be "LinX/LinY", "LogX/LinY", "LinX/LogY", or "LogX/LogY".
        """
        self.path += latexFilePath
        algo1_name = algo1.value[0]
        algo2_name = algo2.value[0]

        # Define color styles
        color_styles = []
        for i, color in enumerate(self.colors[:2]):
            rgb = self.get_rgb_value(color)
            color_styles.append(f"\\definecolor{{{color}}}{{RGB}}{{{rgb}}}")
            color_styles.append(
                f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},"
                f"small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}"
            )

        latex_lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            *color_styles,
            r"\begin{document}"
        ]

        for i in range(len(attributes)):
            maxTime = roundtoNearestThousand(maxTimeList[i])  # Round maxTime to nearest thousand
            print(maxTime)

            # Set the scaling type
            is_log_x = 'LogX' in scaleType
            is_log_y = 'LogY' in scaleType

            # Calculate scaling ratios based on the chosen scale type
            if is_log_x:
                ratioX = scaleX / math.log(maxRowsList[i] + 1)  # Logarithmic scale for X
            else:
                ratioX = scaleX / maxRowsList[i]  # Linear scale for X

            if is_log_y:
                ratioY = scaleY / math.log(maxTime + 1)  # Logarithmic scale for Y
            else:
                ratioY = scaleY / maxTime  # Linear scale for Y

            # Algo 1 line and points
            line1 = f"\\draw[{self.colors[0]}, line width=2pt]"
            points1 = []
            for k in sorted(timeDict1.keys()):
                x = int(round(math.log(k + 1) * ratioX)) if is_log_x else int(round(k * ratioX))
                y = int(round(math.log(timeDict1[k][i] + 1) * ratioY)) if is_log_y else int(
                    round(timeDict1[k][i] * ratioY))
                line1 += f"({x}pt, {y}pt) -- "
                points1.append(f"\\filldraw[color=black, fill={self.colors[0]}] ({x}pt, {y}pt) circle (2pt);")
            line1 = line1.rstrip(" -- ") + ";"

            # Algo 2 line and points
            line2 = f"\\draw[{self.colors[1]}, line width=2pt]"
            points2 = []
            for k in sorted(timeDict2.keys()):
                x = int(round(math.log(k + 1) * ratioX)) if is_log_x else int(round(k * ratioX))
                y = int(round(math.log(timeDict2[k][i] + 1) * ratioY)) if is_log_y else int(
                    round(timeDict2[k][i] * ratioY))
                line2 += f"({x}pt, {y}pt) -- "
                points2.append(f"\\filldraw[color=black, fill={self.colors[1]}] ({x}pt, {y}pt) circle (2pt);")
            line2 = line2.rstrip(" -- ") + ";"

            # Axes graduations
            x_axis = "        \\foreach \\x/\\xtext in {\n"
            if is_log_x:
                log_steps = [math.log(s + 1) for s in range(0, maxRowsList[i] + 1, maxRowsList[i] // 5)]
                for step in log_steps:
                    value = roundtoNearestTen(math.exp(step))
                    x_axis += f"            {int(step * ratioX)}pt/${value}$, \n"
            else:
                for step in [scaleX * s / 5 for s in range(6)]:
                    value = roundtoNearestTen(maxRowsList[i] * (step / scaleX))
                    x_axis += f"            {int(step)}pt/${value}$, \n"
            x_axis = (x_axis.rstrip(", \n")
                      + "} {\n"
                      + "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below, font=\\small] {\\xtext\\strut};\n"
                      + "        }")

            y_axis = "        \\foreach \\y/\\ytext in {\n"
            if is_log_y:
                log_steps = [math.log(s + 1) for s in range(0, maxTime + 1, maxTime // 5)]
                for step in log_steps:
                    adjusted_value = roundtoNearestTen(math.exp(step))
                    y_axis += f"            {int(step * ratioY)}pt/${adjusted_value}$, \n"
            else:
                for step in [scaleY * s / 5 for s in range(5)]:
                    adjusted_value = round(maxTime * (step / (scaleY * 0.8)), 2)
                    y_axis += f"            {int(step)}pt/${adjusted_value}$, \n"
            y_axis = (y_axis.rstrip(", \n")
                      + "} {\n"
                      + "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left, font=\\small] {\\ytext\\strut};\n"
                      + "        }")

            tikz_block = [
                f"    % Graph for {attributes[i]} attributes",
                r"    \begin{tikzpicture}[",
                f"        line join=bevel,",
                f"        big{self.colors[0]}node/.style={{shape=circle, fill={self.colors[0]}, draw=black, line width=1pt}},",
                f"        big{self.colors[1]}node/.style={{shape=circle, fill={self.colors[1]}, draw=black, line width=1pt}},",
                f"        small{self.colors[0]}node/.style={{circle, fill={self.colors[0]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},",
                f"        small{self.colors[1]}node/.style={{circle, fill={self.colors[1]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}",
                r"    ]",
                r"        % Axes",
                f"        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};",
                f"        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south, font=\\large] {{Response time in s}};",
                r"        % Axis graduation",
                x_axis,
                y_axis,
                r"        % Lines",
                f"        {line1}",
                f"        {line2}",
                r"        % Points",
                *["        " + pt for pt in points1],
                *["        " + pt for pt in points2],
                r"        % Caption -",
                r"        \matrix [draw=none, fill=white, fill opacity=0.7, text opacity=1,",
                r"                 above right=0.5cm and 0cm of current bounding box.north west,",
                r"                 nodes={font=\small, anchor=west}] {",
                f"            \\node [small{self.colors[0]}node, label=right:{algo1_name} with {attributes[i]} attributes] {{}}; \\\\",
                f"            \\node [small{self.colors[1]}node, label=right:{algo2_name} with {attributes[i]} attributes] {{}}; \\\\",
                r"        };",
                r"    \end{tikzpicture}"
            ]

            latex_lines.extend(tikz_block)

        latex_lines.append(r"\end{document}")
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        print(self.latexCode)
        self.render()

    def threeAlgoComparaison369LatexLog(self, timeDict1, timeDict2, timeDict3, maxRowsList, maxTimeList, algo1, algo2,
                                        algo3,
                                        latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9],
                                        scaleType="LinX/LinY"):
        """
        Generate LaTeX code to compare three algorithms across multiple attributes
        with optional logarithmic scaling for X and/or Y axes.

        :param timeDict1: Time dictionary for the first algorithm.
        :param timeDict2: Time dictionary for the second algorithm.
        :param timeDict3: Time dictionary for the third algorithm.
        :param maxRowsList: List of maximum row counts per attribute (3, 6, 9).
        :param maxTimeList: List of maximum execution times per attribute (3, 6, 9).
        :param algo1: Enum value (AlgoEnum) corresponding to the first algorithm.
        :param algo2: Enum value (AlgoEnum) corresponding to the second algorithm.
        :param algo3: Enum value (AlgoEnum) corresponding to the third algorithm.
        :param latexFilePath: Output path where the generated LaTeX file will be saved.
        :param scaleX: Width of the generated graph (in pt, default 280).
        :param scaleY: Height of the generated graph (in pt, default 280).
        :param attributes: List of attributes to generate graphs for (default [3, 6, 9]).
        :param scaleType: Type of scaling on X and Y axes ("LinX/LinY", "LogX/LinY", "LinX/LogY", or "LogX/LogY").
        """

        self.path += latexFilePath
        algo_names = [algo1.value[0], algo2.value[0], algo3.value[0]]
        timeDicts = [timeDict1, timeDict2, timeDict3]

        # Define color styles
        color_styles = []
        for i, color in enumerate(self.colors[:3]):
            color_value, color_format = self.get_rgb_value(color)
            color_styles.append(f"\\definecolor{{{color}}}{{{color_format}}}{{{color_value}}}")
            color_styles.append(
                f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},"
                f"small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}"
            )

        latex_lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            *color_styles,
            r"\begin{document}"
        ]

        # Determine scaling type
        is_log_x = 'LogX' in scaleType
        is_log_y = 'LogY' in scaleType

        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]

            maxTime = roundtoNearestThousand(maxTimeList[i])

            ratioX = scaleX / math.log(maxRows + 1) if is_log_x else scaleX / maxRows
            ratioY = scaleY / math.log(maxTime + 1) if is_log_y else scaleY / maxTime

            # Generate lines and points
            lines = []
            points = []
            for j, timeDict in enumerate(timeDicts):
                color = self.colors[j]
                line = f"\\draw[{color}, line width=2pt]"
                point_set = []
                for k in sorted(timeDict.keys()):
                    x = int(round(math.log(k + 1) * ratioX)) if is_log_x else int(round(k * ratioX))
                    yval = timeDict[k][i]
                    y = int(round(math.log(yval + 1) * ratioY)) if is_log_y else int(round(yval * ratioY))
                    line += f"({x}pt, {y}pt) -- "
                    point_set.append(f"\\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);")
                line = line.rstrip(" -- ") + ";"
                lines.append(line)
                points.append(point_set)

            # X axis graduations
            x_axis = "        \\foreach \\x/\\xtext in {\n"
            if is_log_x:
                log_steps = [math.log(s + 1) for s in range(0, maxRows + 1, max(1, maxRows // 5))]
                for step in log_steps:
                    value = roundtoNearestTen(math.exp(step))
                    x_axis += f"            {int(step * ratioX)}pt/${value}$, \n"
            else:
                for step in [scaleX * s / 5 for s in range(6)]:
                    value = roundtoNearestTen(maxRows * (step / scaleX))
                    x_axis += f"            {int(step)}pt/${value}$, \n"
            x_axis = (
                    x_axis.rstrip(", \n") +
                    "} {\n            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below, font=\\small] {\\xtext\\strut};\n        }"
            )

            # Y axis graduations
            y_axis = "        \\foreach \\y/\\ytext in {\n"
            if is_log_y:
                log_steps = [math.log(s + 1) for s in range(0, maxTime + 1, max(1, maxTime // 5))]
                for step in log_steps:
                    value = roundtoNearestTen(math.exp(step))
                    y_axis += f"            {int(step * ratioY)}pt/${value}$, \n"
            else:
                for step in [scaleY * s / 5 for s in range(6)]:
                    adjusted_value = round(maxTime * (step / (scaleY * 0.8)), 2)
                    y_axis += f"            {int(step)}pt/${adjusted_value}$, \n"
            y_axis = (
                    y_axis.rstrip(", \n") +
                    "} {\n            \\draw (2pt, \\y) -- (-2pt, \\y) node[left, font=\\small] {\\ytext\\strut};\n        }"
            )

            tikz_block = [
                f"    % Graph for {attr} attributes",
                r"    \begin{tikzpicture}[",
                r"        line join=bevel,",
                *[
                    f"        small{self.colors[j]}node/.style={{circle, fill={self.colors[j]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},"
                    for j in range(3)
                ],
                r"    ]",
                r"        % Axes",
                f"        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};",
                f"        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south, font=\\large] {{Response time in s}};",
                r"        % Axis graduation",
                x_axis,
                y_axis,
                r"        % Lines",
                *["        " + l for l in lines],
                r"        % Points",
                *[f"        {pt}" for point_set in points for pt in point_set],
                r"        % Caption",
                r"        \matrix [draw=none, fill=white, fill opacity=0.7, text opacity=1,",
                r"                 above right=0.5cm and 0cm of current bounding box.north west,",
                r"                 nodes={font=\small, anchor=west}] {",
                *[
                    f"            \\node [small{self.colors[j]}node, label=right:{algo_names[j]} with {attr} attributes] {{}}; \\\\"
                    for j in range(3)
                ],
                r"        };",
                r"    \end{tikzpicture}",
                r"\clearpage"
            ]

            latex_lines.extend(tikz_block)

        latex_lines.append(r"\end{document}")
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        self.render()

    def threeAlgoComparaison369Latex(self, timeDict1, timeDict2, timeDict3, maxRowsList, maxTimeList, algo1, algo2,
                                     algo3, latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9]):
        """
        Generate LaTeX code for comparing three algorithms across 3, 6, and 9 attributes
        with separate graphs for each attribute.

        :param timeDict1: Time dictionary for the first algorithm.
        :param timeDict2: Time dictionary for the second algorithm.
        :param timeDict3: Time dictionary for the third algorithm.
        :param maxRowsList: List of maximum row counts for each attribute (3, 6, 9).
        :param maxTimeList: List of maximum execution times for each attribute (3, 6, 9).
        :param algo1: Enum value (AlgoEnum) of the first algorithm.
        :param algo2: Enum value (AlgoEnum) of the second algorithm.
        :param algo3: Enum value (AlgoEnum) of the third algorithm.
        :param latexFilePath: Output path where the LaTeX file will be saved.
        :param scaleX: Width of the chart in points (default is 280).
        :param scaleY: Height of the chart in points (default is 280).
        :param attributes: List of attributes to generate the graphs for (default [3, 6, 9]).
        """
        self.path += latexFilePath
        algo_names = [algo1.value[0], algo2.value[0], algo3.value[0]]
        timeDicts = [timeDict1, timeDict2, timeDict3]

        # Define color styles
        color_styles = []
        for i, color in enumerate(self.colors[:3]):
            rgb = self.get_rgb_value(color)
            color_styles.append(f"\\definecolor{{{color}}}{{RGB}}{{{rgb}}}")
            color_styles.append(
                f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},"
                f"\nsmall{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}"
            )

        latex_lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            *color_styles,
            r"\begin{document}"
        ]

        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]
            maxTime = maxTimeList[i]

            maxTime = roundtoNearestThousand(maxTime)


            ratioX = scaleX / maxRows
            ratioY = scaleY / maxTime

            # Build the lines and points for each algorithm
            lines = []
            points = []
            for j, timeDict in enumerate(timeDicts):
                color = self.colors[j]
                print(color)
                line = f"\\draw[{color}, line width=2pt]"
                point_set = []
                for k in sorted(timeDict.keys()):
                    x = int(round(k * ratioX))
                    y = int(round(timeDict[k][i] * ratioY * 0.8))
                    line += f"({x}pt, {y}pt) -- "
                    point_set.append(f"\\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);")
                line = line.rstrip(" -- ") + ";"
                lines.append(line)
                points.append(point_set)

            x_axis = "        \\foreach \\x/\\xtext in {\n"
            for step in [scaleX * s / 5 for s in range(6)]:
                value = round(maxRows * (step / scaleX), 1)
                x_axis += f"            {int(step)}pt/${value}$, \n"
            x_axis = (
                    x_axis.rstrip(", \n")
                    + "} {\n"
                    + "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n"
                    + "        }"
            )

            y_axis = "        \\foreach \\y/\\ytext in {\n"
            # On ajuste les graduations Y pour que la plus haute soit à 80% de la hauteur du graphique
            for step in [scaleY * s / 5 for s in range(5)]:
                value = round(maxTime * (step / scaleY), 2)  # Calculer les valeurs réelles
                adjusted_value = round(maxTime * (step / (scaleY * 0.8)), 2)  # Ajuster pour l'échelle à 80%
                y_axis += f"            {int(step)}pt/${adjusted_value}$, \n"
            y_axis = (
                    y_axis.rstrip(", \n")
                    + "} {\n"
                    + "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n"
                    + "        }"
            )

            tikz_block = [
                f"    % Graph for {attr} attributes",
                r"    \begin{tikzpicture}[",
                f"        line join=bevel,",
                f"        small{self.colors[0]}node/.style={{circle, fill={self.colors[0]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},",
                f"        small{self.colors[1]}node/.style={{circle, fill={self.colors[1]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},",
                f"        small{self.colors[2]}node/.style={{circle, fill={self.colors[2]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}",
                r"    ]",
                r"        % Axes",
                f"        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};",
                f"        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};",
                # Garde l'échelle Y totale
                r"        % Axis graduation",
                x_axis,
                y_axis,
                r"        % Lines",
                f"        {lines[0]}",
                f"        {lines[1]}",
                f"        {lines[2]}",
                r"        % Points",
                *["        " + pt for pt in points[0]],
                *["        " + pt for pt in points[1]],
                *["        " + pt for pt in points[2]],
                r"        % Caption",
                r"        \matrix [left=0cm of current bounding box.north east] at (current bounding box.north east) {",
                f"            \\node [small{self.colors[0]}node, label=right:{algo_names[0]} with {attr} attributes] {{}}; \\\\",
                f"            \\node [small{self.colors[1]}node, label=right:{algo_names[1]} with {attr} attributes] {{}}; \\\\",
                f"            \\node [small{self.colors[2]}node, label=right:{algo_names[2]} with {attr} attributes] {{}}; \\\\",
                r"        };",
                r"    \end{tikzpicture}"
            ]

            latex_lines.extend(tikz_block)

        latex_lines.append(r"\end{document}")
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        self.render()

    def fiveAlgoComparaison369Latex(self, timeDicts, maxRowsList, maxTimeList, algos, latexFilePath="", scaleX=280,
                                    scaleY=280, attributes=[3, 6, 9]):
        """
        Create LaTeX code to compare five algorithms across 3, 6, and 9 attributes,
        each plotted separately.

        :param timeDicts: List of time dictionaries for each algorithm.
        :param maxRowsList: List of maximum cardinalities (rows) for each attribute set.
        :param maxTimeList: List of maximum execution times for each attribute set.
        :param algos: List of algorithm enums (AlgoEnum) representing each algorithm.
        :param latexFilePath: Path to the output LaTeX file.
        :param scaleX: Width of the plot in points (default 280).
        :param scaleY: Height of the plot in points (default 280).
        :param attributes: List of attributes (default [3, 6, 9]) for which the comparison is made.
        """
        self.path += latexFilePath
        algo_names = [algo.value[0] for algo in algos]

        # Define color styles
        color_styles = []
        for color in self.colors[:5]:
            rgb_value, mode = self.get_rgb_value(color)
            color_styles.append(f"\\definecolor{{{color}}}{{{mode}}}{{{rgb_value}}}")
            color_styles.append(
                f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},"
                f"small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}"
            )

        latex_lines = [
            r"\documentclass[tikz, border=10pt]{standalone}",
            r"\usepackage{tikz}",
            r"\usetikzlibrary{arrows.meta, shapes, positioning}",
            r"\usepackage{xcolor}",
            *color_styles,
            r"\begin{document}"
        ]

        # Loop over each attribute set (3, 6, 9 attributes)
        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]
            maxTime = roundtoNearestThousand(maxTimeList[i])

            heightMaxTick = scaleY * 0.8
            ratioX = scaleX / maxRows
            ratioY = heightMaxTick / maxTime

            lines = []
            points = []

            # Draw lines and points for each algorithm
            for j, timeDict in enumerate(timeDicts):
                color = self.colors[j]
                line = f"\\draw[{color}, line width=2pt]"
                point_set = []
                for k in sorted(timeDict.keys()):
                    x = int(round(int(k) * ratioX))
                    y = int(round(timeDict[k][i] * ratioY))
                    line += f"({x}pt, {y}pt) -- "
                    point_set.append(f"\\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);")
                line = line.rstrip(" -- ") + ";"
                lines.append(line)
                points.append(point_set)

            # Generate X-axis graduations
            x_axis = "        \\foreach \\x/\\xtext in {\n"
            for step in [scaleX * s / 5 for s in range(6)]:
                value = round(maxRows * (step / scaleX), 1)
                x_axis += f"            {int(step)}pt/${value}$, \n"
            x_axis = x_axis.rstrip(", \n") + "} {\n"
            x_axis += "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n        }"

            # Generate Y-axis graduations
            y_axis = "        \\foreach \\y/\\ytext in {\n"
            for step in range(8):
                pos = int(round(heightMaxTick * (step / 7)))
                value = roundtoNearestTen(maxTime * (step / 7))
                y_axis += f"            {pos}pt/${value}$, \n"
            y_axis = y_axis.rstrip(", \n") + "} {\n"
            y_axis += "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n        }"

            # Construct TikZ picture block
            tikz_block = [
                f"    % Graph for {attr} attributes",
                r"    \begin{tikzpicture}[",
                r"        line join=bevel,",
                *[
                    f"        small{self.colors[j]}node/.style={{circle, fill={self.colors[j]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},"
                    for j in range(5)
                ],
                r"    ]",
                r"        % Axes",
                f"        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};",
                f"        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};",
                r"        % Axis graduation",
                x_axis,
                y_axis,
                r"        % Lines",
                *["        " + l for l in lines],
                r"        % Points",
                *[f"        {pt}" for point_set in points for pt in point_set],
                r"        % Caption",
                r"        \matrix [left=0cm of current bounding box.north east] at (current bounding box.north east) {",
                *[
                    f"            \\node [small{self.colors[j]}node, label=right:{algo_names[j]} with {attr} attributes] {{}}; \\\\"
                    for j in range(5)
                ],
                r"        };",
                r"    \end{tikzpicture}"
            ]

            latex_lines.extend(tikz_block)

        latex_lines.append(r"\end{document}")

        # Finalize and render LaTeX
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        self.render()

    def coskySqlComparaisonLatex(self, timeDict, maxRows, maxTime, latexFilePath, scaleX=280, scaleY=280):
        """
        Create a LaTeX document that plots the execution time of CoSky SQL queries
        across 3, 6, and 9 attributes on a 2D graph.

        :param timeDict: Dictionary containing execution times by number of rows.
        :param maxRows: Maximum number of rows considered.
        :param maxTime: Maximum execution time observed.
        :param latexFilePath: Path where the resulting LaTeX file will be saved.
        :param scaleX: Width of the graph in points (default 280pt).
        :param scaleY: Height of the graph in points (default 280pt).
        """
        self.path += latexFilePath

        attributes = [3, 6, 9]
        colors = self.colors[:3]
        attr_names = ["3 attributes", "6 attributes", "9 attributes"]

        # Clean and sort the dictionary keys
        time_dict_clean = {int(k): v for k, v in timeDict.items()}
        time_dict_clean = dict(sorted(time_dict_clean.items()))

        # Find the maximum Y value across all columns
        global_max_time = max(
            max(float(row[i]) for row in time_dict_clean.values())
            for i in range(3)
        )
        global_max_time_rounded = smart_roundup(global_max_time)

        heightMaxTick = scaleY * 0.8
        ratio_y = heightMaxTick / global_max_time_rounded
        ratio_x = scaleX / max(time_dict_clean.keys())

        # Start LaTeX code
        self.latexCode = r"""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{tikz}
    \usepackage{xcolor}
    \usepackage{graphicx}
    \usepackage{amsmath}
    \usepackage{caption}

    \definecolor{brightmaroon}{RGB}{195,33,72}
    \definecolor{cyan}{RGB}{0,255,255}
    \definecolor{skyblue}{RGB}{135,206,235}

    \begin{document}
    \begin{figure}[htbp]
        \centering
        \resizebox{.75\linewidth}{!}{
            \begin{tikzpicture}[line join=bevel,
                bigbrightmaroonnode/.style={shape=circle, fill=brightmaroon, draw=black, line width=1pt},
                bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
                bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}]
    """

        # Draw axes
        self.latexCode += f"""        % Axes
            \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};
            \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};
    """

        # Draw X-axis graduations
        self.latexCode += "        % X-axis ticks\n"
        self.latexCode += "        \\foreach \\x/\\xtext in {\n"
        for i in range(6):
            step = int(scaleX * i / 5)
            value = int(max(time_dict_clean.keys()) * i / 5)
            self.latexCode += f"            {step}pt/${value}$,\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n        }\n"

        # Draw Y-axis graduations
        self.latexCode += "        % Y-axis ticks\n"
        self.latexCode += "        \\foreach \\y/\\ytext in {\n"
        for s in range(6):
            pos = int(heightMaxTick * s / 5)
            val = int(global_max_time_rounded * s / 5)
            self.latexCode += f"            {pos}pt/${val}$,\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n        }\n"

        # Draw curves and points
        for i in range(3):
            color = colors[i]
            line = f"        \\draw[{color}, line width=2pt]"
            points = ""
            for k in time_dict_clean:
                x = int(round(k * ratio_x))
                y = int(round(time_dict_clean[k][i] * ratio_y))
                line += f" ({x}pt, {y}pt) --"
                points += f"        \\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);\n"
            self.latexCode += line.rstrip(" --") + ";\n" + points + "\n"

        # Legend
        self.latexCode += r"""        % Caption
            \matrix [below left] at (current bounding box.north east) {
    """
        for i in range(3):
            self.latexCode += f"            \\node [big{colors[i]}node, label=right:CoSky 'SQL query' with {attributes[i]} attributes] {{}}; \\\\\n"
        self.latexCode += r"""        };
            \end{tikzpicture}
        }
        \caption{Execution time of CoSky 'SQL queries' with 3, 6, and 9 attributes}
        \label{fig:cosky_sql_comparaison}
    \end{figure}
    \end{document}"""

        self.addLatexCode(self.latexCode)
        self.render()

    def CoskyComparaisonNColumn(self, column, scaleX=300, scaleY=300, scaleType="LinX/LinY"):
        """
        Create a LaTeX file that draws a single graph for CoSky SQL algorithm with a given number of attributes (3, 6, or 9).

        Supports both linear and logarithmic axis scaling.

        :param column: Number of attributes (must be 3, 6, or 9).
        :param scaleX: Width of the graph in points (default 300pt).
        :param scaleY: Height of the graph in points (default 300pt).
        :param scaleType: String to specify scaling ('LinX/LinY', 'LogX/LogY', etc.).
        """
        import math, json

        column = int(column)
        dataPath = "../../Assets/LatexData/OneAlgoData/CoskySql/OneColumnsDatas/"
        if column == 3:
            self.path += "OneAlgoComparaison/CoskySql3.tex"
            dataPath += "ExecutionCoskySql310^9.json"
        if column == 6:
            self.path += "CoskySql6.tex"
            dataPath += "ExecutionCoskySql6.json"
        if column == 9:
            self.path += "CoskySql9.tex"
            dataPath += "ExecutionCoskySql9.json"

        with open(dataPath, "r") as file:
            data = json.load(file)

        timeDict = data["time_data"]
        maxRows = data["max_rows"]
        maxTime = data["max_time"]

        is_log_x = "LogX" in scaleType
        is_log_y = "LogY" in scaleType

        heightMaxTick = scaleY * 0.8
        ratio_x = scaleX / math.log(maxRows + 1) if is_log_x else scaleX / maxRows
        ratio_y = heightMaxTick / math.log(maxTime + 1) if is_log_y else heightMaxTick / maxTime

        # Start LaTeX document
        self.latexCode = r"""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage[T1]{fontenc}
    \usepackage{tikz}
    \usepackage{xcolor}
    \usepackage{caption}
    \usepackage{amsmath}

    \definecolor{skyblue}{RGB}{135,206,235}
    \definecolor{brightmaroon}{RGB}{195, 33, 72}

    \usetikzlibrary{arrows.meta, shapes, positioning, matrix}

    \begin{document}

    \begin{figure}[htbp]
        \centering
        \resizebox{.45\linewidth}{!}{
            \begin{tikzpicture}[
                line join=bevel,
                bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
                bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}
            ]
                % Axes
                \draw[-stealth] (0pt, 0pt) -- (""" + str(scaleX) + r"""pt, 0pt) node[anchor=north west, yshift=15pt] {Cardinality};
                \draw[-stealth] (0pt, 0pt) -- (0pt, """ + str(scaleY) + r"""pt) node[anchor=south] {Response time (s)};
                % X-axis ticks
    """
        # Generate X-axis graduations
        tick_count = 6
        self.latexCode += "            \\foreach \\x/\\xtext in {\n"
        for i in range(tick_count + 1):
            ratio = i / tick_count
            if is_log_x:
                log_val = math.log(maxRows + 1) * ratio
                raw_val = int(math.exp(log_val)) - 1
                pos = int(log_val * ratio_x)
            else:
                raw_val = int(maxRows * ratio)
                pos = int(scaleX * ratio)

            if raw_val <= 0:
                label = "$0$"
            else:
                exponent = int(math.log10(raw_val)) if raw_val > 0 else 0
                base = int(raw_val / (10 ** exponent)) if exponent != 0 else raw_val
                label = f"${base} \\times 10^{{{exponent}}}$" if exponent > 0 else f"${raw_val}$"
            self.latexCode += f"                {pos}pt/{label},\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "                \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n            }\n"

        # Generate Y-axis graduations
        y_steps = 6
        self.latexCode += "\n            % Y-axis ticks\n"
        self.latexCode += "            \\foreach \\y/\\ytext in {\n"
        for i in range(y_steps + 1):
            ratio = i / y_steps
            if is_log_y:
                log_val = math.log(maxTime + 1) * ratio
                val = int(math.exp(log_val)) - 1
                pos = int(log_val * ratio_y)
            else:
                val = maxTime * ratio
                pos = int(heightMaxTick * ratio)
            label = f"${round(val, 1)}$"
            self.latexCode += f"                {pos}pt/{label},\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "                \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n            }\n"

        # Draw the curve and points
        self.latexCode += "\n            % Curve and points\n"
        line = f"            \\draw[skyblue, line width=2pt]"
        points = ""
        for k in sorted(timeDict.keys(), key=lambda x: int(x)):
            x_raw = int(k)
            y_raw = timeDict[k][0]
            x = int(round(math.log(x_raw + 1) * ratio_x)) if is_log_x else int(round(x_raw * ratio_x))
            y = int(round(math.log(y_raw + 1) * ratio_y)) if is_log_y else int(round(y_raw * ratio_y))
            line += f" ({x}pt, {y}pt) --"
            points += f"            \\filldraw[color=black, fill=skyblue] ({x}pt, {y}pt) circle (2pt);\n"
        self.latexCode += line.rstrip(" --") + ";\n" + points

        # Legend and caption
        self.latexCode += r"""
                % Legend
                \matrix [below left, draw=none] at (current bounding box.north east) {
                    \node [bigskybluenode, label=right:CoSky ``SQL'' with """ + str(column) + r""" attributes] {}; \\
                };
            \end{tikzpicture}
        }
        \caption{CoSky SQL: response time for """ + str(column) + r""" attributes}
        \label{fig:cosky_sql_response_time_""" + str(column) + r"""_attributes}
    \end{figure}

    \end{document}
    """

        self.addLatexCode(self.latexCode)
        self.render()


def roundtoNearestThousand(value):
    """
    Round the given value to the nearest thousand.

    :param value: The value to round.
    :return: Rounded value.
    """
    if value == 0:
        return 0
    return round(value / 1000) * 1000


def round_up_to_multiple(value, multiple):
    """
    Round up the given value to the next multiple of 'multiple'.

    :param value: The value to round.
    :param multiple: The multiple to round up to.
    :return: Rounded value.
    """
    return int(math.ceil(value / multiple) * multiple)


def roundtoNearestTen(value):
    """
    Round the given value to the nearest ten.

    :param value: The value to round.
    :return: Rounded value.
    """
    if value == 0:
        return 0
    return round(value / 10) * 10


def roundToNearestN(value, n):
    """
    Round the given value to the nearest N.

    :param value: The value to round.
    :param n: The nearest number to round to.
    :return: Rounded value.
    """
    if value == 0:
        return 0
    return round(value / (n - 1)) * (n - 1)


def smart_roundup(value):
    """
    Smartly round up a value to a "nice" upper bound (for axis scaling purposes).

    :param value: The value to round up.
    :return: Rounded up value.
    """
    if value == 0:
        return 10
    magnitude = 10 ** (len(str(int(value))) - 1)
    base = (int(value) // magnitude + 1) * magnitude
    return base


if __name__ == "__main__":
    coskyLatex = LatexMaker()
    path = "../../Assets/LatexData/OneAlgoData/CoskySql/ThreeColumnsData/"

    # Generate a LaTeX file for CoskySQL with 3, 6, and 9 attributes
    timeDict, maxRow, maxTime = coskyLatex.getData(path + "ExecutionCoskySql369.json")
    coskyLatex.coskySqlComparaisonLatex(
        timeDict,
        maxRow,
        maxTime,
        latexFilePath="OneAlgoComparaison/CoskySql369.tex",
        scaleX=280,
        scaleY=280
    )

    print_red("1./ Compare three algorithms")
    print_red("2./ Compare two algorithms")

    a = input("Choice: ")
    if a == "1":
        json_paths = [
            path + "OneAlgoData/ExecutionCoskySql369.json",
            path + "OneAlgoData/ExecutionCoskyAlgo369.json",
            path + "OneAlgoData/ExecutionRankSky369.json"
        ]
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)

        coskyLatex.threeAlgoComparaison369Latex(
            timeDicts[0], timeDicts[1], timeDicts[2],
            maxRowsList, maxTimeList,
            AlgoEnum.CoskySql,
            AlgoEnum.CoskyAlgorithme,
            AlgoEnum.RankSky,
            latexFilePath="ThreeAlgosComparaison/RankSkyCoskySqlAlgo369.tex"
        )
    elif a == "2":
        json_paths = [
            path + "OneAlgoData/ExecutionCoskySql369.json",
            path + "OneAlgoData/ExecutionCoskyAlgo369.json"
        ]

        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)
        coskyLatex.twoAlgoComparaison369Latex(
            timeDicts[0],
            timeDicts[1],
            maxRowsList,
            maxTimeList,
            AlgoEnum.CoskySql,
            AlgoEnum.CoskyAlgorithme,
            latexFilePath="TwoAlgosComparaison/CoskySqlAlgo369.tex"
        )
    if a == "3":
        json_paths = [
            path + "OneAlgoData/ExecutionCoskySql369.json",
            path + "OneAlgoData/ExecutionCoskyAlgo369.json"
        ]
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)
        coskyLatex.twoAlgoComparaison369LatexLog(
            timeDicts[0],
            timeDicts[1],
            maxRowsList,
            maxTimeList,
            AlgoEnum.CoskySql,
            AlgoEnum.CoskyAlgorithme,
            latexFilePath="twoAlgosComparaison/CoskySqlAlgo369LogLogAxes.tex",
            scaleType="LinX/LogY",
        )
    if a == "5":
        json_paths = [
            path + "OneAlgoData/OneColumnData/ExecutionCoskySql3.json",
            path + "OneAlgoData/OneColumnData/ExecutionCoskyAlgo3.json",
            path + "OneAlgoData/OneColumnData/ExecutionRankSky3.json",
            path + "OneAlgoData/OneColumnData/ExecutionDpIdpDh3.json",
            path + "OneAlgoData/OneColumnData/ExecutionSkyIR3.json"
        ]
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths, attributes=[3])
        algos = [
            AlgoEnum.CoskySql,
            AlgoEnum.CoskyAlgorithme,
            AlgoEnum.RankSky,
            AlgoEnum.DpIdpDh,
            AlgoEnum.SkyIR
        ]
        coskyLatex.fiveAlgoComparaison369Latex(
            timeDicts,
            maxRowsList,
            maxTimeList,
            algos,
            latexFilePath="FiveAlgosComparaison/CoskySqlAlgoRankSkyDpIdpDhSkyIR369.tex",
            attributes=[3]
        )