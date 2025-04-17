import json
import textwrap

from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.CoskySql import CoskySQL
from Utils.DisplayHelpers import beauty_print, print_red
from AlgoEnum import AlgoEnum


class LatexMaker:
    """
    Class to create a latex document for the results of the algorithms
    """

    def __init__(self):
        self.latexCode = ""
        self.latexFinal = ""
        self.colors = ["brightmaroon", "cyan", "skyblue"]
        self.path = "../../Assets/LatexFiles/"
        self.defineColor = """\\definecolor{aliceblue}{rgb}{0.94, 0.97, 1.0}
                                \\definecolor{skyblue}{rgb}{0.53, 0.81, 0.92}
                                \\definecolor{brightmaroon}{rgb}{0.95, 0.82, 0.85}"""

    def addLatexCode(self, latexCode):
        """Add the latex code to the final document"""
        self.latexFinal += latexCode

    def render(self):
        """Render the latex code to a file"""
        with open(self.path, "w") as f:
            f.write(self.latexFinal)

    def getData(self, path):
        """Get the data from the json file"""
        with open(path, "r") as f:
            data = f.read()
        data = json.loads(data)
        timeDict = data["time_data"]
        maxRows = data["max_rows"]
        maxTime = data["max_time"]
        return timeDict, maxRows, maxTime

    def get_rgb_value(self, color_name):
        """Map color names to RGB values"""
        color_map = {
            "brightmaroon": "195,33,72",
            "cyan": "0,255,255",
            "skyblue": "135,206,235"
        }
        return color_map.get(color_name, "0,0,0")

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
                all_times_per_attr[i].extend(
                    timeDict[k][i] for k in timeDict
                )

        maxRowsList = [max(all_max_rows)] * len(attributes)
        maxTimeList = [max(times) for times in all_times_per_attr]

        return timeDicts, maxRowsList, maxTimeList

    def oneAlgoComparaison(self, timeDict, maxRows, maxTime, algo, scaleX=280, scaleY=280, latexFilePath="",
                           isDebug=False):
        """
        Create the latex code for algorithm comparison for 3, 6, 9 columns
        """
        self.path += latexFilePath
        ratio_x = scaleX / maxRows
        ratio_y = scaleY / maxTime

        # Get the algorithm name from the enum
        algo_name = algo.value

        self.latexCode += """\\documentclass{article}
        \\usepackage[utf8]{inputenc}
        \\usepackage{tikz}
        \\usepackage{xcolor}
        \\usepackage{graphicx}
        \\usepackage{amsmath}
        \\usepackage{caption}

        \\definecolor{brightmaroon}{RGB}{195,33,72}
        \\definecolor{cyan}{RGB}{0,255,255}
        \\definecolor{skyblue}{RGB}{135,206,235}

        \\begin{document}
        \\begin{figure}[htbp]
        \\centering
        \\resizebox{.45\\linewidth}{!}{
        \\begin{tikzpicture}[line join=bevel,
        biggraynode/.style={shape=circle, fill=gray, draw=black, line width=1pt},
        bigbrightmaroonnode/.style={shape=circle, fill=brightmaroon, draw=black, line width=1pt},
        bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
        bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}]
        \\draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
        \\draw[-stealth] (0pt, 0pt) -- (0pt, 340pt) node[anchor=south] {Response time in s};
        """
        self.latexCode += """% X-axis ticks and labels
                \\foreach \\x/\\xtext in {0pt/$0$, 50pt/$""" + str(round(maxRows / 10, 1)) + """$, 100pt/$""" + str(
            round(maxRows / 5, 1)) + """$, 150pt/$""" + str(round(maxRows / 3.33, 1)) + """$, 200pt/$""" + str(
            round(maxRows / 2, 1)) + """$, 250pt/$""" + str(round(maxRows / 1.25, 1)) + """$, 300pt/$""" + str(
            round(maxRows, 1)) + """$} {
                  \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};
                }
                % Y-axis ticks and labels
                \\foreach \\y/\\ytext in {0pt/$0$, 40pt/$""" + str(round(maxTime / 10, 1)) + """$, 80pt/$""" + str(
            round(maxTime / 5, 1)) + """$, 120pt/$""" + str(round(maxTime / 3.33, 1)) + """$, 160pt/$""" + str(
            round(maxTime / 2, 1)) + """$, 200pt/$""" + str(round(maxTime / 1.25, 1)) + """$, 240pt/$""" + str(
            round(maxTime, 1)) + """$} {
                  \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};
                }
                """

        self.latexCode += "% Lines\n"
        line2 = ""
        for i in range(len(timeDict[min(timeDict.keys())])):
            line1Header = f"\\draw[{self.colors[i]}, line width=2pt]"
            line1 = ""
            for k in timeDict.keys():  # Tri des clés pour ordre correct
                k = int(k)
                x = int(round(k * ratio_x))
                y = int(round(timeDict[k][i] * ratio_y))
                line1 += f"({x}pt, {y}pt) -- "
                line2 += fr"\filldraw[color=black, fill={self.colors[i]}] ({x}pt, {y}pt) circle (2pt);"
                line2 += "\n"

            line1 = line1Header + line1.rstrip(" -- ") + ";\n"
            self.latexCode += line1
        self.latexCode += "% Points and labels\n"
        self.latexCode += line2

        # Dynamic caption based on algorithm Name
        self.latexCode += """%% Caption
        \\matrix [below left] at (current bounding box.north east) {
        \\node [bigbrightmaroonnode, label=right:""" + algo_name + """ with 9 attributes] {}; \\\\
        \\node [bigcyannode, label=right:""" + algo_name + """ with 6 attributes] {}; \\\\
        \\node [bigskybluenode, label=right:""" + algo_name + """ with 3 attributes] {}; \\\\
        };
        \\end{tikzpicture}
        }
        \\caption{""" + algo_name + """ response time for different attribute counts}
        \\label{fig:temps_de_reponse_""" + algo.name.lower() + """}
        \\end{figure}
        \\end{document}"""

        self.addLatexCode(self.latexCode)
        self.render()

        def twoAlgoComparaison369Latex(self, timeDict1, timeDict2, maxRows, maxTime, latexFilePath, scaleX=280,
                                       scaleY=280):
            """
            Create the latex code for the Cosky Sql and Algo comparison
            """
            self.path += latexFilePath
            ratioX = scaleX / maxRows
            ratioY = scaleY / maxTime

            self.latexCode = """
            \\documentclass[tikz, border=10pt]{standalone}
            \\usepackage{tikz}
            \\usetikzlibrary{arrows.meta, shapes, positioning}
            \\usepackage{xcolor}
            \\definecolor{brightmaroon}{RGB}{195,33,72}
            \\definecolor{cyan}{RGB}{0,255,255}
            \\definecolor{skyblue}{RGB}{135,206,235}
            \\begin{document}"""
            self.colors.pop(0)

            # For the Graphs
            drawSql = []
            drawAlgo = []
            filldrawSql = []
            filldrawAlgo = []
            for i in range(len(timeDict1[min(timeDict1.keys())])):
                # Sql part
                line2Sql = ""
                line1HeaderSql = f"\\draw[{self.colors[0]}, line width=2pt]"
                line1Sql = ""
                for k in timeDict1.keys():
                    k = int(k)
                    x = int(round(k * ratioX))
                    y = int(round(timeDict1[k][i] * ratioY))
                    line1Sql += f"({x}pt, {y}pt) -- "
                    line2Sql += fr"\filldraw[color=black, fill={self.colors[0]}] ({x}pt, {y}pt) circle (2pt);"
                    line2Sql += "\n"
                line1Sql = line1HeaderSql + line1Sql.rstrip(" -- ") + ";\n"
                drawSql.append(line1Sql)
                filldrawSql.append(line2Sql)

                # Algo part
                line2Algo = ""
                line1HeaderAlgo = f"\\draw[{self.colors[1]}, line width=2pt]"
                line1Algo = ""
                for k in timeDict2.keys():
                    k = int(k)
                    x = int(round(k * ratioX))
                    y = int(round(timeDict2[k][i] * ratioY))
                    line1Algo += f"({x}pt, {y}pt) -- "
                    line2Algo += fr"\filldraw[color=black, fill={self.colors[1]}] ({x}pt, {y}pt) circle (2pt);"
                    line2Algo += "\n"
                line1Algo = line1HeaderAlgo + line1Algo.rstrip(" -- ") + ";\n"
                drawAlgo.append(line1Algo)
                filldrawAlgo.append(line2Algo)

            """beauty_print("drawSql", drawSql)
            beauty_print("drawAlgo", drawAlgo)
            beauty_print("filldrawSql", filldrawSql)
            beauty_print("filldrawAlgo", filldrawAlgo)
            beauty_print("latexCode", self.latexCode)"""

            # ------------------------------ Graph 1 -------------------------------
            picture1 = """
            		\\begin{tikzpicture}[
            			line join=bevel,
            			bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
            			bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}
            			]

            			%% Draws
            			\draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
            			\draw[-stealth] (0pt, 0pt) -- (0pt, 310pt) node[anchor=south] {Response time in s};"""

            axisGraduation1 = """% Axis Graduation
                                \\foreach \\x/\\xtext in {0pt/$0$, 56pt/$""" + str(
                round(maxRows / 5, 1)) + """$, 112pt/$""" + str(
                round(maxRows * 2 / 5, 1)) + """$, 168pt/$""" + str(round(maxRows * 3 / 5, 1)) + """$, 224pt/$""" + str(
                round(maxRows * 4 / 5, 1)) + """$, 280pt/$""" + str(round(maxRows, 1)) + """$} {
                                    \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};
                                }
                                \\foreach \\y/\\ytext in {0pt/$0$, 9pt/$""" + str(
                round(maxTime / 5, 2)) + """$, 55pt/$""" + str(
                round(maxTime * 2 / 5, 2)) + """$, 110pt/$""" + str(round(maxTime * 3 / 5, 2)) + """$, 165pt/$""" + str(
                round(maxTime * 4 / 5, 2)) + """$, 220pt/$""" + str(round(maxTime, 2)) + """$} {
                                    \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};
                                }
                    """

            self.latexCode += (picture1 + "\n" + axisGraduation1 + "\n" + drawSql[0] +
                               "\n" + drawAlgo[0] + "\n" + filldrawSql[0] + "\n" + filldrawAlgo[0] + "\n")

            caption1 = """
                    %% Caption
                    \\matrix [below left] at (current bounding box.north east) {
                    \\node [bigskybluenode, label=right:CoSky "Algorithm" with 3 attributes] {}; \\\\
                    \\node [bigcyannode, label=right:CoSky "SQL query" with 3 attributes] {}; \\\\
                    };
                    """
            self.latexCode += caption1

            self.latexCode += """
            \\node[bigskybluenode, right=5pt] at (280pt,240pt) {Algo};
            \\node[bigcyannode, right=5pt] at (280pt,200pt) {SQL};
            \\end{tikzpicture}
            """

            # ------------------------------ Graph 2 -------------------------------
            picture2 = """
                    \\begin{tikzpicture}[
                    line join=bevel,
                    bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
                    bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}
                    ]
                    %% Draws
                    \draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
                    \draw[-stealth] (0pt, 0pt) -- (0pt, 310pt) node[anchor=south] {Response time in s};"""

            axisGraduation2 = ("""
                            % Axis Graduation
                            \\foreach \\y/\\ytext in {0pt/$0$, 9pt/$""" +
                               str(round(maxTime / 5, 2)) + """$, 55pt/$""" + str(
                        round(maxTime * 2 / 5, 2)) + """$, 110pt/$""" +
                               str(round(maxTime * 3 / 5, 2)) + """$, 165pt/$""" + str(
                        round(maxTime * 4 / 5, 2)) + """$, 220pt/$""" + str(round(maxTime, 2)) + """$} {
                                \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};
                            }

                            \\foreach \\x/\\xtext in {0pt/$0$, 56pt/$""" +
                               str(round(maxRows / 5, 1)) + """$, 112pt/$""" + str(
                        round(maxRows * 2 / 5, 1)) + """$, 168pt/$""" +
                               str(round(maxRows * 3 / 5, 1)) + """$, 224pt/$""" + str(
                        round(maxRows * 4 / 5, 1)) + """$, 280pt/$""" +
                               str(round(maxRows, 1)) + """$} {
                                \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};
                            }
                        """)

            self.latexCode += (picture2 + "\n" + axisGraduation2 + "\n" + drawSql[1] +
                               "\n" + drawAlgo[1] + "\n" + filldrawSql[1] + "\n" + filldrawAlgo[1] + "\n")
            caption2 = """
                    %% Caption
                    \\matrix [below left] at (current bounding box.north east) {
                    \\node [bigskybluenode, label=right:CoSky "Algorithm" with 6 attributes] {}; \\\\
                    \\node [bigcyannode, label=right:CoSky "SQL query" with 6 attributes] {}; \\\\
                    };
                    """

            self.latexCode += caption2

            self.latexCode += """
                        \\node[bigskybluenode, right=5pt] at (280pt,240pt) {Algo};
                        \\node[bigcyannode, right=5pt] at (280pt,200pt) {SQL};
                        \\end{tikzpicture}"""

            # ------------------------------ Graph 3 -------------------------------

            picture3 = """
                    \\begin{tikzpicture}[
                    line join=bevel,
                    bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
                    bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}
                    ]
                    %% Draws
                    \draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
                    \draw[-stealth] (0pt, 0pt) -- (0pt, 310pt) node[anchor=south] {Response time in s};"""

            axisGraduation3 = """
                            % Axis Graduation
                            """

            self.latexCode += (picture3 + "\n" + axisGraduation3 + "\n" + drawSql[2] +
                               "\n" + drawAlgo[2] + "\n" + filldrawSql[2] + "\n" + filldrawAlgo[2] + "\n")

            caption3 = """%% Caption
    			    \\matrix [below left] at (current bounding box.north east) {
    				\\node [bigskybluenode, label=right:CoSky "Algorithm" with 9 attributes] {}; \\\\
    				\\node [bigcyannode, label=right:CoSky "SQL query" with 9 attributes] {}; \\\\
    			    };"""

            self.latexCode += caption3

            self.latexCode += """
                        \\node[bigskybluenode, right=5pt] at (280pt,240pt) {Algo};
                        \\node[bigcyannode, right=5pt] at (280pt,200pt) {SQL};
                        \\end{tikzpicture}
                        \\end{document}"""

            self.addLatexCode(self.latexCode)
            self.render()

    def twoAlgoComparaison369Latex(self, timeDict1, timeDict2, maxRowsList, maxTimeList, algo1, algo2,
                                   latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9]):
        """
        Generate LaTeX code to compare two algorithms for 3, 6, and 9 attributes,
        with dynamic scaling per graph based on local maxRows and maxTime.
        """
        self.path += latexFilePath

        algo1_name = algo1.value
        algo2_name = algo2.value

        # Define color styles
        color_styles = ""
        for i, color in enumerate(self.colors[:2]):
            rgb = self.get_rgb_value(color)
            color_styles += f"\\definecolor{{{color}}}{{RGB}}{{{rgb}}}\n"
            color_styles += f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},\n"
            color_styles += f"small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}\n"

        self.latexCode = f"""
    \\documentclass[tikz, border=10pt]{{standalone}}
    \\usepackage{{tikz}}
    \\usetikzlibrary{{arrows.meta, shapes, positioning}}
    \\usepackage{{xcolor}}
    {color_styles}
    \\begin{{document}}"""

        for i in range(len(attributes)):
            ratioX = scaleX / maxRowsList[i]
            ratioY = scaleY / maxTimeList[i]

            # Algo 1
            line1 = f"\\draw[{self.colors[0]}, line width=2pt]"
            points1 = ""
            for k in sorted(timeDict1.keys()):
                x = int(round(k * ratioX))
                y = int(round(timeDict1[k][i] * ratioY))
                line1 += f"({x}pt, {y}pt) -- "
                points1 += f"\\filldraw[color=black, fill={self.colors[0]}] ({x}pt, {y}pt) circle (2pt);\n"
            line1 = line1.rstrip(" -- ") + ";\n"

            # Algo 2
            line2 = f"\\draw[{self.colors[1]}, line width=2pt]"
            points2 = ""
            for k in sorted(timeDict2.keys()):
                x = int(round(k * ratioX))
                y = int(round(timeDict2[k][i] * ratioY))
                line2 += f"({x}pt, {y}pt) -- "
                points2 += f"\\filldraw[color=black, fill={self.colors[1]}] ({x}pt, {y}pt) circle (2pt);\n"
            line2 = line2.rstrip(" -- ") + ";\n"

            # Axes graduations
            x_axis = "\\foreach \\x/\\xtext in {"
            for step in [scaleX * s / 5 for s in range(6)]:
                value = round(maxRowsList[i] * (step / scaleX), 1)
                x_axis += f"{int(step)}pt/${value}$, "
            x_axis = x_axis.rstrip(", ") + "} {\n\\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n}"

            y_axis = "\\foreach \\y/\\ytext in {"
            for step in [scaleY * s / 5 for s in range(6)]:
                value = round(maxTimeList[i] * (step / scaleY), 2)
                y_axis += f"{int(step)}pt/${value}$, "
            y_axis = y_axis.rstrip(", ") + "} {\n\\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n}"

            # TikZ picture
            self.latexCode += f"""
    % Graph for {attributes[i]} attributes
    \\begin{{tikzpicture}}[
        line join=bevel,
        big{self.colors[0]}node/.style={{shape=circle, fill={self.colors[0]}, draw=black, line width=1pt}},
        big{self.colors[1]}node/.style={{shape=circle, fill={self.colors[1]}, draw=black, line width=1pt}},
        small{self.colors[0]}node/.style={{circle, fill={self.colors[0]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},
        small{self.colors[1]}node/.style={{circle, fill={self.colors[1]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}
    ]
        % Axes
        \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west] {{Cardinality}};
        \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};

        % Axis graduation
        {x_axis}
        {y_axis}

        % Lines
        {line1}
        {line2}

        % Points
        {points1}
        {points2}

        % Caption
        \\matrix [below left] at (current bounding box.north east) {{
            \\node [small{self.colors[1]}node, label=right:{algo2_name} with {attributes[i]} attributes] {{}}; \\\\
            \\node [small{self.colors[0]}node, label=right:{algo1_name} with {attributes[i]} attributes] {{}}; \\\\
        }};
    \\end{{tikzpicture}}
    """

        self.latexCode += "\n\\end{document}"
        self.addLatexCode(self.latexCode)
        self.render()

    def threeAlgoComparaison369Latex(self, timeDict1, timeDict2, timeDict3, maxRowsList, maxTimeList, algo1, algo2,
                                     algo3,
                                     latexFilePath="", scaleX=280, scaleY=280, attributes=[3, 6, 9]):
        """
        Create LaTeX code for comparing three algorithms across 3, 6, 9 attributes,
        with separate scaling per graph.

        Args:
            timeDict1, timeDict2, timeDict3: Time dictionaries for each algorithm
            maxRowsList: List of max cardinalities per attribute setting
            maxTimeList: List of max times per attribute setting
            algo1, algo2, algo3: AlgoEnum or similar (should have `.value` for names)
            latexFilePath: Output file path
            scaleX, scaleY: Dimensions in pt for the TikZ graph
            attributes: List of attribute counts (default: [3, 6, 9])
        """
        self.path += latexFilePath

        algo_names = [algo1.value, algo2.value, algo3.value]
        timeDicts = [timeDict1, timeDict2, timeDict3]

        color_styles = ""
        for i, color in enumerate(self.colors[:len(attributes)]):
            rgb = self.get_rgb_value(color)
            color_styles += f"\\definecolor{{{color}}}{{RGB}}{{{rgb}}}\n"
            color_styles += f"\\tikzset{{big{color}node/.style={{circle, fill={color}, draw=black, line width=1pt}},\n"
            color_styles += f"small{color}node/.style={{circle, fill={color}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}}}\n"

        self.latexCode = f"""
        \\documentclass[tikz, border=10pt]{{standalone}}
        \\usepackage{{tikz}}
        \\usetikzlibrary{{arrows.meta, shapes, positioning}}
        \\usepackage{{xcolor}}
        {color_styles}
        \\begin{{document}}"""

        for i, attr in enumerate(attributes):
            maxRows = maxRowsList[i]
            maxTime = maxTimeList[i]
            ratioX = scaleX / maxRows
            ratioY = scaleY / maxTime

            lines = []
            points = []

            for j, timeDict in enumerate(timeDicts):
                color = self.colors[j]
                line = f"\\draw[{color}, line width=2pt]"
                point_str = ""
                for k in sorted(timeDict.keys()):
                    k = int(k)
                    x = int(round(k * ratioX))
                    y = int(round(timeDict[k][i] * ratioY))
                    line += f"({x}pt, {y}pt) -- "
                    point_str += fr"\filldraw[color=black, fill={color}] ({x}pt, {y}pt) circle (2pt);" + "\n"
                line = line.rstrip(" -- ") + ";\n"
                lines.append(line)
                points.append(point_str)

            # Axis
            x_axis = "\\foreach \\x/\\xtext in {"
            for step in [scaleX * x / 5 for x in range(6)]:
                value = round(maxRows * (step / scaleX), 1)
                x_axis += f"{int(step)}pt/${value}$, "
            x_axis = x_axis.rstrip(", ") + "} {\n\\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};\n}"

            y_axis = "\\foreach \\y/\\ytext in {"
            for step in [scaleY * y / 5 for y in range(6)]:
                value = round(maxTime * (step / scaleY), 2)
                y_axis += f"{int(step)}pt/${value}$, "
            y_axis = y_axis.rstrip(", ") + "} {\n\\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};\n}"

            self.latexCode += f"""
            % Graph for {attr} attributes
            \\begin{{tikzpicture}}[
                line join=bevel,
                small{self.colors[0]}node/.style={{circle, fill={self.colors[0]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},
                small{self.colors[1]}node/.style={{circle, fill={self.colors[1]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}},
                small{self.colors[2]}node/.style={{circle, fill={self.colors[2]}, draw=black, line width=0.5pt, minimum size=4pt, inner sep=0pt}}
            ]
                \\draw[-stealth] (0pt, 0pt) -- ({scaleX}pt, 0pt) node[anchor=north west] {{Cardinality}};
                \\draw[-stealth] (0pt, 0pt) -- (0pt, {scaleY}pt) node[anchor=south] {{Response time in s}};

                % Axis graduations
                {x_axis}
                {y_axis}

                % Curves
                {lines[0]}
                {lines[1]}
                {lines[2]}

                % Points
                {points[0]}
                {points[1]}
                {points[2]}

                % Caption
                \\matrix [below left] at (current bounding box.north east) {{
                    \\node [small{self.colors[2]}node, label=right:{algo_names[2]} with {attr} attributes] {{}}; \\\\
                    \\node [small{self.colors[1]}node, label=right:{algo_names[1]} with {attr} attributes] {{}}; \\\\
                    \\node [small{self.colors[0]}node, label=right:{algo_names[0]} with {attr} attributes] {{}}; \\\\
                }};
            \\end{{tikzpicture}}
            """

        self.latexCode += """
        \\end{document}"""

        self.addLatexCode(self.latexCode)
        self.render()


