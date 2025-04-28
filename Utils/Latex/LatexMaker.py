import json

from Utils.DisplayHelpers import print_red
from AlgoEnum import AlgoEnum
import math


class LatexMaker:
    """
    Class to create a latex document for the results of the algorithms
    """

    def __init__(self):
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
        """Add the latex code to the final document"""
        self.latexFinal += latexCode

    def render(self):
        """Render the latex code to a file"""
        print(self.path)
        with open(self.path, 'w') as file:
            file.write(self.latexCode)
        #writeJson(self.path, self.latexFinal)

    def getData(self, path):
        """
        Reads and processes JSON data from the given path.
        :param path: Path to the JSON file.
        :return: A tuple containing timeDict, maxRows, and maxTime.
        """
        with open(path, 'r') as file:
            data = json.load(file)  # Use json.load instead of json.loads for file objects

        # Assuming data is already a dictionary at this point
        timeDict = data.get("time_data", {})
        maxRows = data.get("max_rows", 0)
        maxTime = data.get("max_time", 0)


        return timeDict, maxRows, maxTime

    def get_rgb_value(self, color_name):
        """
        Return a tuple: (value, format) for the LaTeX \definecolor command.
        Ex: ('135,206,235', 'RGB') or ('C42043', 'HTML')
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
        Prepares the timeDicts, maxRowsList, and maxTimeList from JSON paths.
        Args:
            jsonPaths (list): List of JSON paths (1 per algorithm)
            attributes (list): Attributes to process (default [3, 6, 9])
        Returns:
            timeDicts: List of time dictionaries
            maxRowsList: List of max cardinalities per attribute
            maxTimeList: List of max execution times per attribute
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
        if value == 0:
            return 0
        return round(value / (n - 1)) * (n - 1)

    def twoAlgoComparaison369Latex(self, timeDict1, timeDict2, maxRowsList, maxTimeList, algo1, algo2,
                                   latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9]):
        """
        Generate clean and well-indented LaTeX code to compare two algorithms for multiple attributes.
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
        Generate LaTeX code to compare two algorithms for multiple attributes, with options for linear or logarithmic scaling.
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
                                     algo3, latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9],
                                     rounding_multiple=10):
        """
        Create LaTeX code for comparing three algorithms across 3, 6, 9 attributes,
        with separate scaling per graph.
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
                                    scaleY=280, attributes=[3, 6, 9], rounding_multiple=10):
        """
        Create LaTeX code for comparing five algorithms across 3, 6, 9 attributes,
        with separate scaling per graph.
        """
        self.path += latexFilePath
        algo_names = [algo.value[0] for algo in algos]

        # Define color styles with format
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

        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]
            maxTime = roundtoNearestThousand(maxTimeList[i])

            heightMaxTick = scaleY * 0.8
            ratioX = scaleX / maxRows
            ratioY = heightMaxTick / maxTime

            lines = []
            points = []

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

            # X-axis ticks
            x_axis = "        \\foreach \\x/\\xtext in {\n"
            for step in [scaleX * s / 5 for s in range(6)]:
                value = round(maxRows * (step / scaleX), 1)
                x_axis += f"            {int(step)}pt/${value}$, \n"
            x_axis = x_axis.rstrip(", \n") + "} {\n"
            x_axis += "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n        }"

            # Y-axis ticks (maxTime à 80% hauteur)
            y_axis = "        \\foreach \\y/\\ytext in {\n"
            for step in range(8):
                pos = int(round(heightMaxTick * (step / 7)))
                value = roundtoNearestTen(maxTime * (step / 7))
                y_axis += f"            {pos}pt/${value}$, \n"
            y_axis = y_axis.rstrip(", \n") + "} {\n"
            y_axis += "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n        }"

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
        self.latexCode = "\n".join(latex_lines)
        self.addLatexCode(self.latexCode)
        self.render()

    def coskySqlComparaisonLatex(self, timeDict, maxRows, maxTime, latexFilePath, scaleX=280, scaleY=280):
        self.path += latexFilePath

        attributes = [3, 6, 9]
        colors = self.colors[:3]
        attr_names = ["3 attributes", "6 attributes", "9 attributes"]

        # Nettoyage et tri des clés
        time_dict_clean = {int(k): v for k, v in timeDict.items()}
        time_dict_clean = dict(sorted(time_dict_clean.items()))

        # Trouver le plus grand temps Y toutes colonnes confondues
        global_max_time = max(
            max(float(row[i]) for row in time_dict_clean.values())
            for i in range(3)
        )
        global_max_time_rounded = smart_roundup(global_max_time)

        heightMaxTick = scaleY * 0.8
        ratio_y = heightMaxTick / global_max_time_rounded
        ratio_x = scaleX / max(time_dict_clean.keys())

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

        # Axes
        self.latexCode += f"""        % Axes
            \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west, yshift=15pt] {{Cardinality}};
            \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};
    """

        # Graduation X
        self.latexCode += "        % X-axis ticks\n"
        self.latexCode += "        \\foreach \\x/\\xtext in {\n"
        for i in range(6):
            step = int(scaleX * i / 5)
            value = int(max(time_dict_clean.keys()) * i / 5)
            self.latexCode += f"            {step}pt/${value}$,\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "            \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n        }\n"

        # Graduation Y (commune à tous)
        self.latexCode += "        % Y-axis ticks\n"
        self.latexCode += "        \\foreach \\y/\\ytext in {\n"
        for s in range(6):
            pos = int(heightMaxTick * s / 5)
            val = round(global_max_time_rounded * s / 5, 2)
            self.latexCode += f"            {pos}pt/${val}$,\n"
        self.latexCode = self.latexCode.rstrip(",\n") + "} {\n"
        self.latexCode += "            \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n        }\n"

        # Courbes et points
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

        # Légende
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
        Create LaTeX code for CoSky SQL with 'column' attributes,
        with support for scientific/logarithmic X and/or Y axes.
        """
        import math, json

        column = int(column)
        dataPath = "../../Assets/LatexDatas/OneAlgoDatas/CoskySql/OneColumnsDatas/"
        match column:
            case 3:
                self.path += "OneAlgoComparaison/CoskySql3.tex"
                dataPath += "ExecutionCoskySql310^9.json"
            case 6:
                self.path += "CoskySql6.tex"
                dataPath += "ExecutionCoskySql6.json"
            case 9:
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

        # Y-axis ticks
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

        # Curve and points
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
    if value == 0:
        return 0
    return round(value / 1000) * 1000

