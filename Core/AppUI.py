# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import ast
import json
import humanize

# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from Core.App import App
from Utils.Exporter.CsvExporterImpl import CsvExporterImpl
from Utils.Exporter.JsonExporterImpl import JsonExporterImpl
from Utils.DataTypes.DbObject import DbObject
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DictObject import DictObject
from Database.DatabaseHelpers import Database
from Utils.DataModifier.JsonUtils import readJson
from Algorithms.CoskySql import CoskySQL
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR
from Core.Styles.StyleManager import StyleManager


class AppUI:
    """
    GUI class to manage user interactions with the application.
    """

    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title("SkyRank - Algorithm Runner")
        self.root.geometry("600x750")

        StyleManager.apply_styles(self.root)
        self.createWidgets()

    def createWidgets(self):
        """
        Create all GUI widgets (labels, dropdowns, buttons).
        """
        self.dataLabel = ttk.Label(self.root, text="Choose Data Type:")
        self.dataLabel.pack(pady=5)

        self.dataVar = tk.StringVar()
        self.dataDropdown = ttk.Combobox(self.root, textvariable=self.dataVar, state="readonly")
        self.dataDropdown['values'] = ("Database", "JSON", "Dictionary", "Generate Random Database")
        self.dataDropdown.pack(pady=5)
        self.dataDropdown.bind("<<ComboboxSelected>>", self.onDataChoiceChanged)

        self.fileFrame = ttk.Frame(self.root)
        self.fileFrame.pack(pady=5)

        self.fileVar = tk.StringVar()

        self.algoLabel = ttk.Label(self.root, text="Choose Algorithm:")
        self.algoLabel.pack(pady=5)

        self.algoVar = tk.StringVar()
        self.algoDropdown = ttk.Combobox(self.root, textvariable=self.algoVar, state="readonly")
        self.algoDropdown['values'] = ("SkyIR", "DpIdpDh", "CoskyAlgorithme", "CoskySQL", "RankSky")
        self.algoDropdown.pack(pady=5)

        self.outputLabel = ttk.Label(self.root, text="Choose Output Format:")
        self.outputLabel.pack(pady=5)

        self.outputVar = tk.StringVar()
        self.outputDropdown = ttk.Combobox(self.root, textvariable=self.outputVar, state="readonly")
        self.outputDropdown['values'] = ("CSV", "JSON")
        self.outputDropdown.current(0)
        self.outputDropdown.pack(pady=5)

        self.runButton = ttk.Button(self.root, text="Run Algorithm", command=self.runAlgorithm)
        self.runButton.pack(pady=20)

        self.viewButton = ttk.Button(self.root, text="View Skyline Points", command=self.viewSkylinePoints)
        self.viewButton.pack(pady=5)

        self.statusLabel = ttk.Label(self.root, text="")
        self.statusLabel.pack(pady=5)

    def onDataChoiceChanged(self, _event):
        """
        Handle user data type choice and dynamically update the file import options.
        """
        for widget in self.fileFrame.winfo_children():
            widget.destroy()

        choice = self.dataVar.get()
        self.selectedDataPath = None

        if choice == "Generate Random Database":
            ttk.Label(self.fileFrame, text="Number of Columns (3, 6, 9):").pack(side="left", padx=5)
            self.columnEntry = ttk.Entry(self.fileFrame, width=5)
            self.columnEntry.pack(side="left", padx=5)

            ttk.Label(self.fileFrame, text="Number of Rows:").pack(side="left", padx=5)
            self.rowEntry = ttk.Entry(self.fileFrame, width=10)
            self.rowEntry.pack(side="left", padx=5)

        elif choice in ("Database", "JSON"):
            files = self.listAvailableFiles(choice)
            if files:
                self.fileDropdown = ttk.Combobox(self.fileFrame, textvariable=self.fileVar, state="readonly", values=files)
                self.fileDropdown.pack(side="left", padx=5)
            self.importButton = ttk.Button(self.fileFrame, text="Import File", command=self.importFile)
            self.importButton.pack(side="left", padx=5)

        elif choice == "Dictionary":
            ttk.Label(self.fileFrame, text="Enter Dictionary manually:").pack()
            self.dictTextArea = tk.Text(self.fileFrame, height=10, width=60)
            self.dictTextArea.pack(pady=5)

            ttk.Label(self.fileFrame, text="Or import from a JSON file:").pack(pady=5)
            self.fileDropdown = ttk.Combobox(self.fileFrame, textvariable=self.fileVar, state="readonly", values=self.listAvailableFiles("Dictionary"))
            self.fileDropdown.pack(side="left", padx=5)
            self.importButton = ttk.Button(self.fileFrame, text="Import File", command=self.importFile)
            self.importButton.pack(side="left", padx=5)

    @staticmethod
    def listAvailableFiles(dataType):
        baseFolders = {
            "Database": "../Assets/Databases",
            "JSON": "../Assets/AlgoExecution/JsonFiles",
            "Dictionary": "../Assets/AlgoExecution/JsonFiles"
        }
        extensions = {
            "Database": ".db",
            "JSON": ".json",
            "Dictionary": ".json"
        }
        folder = baseFolders.get(dataType)
        ext = extensions.get(dataType)
        if folder and os.path.exists(folder):
            return [f for f in os.listdir(folder) if f.endswith(ext)]
        return []

    def importFile(self):
        choice = self.dataVar.get()
        filetypes = [("Database Files", "*.db")] if choice == "Database" else [("JSON Files", "*.json")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.selectedDataPath = filepath
            self.fileVar.set(os.path.basename(filepath))

    from Utils.Exporter.CsvExporterImpl import CsvExporterImpl
    from Utils.Exporter.JsonExporterImpl import JsonExporterImpl
    # ...

    def runAlgorithm(self):
        """
        Run the selected algorithm based on configuration and export results.
        """
        import time
        dataChoice = self.dataVar.get()
        algoChoice = self.algoVar.get()
        outputFormat = self.outputVar.get()

        if not dataChoice or not algoChoice:
            messagebox.showerror("Error", "Please select data type and algorithm.")
            return

        try:
            # Load data
            if dataChoice == "Database":
                filename = self.fileVar.get()
                path = self.selectedDataPath or os.path.join("../Assets/Databases", filename)
                data = DbObject(path)
            elif dataChoice == "JSON":
                filename = self.fileVar.get()
                path = self.selectedDataPath or os.path.join("../Assets/AlgoExecution/JsonFiles", filename)
                data = JsonObject(path)
            elif dataChoice == "Dictionary":
                userInput = self.dictTextArea.get("1.0", tk.END).strip()
                if userInput:
                    rawDict = ast.literal_eval(userInput)
                    data = DictObject(rawDict)
                else:
                    filename = self.fileVar.get()
                    path = self.selectedDataPath or os.path.join("../Assets/AlgoExecution/JsonFiles", filename)
                    data = DictObject(readJson(path))
            elif dataChoice == "Generate Random Database":
                cols = int(self.columnEntry.get())
                rows = int(self.rowEntry.get())
                dbPath = "../Assets/AlgoExecution/DbFiles/TestExecution.db"
                Database(dbPath, cols, rows)
                data = DbObject(dbPath)
            else:
                raise ValueError("Unsupported data type.")

            # Algo mapping
            algoMap = {
                "SkyIR": SkyIR,
                "DpIdpDh": DpIdpDh,
                "CoskyAlgorithme": CoskyAlgorithme,
                "CoskySQL": CoskySQL,
                "RankSky": RankSky
            }
            algoClass = algoMap.get(algoChoice)
            if not algoClass:
                raise ValueError("Unsupported algorithm.")

            # Exporter selection
            exporter = None
            if outputFormat == "CSV":
                exporter = CsvExporterImpl(output_path="../Assets/Export/CSVFiles/Results.csv")
            elif outputFormat == "JSON":
                exporter = JsonExporterImpl(output_path="../Assets/Export/JsonFiles/Result.json")

            # Run app
            app = App(
                data,
                algoClass,
                exporter=exporter,
                input_type=dataChoice,
                input_file=self.fileVar.get() if self.fileVar.get() else "generated"
            )
            self.lastAppInstance = app

            self.statusLabel.config(
                text=f"Execution complete. Results saved to {outputFormat}.",
                foreground="green"
            )

        except Exception as e:
            self.statusLabel.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Execution Error", str(e))


    def getSkylinePoints(self):
        algoInstance = self.lastAppInstance.algo_instance
        algoName = self.lastAppInstance.algo
        match algoName:
            case "SkyIR": return algoInstance.result
            case "DpIdpDh": return algoInstance.score
            case "CoskyAlgorithme": return algoInstance.s
            case "CoskySQL": return algoInstance.rows_res
            case "RankSky": return algoInstance.score
        return []

    def viewSkylinePoints(self):
        if hasattr(self, "lastAppInstance") and self.lastAppInstance:
            points = self.getSkylinePoints()
            if not points:
                messagebox.showinfo("Skyline Points", "No skyline points found.")
                return
            win = tk.Toplevel(self.root)
            win.title("Skyline Points")
            textArea = tk.Text(win, wrap="word")
            textArea.pack(expand=True, fill="both")
            for p in points:
                textArea.insert(tk.END, str(p) + "\n")
        else:
            messagebox.showwarning("Warning", "Please run an algorithm first.")


if __name__ == "__main__":
    rootWindow = tk.Tk()
    appUI = AppUI(rootWindow)
    rootWindow.mainloop()