def coskySqlComparaisonLatex(self, timeDict, maxRows, maxTime, scaleX=280, scaleY=280, isDebug=False):
    """
    Create the latex code for the Cosky comparison for 3, 6, 9 columns
    """
    self.path += latexFilePath
    ratio_x = scaleX / maxRows
    ratio_y = scaleY / maxTime

    self.latexCode += """\\documentclass{article}
    \\usepackage[utf8]{inputenc}
    \\usepackage{tikz}
    \\usepackage{xcolor}
    \\usepackage{graphicx}
    \\usepackage{amsmath}
    \\usepackage{caption}

    \\definecolor{brightmaroon}{RGB}{195,33,72}
    \\definecolor{cyan}{RGB}{0,255,255}
    \\definecolor{skyblue}{RGB}{135,206,235}

    \\begin{document}
    \\begin{figure}[htbp]
    \\centering
    \\resizebox{.45\\linewidth}{!}{
    \\begin{tikzpicture}[line join=bevel,
    biggraynode/.style={shape=circle, fill=gray, draw=black, line width=1pt},
    bigbrightmaroonnode/.style={shape=circle, fill=brightmaroon, draw=black, line width=1pt},
    bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
    bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}]
    \\draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
    \\draw[-stealth] (0pt, 0pt) -- (0pt, 340pt) node[anchor=south] {Response time in s};
    """
    self.latexCode += """% X-axis ticks and labels
            \\foreach \\x/\\xtext in {0pt/$0$, 50pt/$""" + str(round(maxRows / 10, 1)) + """$, 100pt/$""" + str(
        round(maxRows / 5, 1)) + """$, 150pt/$""" + str(round(maxRows / 3.33, 1)) + """$, 200pt/$""" + str(
        round(maxRows / 2, 1)) + """$, 250pt/$""" + str(round(maxRows / 1.25, 1)) + """$, 300pt/$""" + str(
        round(maxRows, 1)) + """$} {
              \\draw (\\x, 2pt) -- (\\x, -2pt) node[below] {\\xtext\\strut};
            }
            % Y-axis ticks and labels
            \\foreach \\y/\\ytext in {0pt/$0$, 40pt/$""" + str(round(maxTime / 10, 1)) + """$, 80pt/$""" + str(
        round(maxTime / 5, 1)) + """$, 120pt/$""" + str(round(maxTime / 3.33, 1)) + """$, 160pt/$""" + str(
        round(maxTime / 2, 1)) + """$, 200pt/$""" + str(round(maxTime / 1.25, 1)) + """$, 240pt/$""" + str(
        round(maxTime, 1)) + """$} {
              \\draw (2pt, \\y) -- (-2pt, \\y) node[left] {\\ytext\\strut};
            }
            """

    self.latexCode += "% Lines\n"
    line2 = ""
    for i in range(len(timeDict[min(timeDict.keys())])):
        line1Header = f"\\draw[{self.colors[i]}, line width=2pt]"
        line1 = ""
        for k in timeDict.keys():  # Tri des clés pour ordre correct

            k = int(k)
            x = int(round(k * ratio_x))
            y = int(round(timeDict[k][i] * ratio_y))
            line1 += f"({x}pt, {y}pt) -- "
            line2 += fr"\filldraw[color=black, fill={self.colors[i]}] ({x}pt, {y}pt) circle (2pt);"
            line2 += "\n"

        line1 = line1Header + line1.rstrip(" -- ") + ";\n"
        self.latexCode += line1
    self.latexCode += "% Points and labels\n"
    self.latexCode += line2
    self.latexCode += """%% Caption
    \\matrix [below left] at (current bounding box.north east) {
    \\node [bigbrightmaroonnode, label=right:CoSky "SQL query" with 9 attributes] {}; \\\\
    \\node [bigcyannode, label=right:CoSky "SQL query" with 6 attributes] {}; \\\\
    \\node [bigskybluenode, label=right:CoSky "SQL query" with 3 attributes] {}; \\\\
    };
    \\end{tikzpicture}
    }
    \\caption{CoSky response time for SQL queries}
    \\label{fig:temps_de_reponse_de_CoSky_en_sql}
    \\end{figure}
    \\end{document}"""
    self.addLatexCode(self.latexCode)
    self.render()

