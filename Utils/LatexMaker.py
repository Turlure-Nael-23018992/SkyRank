import textwrap

from .DisplayHelpers import beauty_print

class LatexMaker():
    """
    Class to create a latex document for the results of the algorithms
    """

    def __init__(self):
        self.latexHeader = ("""
        \\documentclass{article}

        % --- PACKAGES NECESSAIRES ---
        \\usepackage[utf8]{inputenc}
        \\usepackage{tikz}
        \\usepackage{xcolor}
        \\usepackage{graphicx}

        % --- COULEURS PERSONNALISÉES ---
        \\definecolor{brightmaroon}{RGB}{195,33,72}
        \\definecolor{cyan}{RGB}{0,255,255}
        \\definecolor{skyblue}{RGB}{135,206,235}

        \\begin{figure}[htbp]
        \\centering
        \\resizebox{.45\\linewidth}{!}{
        \\begin{tikzpicture}[
        line join=bevel,
        biggraynode/.style={shape=circle, fill=gray, draw=black, line width=1pt},
        bigbrightmaroonnode/.style={shape=circle, fill=brightmaroon, draw=black, line width=1pt},
        bigcyannode/.style={shape=circle, fill=cyan, draw=black, line width=1pt},
        bigskybluenode/.style={shape=circle, fill=skyblue, draw=black, line width=1pt}
        ]

        %% Draws
        \\draw[-stealth] (0pt, 0pt) -- (300pt, 0pt) node[anchor=north west] {Cardinality};
        \\draw[-stealth] (0pt, 0pt) -- (0pt, 340pt) node[anchor=south] {Response time in s};
    """)
        self.latexFinal = ""
        self.colors = [f"gray", "brightmaroon", "cyan", "skyblue"]
        self.caption = """%% Caption
			\\matrix [below left] at (current bounding box.north east) {"""

    def addLatexCode(self, latexCode):
        """
        Add the latex code to the final document
        """
        self.latexFinal += latexCode


    def coskyComparaisonLatex(self, timeDict, maxRows, maxTime, scaleX=280, scaleY=280, isDebug=False):
        """
        Create the latex code for the Cosky comparison for 3, 6, 9 columns
        """
        # Ratios for the axes of the graph
        self.colors.pop(0)
        #beauty_print("colors", self.colors)
        ratio_x = scaleX / maxRows
        ratio_y = scaleY / maxTime
        dict_ = '\n'.join([f"{k}:{v}" for k, v in timeDict.items()])
        mini_ = min(timeDict.keys())  # minimum of the bd column
        mini_key = timeDict[mini_]  # Tab of values for the mini_ column
        lenDict = len(mini_key)  # Number of tested DB
        beauty_print("timeDict", timeDict)
        beauty_print("maxRows", maxRows)
        beauty_print("maxTime", maxTime)
        beauty_print("ratio_x", ratio_x)
        beauty_print("ratio_y", ratio_y)
        #beauty_print("lenDict", lenDict)
        self.addLatexCode(self.latexHeader)
        self.addLatexCode("% Lines\n")
        line2 = ""
        #beauty_print("timeDict", timeDict)
        for i in range(lenDict):
            if isDebug:
                print(f"i:{i}")
            line1Header = f"\\draw[{self.colors[i]}, line width=2pt]"
            line1 = ""
            for k in timeDict.keys():
                #beauty_print("k",k)
                x = int(round(k * ratio_x))
                #beauty_print("x", x)
                y = int(round(timeDict[k][i] * ratio_y))
                line1 += f"({x}pt, {y}pt) -- "
                line2 += fr"\filldraw[color=black, fill={self.colors[i]}] ({x}pt, {y}pt) circle (2pt);"
                line2 += "\n"
                if isDebug:
                    beauty_print(f"x:{x}", x)
                    beauty_print(f"y:{y}", y)
                    beauty_print(f"line1", line1)
                    beauty_print(f"line2", line2)
            line1Full = line1Header + line1 + ";"
            line1Full = line1Full.replace(" -- ;", ";")
            line1Full += "\n"
            #beauty_print("line1Full", line1Full)


            #print(line1Full)
            self.addLatexCode(line1Full)
        self.addLatexCode("% Filldraws\n")
        self.addLatexCode(line2)
        endCaption = """        \\node [bigbrightmaroonnode, label=right:CoSky "SQL query" with 9 attributes] {}; \\
                        \\node [bigcyannode, label=right:CoSky "SQL query" with 6 attributes] {}; \\
                        \\node [bigskybluenode, label=right:CoSky "SQL query" with 3 attributes] {}; \\
                    };
                \end{tikzpicture}
            }
            \caption{CoSky response time for SQL queries}\label{fig:temps_de_reponse_de_CoSky_en_sql}
        \end{figure}"""
        self.addLatexCode(self.caption)
        self.addLatexCode(endCaption)





        self.render()

    def render(self):
        """
        Render the latex code to a file
        """

        with open("../Assets/LatexFiles/test.tex", "w") as f:
            f.write(self.latexFinal)


if __name__ == "__main__":
    pass