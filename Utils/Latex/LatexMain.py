from Utils.Latex.LatexMaker import LatexMaker
from Utils.Latex.AlgoEnum import AlgoEnum
import os
from Utils.DisplayHelpers import print_red

def compareAlgos(coskyLatex, algos, outputFile, basePath=""):
    """
    Compare the algorithms and generate a LaTeX file for the comparison.
    :param coskyLatex: Object to handle LaTeX generation.
    :param algos: the algorithms to compare.
    :param outputFile: the name of the output LaTeX file.
    :param basePath: the base path for the JSON files.
    """
    json_paths = [basePath + algo.filepath for algo in algos]
    timeDicts, maxRowsList, maxTimeList = coskyLatex.prepareComparisonData(json_paths)

    if len(algos) == 2:
        folder = "../../Assets/LatexFiles/TwoAlgosComparaison/"
        fullPath = os.path.join(folder, outputFile)
        coskyLatex.twoAlgoComparaison369Latex(
            timeDicts[0], timeDicts[1],
            maxRowsList, maxTimeList,
            algos[0], algos[1],
            latexFilePath=fullPath
        )
    elif len(algos) == 3:
        folder = "../../Assets/LatexFiles/ThreeAlgosComparaison/"
        fullPath = os.path.join(folder, outputFile)
        coskyLatex.threeAlgoComparaison369Latex(
            timeDicts[0], timeDicts[1], timeDicts[2],
            maxRowsList, maxTimeList,
            algos[0], algos[1], algos[2],
            latexFilePath=fullPath
        )
    else:
        print("❌ Comparaison disponible uniquement pour 2 ou 3 algorithmes.")

def getAlgoByName(name):
    """
    Get the algorithm by its name or label.
    :param name: The name or label of the algorithm.
    :return: The corresponding AlgoEnum member or None if not found.
    """
    for algo in AlgoEnum:
        if name.lower() in algo.name.lower() or name.lower() in algo.label.lower():
            return algo
    return None

def promptAlgos():
    print_red("\nListe des algorithmes disponibles :")
    for algo in AlgoEnum:
        print(f"- {algo.name} ({algo.label})")

    nb = int(input("\nCombien d'algorithmes voulez-vous comparer ? (2 ou 3) : "))
    assert nb in [2, 3], "❌ Veuillez entrer 2 ou 3." # Return an error if not 2 or 3

    algos = []
    for i in range(nb):
        name = input(f"Nom de l'algorithme {i+1} : ")
        algo = getAlgoByName(name)
        if not algo:
            raise ValueError(f"❌ Algorithme '{name}' introuvable.") # Return an error if algo not found
        algos.append(algo)

    output = input("Nom du fichier LaTeX de sortie (avec .tex) : ")

    return algos, output

if __name__ == "__main__":
    coskyLatex = LatexMaker()
    path = "../../Assets/LatexDatas/"
    algos, outputFile = promptAlgos()
    compareAlgos(coskyLatex, algos, outputFile, basePath=path)