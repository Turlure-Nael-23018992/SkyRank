import json
import textwrap
from Utils.DisplayHelpers import beauty_print, print_red

class LatexMaker:
    """
    Class to create a latex document for the results of the algorithms
    """
    def __init__(self):
        self.latexCode = ""
        self.latexFinal =""
        self.colors = ["brightmaroon", "cyan", "skyblue"]
        self.path = "../Assets/LatexFiles/"

    def addLatexCode(self, latexCode):
        """Add the latex code to the final document"""
        self.latexFinal += latexCode

    def render(self):
        """Render the latex code to a file"""
        with open(self.path, "w") as f:
            f.write(self.latexFinal)

    def getData(self,path):
        """Get the data from the json file"""
        with open(path, "r") as f:
            data = f.read()
        return json.loads(data)


    def coskySqlComparaisonLatex(self, timeDict, maxRows, maxTime, scaleX=280, scaleY=280, isDebug=False):
        """
        Create the latex code for the Cosky comparison for 3, 6, 9 columns
        """
        self.path += "CoskySql369.tex"
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


    def CoskyAlgoSqlComparaisonLatex(self, timeDictSql, timeDictAlgo, maxRows, maxTime, scaleX=280, scaleY=280):
        """
        Create the latex code for the Cosky Sql and Algo comparison
        """
        self.path += "CoskySqlAlgo.tex"
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

        #For the Graphs
        drawSql = []
        drawAlgo = []
        filldrawSql = []
        filldrawAlgo = []
        for i in range(len(timeDictSql[min(timeDictSql.keys())])):
            # Sql part
            line2Sql = ""
            line1HeaderSql = f"\\draw[{self.colors[0]}, line width=2pt]"
            line1Sql = ""
            for k in timeDictSql.keys():
                k = int(k)
                x = int(round(k * ratioX))
                y = int(round(timeDictSql[k][i] * ratioY))
                line1Sql += f"({x}pt, {y}pt) -- "
                line2Sql += fr"\filldraw[color=black, fill={self.colors[0]}] ({x}pt, {y}pt) circle (2pt);"
                line2Sql += "\n"
            line1Sql = line1HeaderSql + line1Sql.rstrip(" -- ") + ";\n"
            drawSql.append(line1Sql)
            filldrawSql.append(line2Sql)

            #Algo part
            line2Algo = ""
            line1HeaderAlgo = f"\\draw[{self.colors[1]}, line width=2pt]"
            line1Algo = ""
            for k in timeDictAlgo.keys():
                k = int(k)
                x = int(round(k * ratioX))
                y = int(round(timeDictAlgo[k][i] * ratioY))
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

    def CoskyComparaisonNColumn(self, timeDict, n, scaleX=280, scaleY=280):
        """
        Create the latex code for the Cosky comparison for n columns
        """
        pass




if __name__ == "__main__":
    coskyLatex = LatexMaker()
    path = "../Assets/LatexDatas/"

    print_red("1./ Comaraison Cosky SQL entre plusieurs colonnes (3, 6, 9)")
    print_red("2./ Comparaison entre SQL et Algo")
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
        coskyLatex.CoskyAlgoSqlComparaisonLatex(timeDictSql, timeDictAlgo, maxRows, maxTime)