def CoskyComparaisonNColumn(self, column, scaleX=280, scaleY=280):
        """
        Create the latex code for the Cosky comparison for n columns
        """
        self.colors.pop(0)
        self.colors.pop(0)
        column = int(column)
        dataPath = "../../Assets/LatexDatas/"

        match column:
            case 3:
                print("3")
                self.path += "CoskySql3.tex"
                dataPath += "ExecutionCoskySql3.json"
            case 6:
                print("6")
                self.path += "CoskySql6.tex"
                dataPath += "ExecutionCoskySql6.json"
            case 9:
                print("9")
                self.path += "CoskySql9.tex"
                dataPath += "ExecutionCoskySql9.json"

        data = self.getData(dataPath)
        timeDict = data["timeDict"]
        maxRows = data["maxRows"]
        maxTime = data["maxTime"]

        ratio_x = scaleX / maxRows
        ratio_y = scaleY / maxTime

        self.latexCode += r"""
        \documentclass{article}
        \usepackage{tikz}
        \usepackage{xcolor}
        \usepackage{graphicx}
        \usepackage{caption}

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
        \draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
        \draw[-stealth] (0pt, 0pt) -- (0pt, 300pt) node[anchor=south] {Response time in s};
        """

        self.latexCode += r"""
        % X-axis ticks and labels
        \foreach \x/\xtext in {
            0pt/$0$,
            50pt/$""" + str(round(maxRows / 10, 1)) + r"""$,
            100pt/$""" + str(round(maxRows / 5, 1)) + r"""$,
            150pt/$""" + str(round(maxRows / 3.33, 1)) + r"""$,
            200pt/$""" + str(round(maxRows / 2, 1)) + r"""$,
            250pt/$""" + str(round(maxRows / 1.25, 1)) + r"""$,
            300pt/$""" + str(round(maxRows, 1)) + r"""$
        } {
            \draw (\x, 2pt) -- (\x, -2pt) node[below] {\xtext\strut};
        }

        % Y-axis ticks and labels
        \foreach \y/\ytext in {
            0pt/$0$,
            40pt/$""" + str(round(maxTime / 10, 1)) + r"""$,
            80pt/$""" + str(round(maxTime / 5, 1)) + r"""$,
            120pt/$""" + str(round(maxTime / 3.33, 1)) + r"""$,
            160pt/$""" + str(round(maxTime / 2, 1)) + r"""$,
            200pt/$""" + str(round(maxTime / 1.25, 1)) + r"""$,
            240pt/$""" + str(round(maxTime, 1)) + r"""$
        } {
            \draw (2pt, \y) -- (-2pt, \y) node[left] {\ytext\strut};
        }
        """

        line2 = ""
        for i in range(len(timeDict[min(timeDict.keys())])):
            line1Header = f"\\draw[{self.colors[i]}, line width=2pt]"
            line1 = ""
            for k in timeDict.keys():  # Tri des clés pour ordre correct
                x = int(round(int(k) * ratio_x))
                y = int(round(timeDict[k][i] * ratio_y))
                line1 += f"({x}pt, {y}pt) -- "
                line2 += fr"\filldraw[color=black, fill={self.colors[i]}] ({x}pt, {y}pt) circle (2pt);"
                line2 += "\n"
            line1 = line1Header + line1.rstrip(" -- ") + ";\n"
            self.latexCode += line1
            self.latexCode += "% Points and labels\n"
            self.latexCode += line2

        self.latexCode += r"""
            \matrix [below left, draw=none] at (current bounding box.north east) {
            \node [bigskybluenode, label=right:CoSky "SQL query" with """ + str(column) + r""" attributes] {}; \\
            };"""

        self.latexCode += r"""
                \end{tikzpicture}
            }
            \caption{CoSky response time for SQL query with """ + str(column) + r""" attributes}
            \label{fig:temps_de_reponse_de_CoSky_en_sql_avec_""" + str(column) + r"""_dimensions}
        \end{figure}   
        \end{document}
        """

        self.addLatexCode(self.latexCode)
        self.render()


