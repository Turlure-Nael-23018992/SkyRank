import json
import textwrap
from Utils.DisplayHelpers import beauty_print

class LatexMaker:
    """
    Class to create a latex document for the results of the algorithms
    """
    def __init__(self):
        self.latexHeader = """\\documentclass{article}
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
        self.latexFinal = ""
        self.colors = ["brightmaroon", "cyan", "skyblue"]
        self.caption = """%% Caption
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

    def addLatexCode(self, latexCode):
        """Add the latex code to the final document"""
        self.latexFinal += latexCode



    def render(self):
        """Render the latex code to a file"""
        with open("../Assets/LatexFiles/test.tex", "w") as f:
            f.write(self.latexFinal)


    def coskySqlComparaisonLatex(self, timeDict, maxRows, maxTime, scaleX=280, scaleY=280, isDebug=False):
        """Create the latex code for the Cosky comparison for 3, 6, 9 columns"""
        ratio_x = scaleX / maxRows
        ratio_y = scaleY / maxTime

        self.latexHeader += """% X-axis ticks and labels
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

        self.addLatexCode(self.latexHeader)

        self.addLatexCode("% Lines\n")
        line2 = ""

        for i in range(len(timeDict[min(timeDict.keys())])):
            line1Header = f"\\draw[{self.colors[i]}, line width=2pt, opacity=0.7]"
            line1 = ""
            for k in timeDict.keys():  # Tri des clés pour ordre correct

                k = int(k)
                x = int(round(k * ratio_x))
                y = int(round(timeDict[k][i] * ratio_y))
                line1 += f"({x}pt, {y}pt) -- "
                line2 += fr"\filldraw[color=black, fill={self.colors[i]}] ({x}pt, {y}pt) circle (2pt);"
                line2 += "\n"

            line1 = line1Header + line1.rstrip(" -- ") + ";\n"
            self.addLatexCode(line1)

        self.addLatexCode("% Points and labels\n")
        self.addLatexCode(line2)
        self.addLatexCode(self.caption)
        self.render()


    def CoskyAlgoSqlComparaisonLatex(self):
        """
        Create the latex code for the Cosky Sql and Algo comparison
        """


if __name__ == "__main__":
    with open("../Assets/LatexDatas/ExecutionCoskyDatas.json", "r") as f:
        data = f.read()
    coskyData = json.loads(data)

    timeDict = coskyData["time_data"]
    max_rows = coskyData["max_rows"]
    max_time = coskyData["max_time"]

    timeDict = {int(key): value for key, value in timeDict.items()}

    cokyLatex = LatexMaker()
    cokyLatex.coskySqlComparaisonLatex(timeDict, max_rows, max_time)