def round_up_to_multiple(value, multiple):
    return int(math.ceil(value / multiple) * multiple)

def roundtoNearestTen(value):
    if value == 0:
        return 0
    return round(value / 10) * 10

def roundToNearestN(value, n):
    if value == 0:
        return 0
    return round(value / (n - 1)) * (n - 1)

def smart_roundup(value):
    if value == 0:
        return 10
    magnitude = 10 ** (len(str(int(value))) - 1)
    base = (int(value) // magnitude + 1) * magnitude
    return base



if __name__ == "__main__":
    coskyLatex = LatexMaker()
    path = "../../Assets/LatexDatas/OneAlgoDatas/CoskySql/ThreeColumnsDatas/"

    timeDict, maxRow, maxTime = coskyLatex.getData(path + "ExecutionCoskySql369.json")

    coskyLatex.coskySqlComparaisonLatex(
        timeDict,
        maxRow,
        maxTime,
        latexFilePath="OneAlgoComparaison/CoskySql369.tex",
        scaleX=280,
        scaleY=280
    )

    """timeDict, maxRow, maxTime = coskyLatex.getData(path + "OneAlgoDatas/ExecutionCoskySql369.json")
    coskyLatex.coskySqlComparaisonLatex(
        timeDict,
        maxRow,
        maxTime,
        latexFilePath="OneAlgoComparaison/CoskySql369.tex",
        scaleX=280,
        scaleY=280
    )"""



    """timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(
        [
            path + "OneAlgoDatas/ExecutionCoskySql369.json",
            path + "OneAlgoDatas/ExecutionCoskyAlgo369.json",
            path + "OneAlgoDatas/ExecutionRankSky369.json"
        ]
    )
    beauty_print("maxRowsList", maxRowsList)
    beauty_print("maxTimeList", maxTimeList)
    timeDict1 = timeDicts[0]
    timeDict2 = timeDicts[1]
    timeDict3 = timeDicts[2]
    algo1 = AlgoEnum.CoskySql
    algo2 = AlgoEnum.CoskyAlgorithme
    algo3 = AlgoEnum.RankSky
    coskyLatex.threeAlgoComparaison369LatexLog(
        timeDict1,
        timeDict2,
        timeDict3,
        maxRowsList,
        maxTimeList,
        algo1,
        algo2,
        algo3,
        latexFilePath="ThreeAlgosComparaison/CoskySqlAlgoRankSkyLinLog.tex",
        attributes=[3, 6, 9],
        scaleType="LinX/LogY",
    )"""

    print_red("1./ Comparaison de trois algorithmes")
    print_red("2./ Comparaison de deux algorithmes")

    a = input("Choix: ")
    if a == "1":
        json_paths = [
            path + "OneAlgoDatas/ExecutionCoskySql369.json",
            path + "OneAlgoDatas/ExecutionCoskyAlgo369.json",
            path + "OneAlgoDatas/ExecutionRankSky369.json"
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
            path + "OneAlgoDatas/ExecutionCoskySql369.json",
            path + "OneAlgoDatas/ExecutionCoskyAlgo369.json"
        ]

        # Appelle ta méthode utilitaire
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)

        # Puis appelle la fonction d'affichage
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
            path + "OneAlgoDatas/ExecutionCoskySql369.json",
            path + "OneAlgoDatas/ExecutionCoskyAlgo369.json"
        ]

        # Appelle ta méthode utilitaire
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)
        timeDict1 = timeDicts[0]
        timeDict2 = timeDicts[1]
        algo1 = AlgoEnum.CoskySql
        algo2 = AlgoEnum.CoskyAlgorithme
        coskyLatex.twoAlgoComparaison369LatexLog(
            timeDict1,
            timeDict2,
            maxRowsList,
            maxTimeList,
            algo1,
            algo2,
            latexFilePath="twoAlgosComparaison/CoskySqlAlgo369LogLogAxes.tex",
            scaleType="LinX/LogY",
        )
    if a == "5":
        json_paths = [
            path + "OneAlgoDatas/OneColumnDatas/ExecutionCoskySql3.json",
            path + "OneAlgoDatas/OneColumnDatas/ExecutionCoskyAlgo3.json",
            path + "OneAlgoDatas/OneColumnDatas/ExecutionRankSky3.json",
            path + "OneAlgoDatas/OneColumnDatas/ExecutionDpIdpDh3.json",
            path + "OneAlgoDatas/OneColumnDatas/ExecutionSkyIR3.json"
        ]
        # Appelle ta méthode utilitaire
        timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths, attributes=[3])
        algo1 = AlgoEnum.CoskySql
        algo2 = AlgoEnum.CoskyAlgorithme
        algo3 = AlgoEnum.RankSky
        algo4 = AlgoEnum.DpIdpDh
        algo5 = AlgoEnum.SkyIR
        algos = [algo1, algo2, algo3, algo4, algo5]
        coskyLatex.fiveAlgoComparaison369Latex(
            timeDicts,
            maxRowsList,
            maxTimeList,
            algos,
            latexFilePath="FiveAlgosComparaison/CoskySqlAlgoRankSkyDpIdpDhSkyIR369.tex",
            attributes = [3]
        )