if __name__ == "__main__":
    coskyLatex = LatexMaker()
    path = "../../Assets/LatexDatas/"

    """timeDict, maxRows, maxTime = coskyLatex.getData("../../Assets/LatexDatas/ExecutionCoskyAlgo369.json")

    timeDict = {int(key): value for key, value in timeDict.items()}
    coskyLatex.oneAlgoComparaison(timeDict, maxRows, maxTime, AlgoEnum.CoskyAlgorithme, latexFilePath="OneAlgoComparaison/CoskyAlgo369.tex")"""

    print_red("1./ Comparaison de deux algorithmes")
    print_red("2./ Comparaison de trois algorithmes")
    a = input("Choix: ")
    if a == "1":
        json_paths = [
            path + "OneAlgoDatas/ExecutionCoskySql369.json",
            path + "OneAlgoDatas/CoskyAlgoTemp.json",
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
            path + "OneAlgoDatas/CoskyAlgoTemp.json"
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

    """path = "../../Assets/LatexDatas/ExecutionRankSky369.json"
    with open(path, "r") as f:
        data = f.read()
    timeDict1 = json.loads(data)
    timeDictRankSky = timeDict1["time_data"]

    path = "../../Assets/LatexDatas/ExecutionCoskyAlgo369.json"
    with open(path, "r") as f:
        data = f.read()
    timeDictAlgo = json.loads(data)
    timeDictAlgo = timeDictAlgo["time_data"]
    maxRows = timeDict1["max_rows"]
    maxTime = max(timeDict1["max_time"], timeDict1["max_time"])
    timeDictRankSky = {int(key): value for key, value in timeDictRankSky.items()}
    timeDictAlgo = {int(key): value for key, value in timeDictAlgo.items()}

    coskyLatex.twoAlgoComparaison369Latex(timeDictRankSky, timeDictAlgo, maxRows, maxTime, "RankSkyCoskyAlgo.tex")"""






    """data = coskyLatex.getData("../Assets/LatexDatas/ExecutionCoskySql3.json")
    timeDict = data["timeDict"]
    beauty_print("TimeDict", timeDict)
    quit()"""

    """print_red("1./ Comaraison Cosky SQL entre plusieurs colonnes (3, 6, 9)")
    print_red("2./ Comparaison entre SQL et Algo")
    print_red("3./ Comparaison de Cosky en SQL avec un nombre de colonnes choisi")
    a = input("Choix: ")
    if a == "1":
        path += "ExecutionCoskySql369.json"
        coskyData = coskyLatex.getData(path)
        timeDict = coskyData["time_data"]
        max_rows = coskyData["max_rows"]
        max_time = coskyData["max_time"]
        timeDict = {int(key): value for key, value in timeDict.items()}
        coskyLatex.coskySqlComparaisonLatex(timeDict, max_rows, max_time)
    elif a == "2":
        path += "ExecutionCoskySqlAlgo.json"
        with open(path, "r") as f:
            data = f.read()
        coskyData = json.loads(data)
        timeDictSql = coskyData["timeDictSql"]
        timeDictAlgo = coskyData["timeDictAlgo"]
        maxRows = coskyData["maxRows"]
        maxTime = coskyData["maxTime"]
        timeDictSql = {int(key): value for key, value in timeDictSql.items()}
        timeDictAlgo = {int(key): value for key, value in timeDictAlgo.items()}
        coskyLatex.twoAlgoComparaison369Latex(timeDictSql, timeDictAlgo, maxRows, maxTime, "CoskySqlAlgo.tex")
    elif a == "3":
        print_red("Avec combien de colonnes souhaitez-vous faire la comparaison ? (3, 6, 9):")
        column = input("Choix: ")
        if column not in ["3", "6", "9"]:
            print_red("Erreur, le nombre de colonnes doit être 3, 6 ou 9")
            exit(1)
        coskyLatex.CoskyComparaisonNColumn(column)"""

