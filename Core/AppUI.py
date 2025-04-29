# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import ast

# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from Core.App import App
from Utils.Exporter.CsvExporterImpl import CsvExporterImpl
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
from Styles.StyleManager import StyleManager


class AppUI:
    """
    GUI class to manage user interactions with the application.
    """

    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title("SkyRank - Algorithm Runner")
        self.root.geometry("600x700")

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

        elif choice == "Database" or choice == "JSON":
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
        """
        List available files for selection depending on the data type.
        """
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
        """
        Open a file dialog to import a selected file.
        """
        choice = self.dataVar.get()
        filetypes = [("Database Files", "*.db")] if choice == "Database" else [("JSON Files", "*.json")]

        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.selectedDataPath = filepath
            filename = os.path.basename(filepath)
            self.fileVar.set(filename)

    def runAlgorithm(self):
        """
        Run the selected algorithm based on user configuration.
        """
        dataChoice = self.dataVar.get()
        algoChoice = self.algoVar.get()

        if not dataChoice or not algoChoice:
            messagebox.showerror("Error", "Please select both data type and algorithm.")
            return

        try:
            # Determine the data source
            if dataChoice == "Database":
                filename = self.fileVar.get()
                if not filename:
                    raise ValueError("No database file selected.")
                path = self.selectedDataPath or os.path.join("../Assets/Databases", filename)
                data = DbObject(path)

            elif dataChoice == "JSON":
                filename = self.fileVar.get()
                if not filename:
                    raise ValueError("No JSON file selected.")
                path = self.selectedDataPath or os.path.join("../Assets/AlgoExecution/JsonFiles", filename)
                data = JsonObject(path)

            elif dataChoice == "Dictionary":
                userInput = self.dictTextArea.get("1.0", tk.END).strip()
                if userInput:
                    try:
                        rawDict = ast.literal_eval(userInput)
                        if not isinstance(rawDict, dict):
                            raise ValueError("Input is not a valid dictionary.")
                        data = DictObject(rawDict)
                    except Exception as e:
                        raise ValueError(f"Invalid dictionary input: {e}")
                else:
                    filename = self.fileVar.get()
                    if not filename:
                        raise ValueError("No Dictionary file selected.")
                    path = self.selectedDataPath or os.path.join("../Assets/AlgoExecution/JsonFiles", filename)
                    rawDict = readJson(path)
                    data = DictObject(rawDict)

            elif dataChoice == "Generate Random Database":
                columns = int(self.columnEntry.get())
                rows = int(self.rowEntry.get())

                if columns not in (3, 6, 9):
                    raise ValueError("Number of columns must be 3, 6 or 9.")

                db = Database("../Assets/AlgoExecution/DbFiles/TestExecution.db", columns, rows)
                data = DbObject("../Assets/AlgoExecution/DbFiles/TestExecution.db")

            else:
                raise ValueError("Invalid data type selected.")

            # Select algorithm
            algoMap = {
                "SkyIR": SkyIR,
                "DpIdpDh": DpIdpDh,
                "CoskyAlgorithme": CoskyAlgorithme,
                "CoskySQL": CoskySQL,
                "RankSky": RankSky,
            }

            algoClass = algoMap.get(algoChoice)
            if not algoClass:
                raise ValueError("Invalid algorithm choice.")

            exporter = CsvExporterImpl(output_path="../Assets/Export/Results.csv")
            appInstance = App(data, algoClass, exporter=exporter)
            self.lastAppInstance = appInstance

            self.statusLabel.config(text="Execution completed! Result saved to Results.csv", foreground="green")

        except Exception as e:
            self.statusLabel.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Execution Error", str(e))

    def getSkylinePoints(self):
        """
        Retrieve the result points after algorithm execution.
        """
        algoInstance = self.lastAppInstance.algo_instance
        algoName = self.lastAppInstance.algo

        match algoName:
            case "SkyIR":
                return algoInstance.result
            case "DpIdpDh":
                return algoInstance.score
            case "CoskyAlgorithme":
                return algoInstance.s
            case "CoskySQL":
                return algoInstance.rows_res
            case "RankSky":
                return algoInstance.score
            case _:
                return None

    def viewSkylinePoints(self):
        """
        Open a new window to display the calculated Skyline points.
        """
        if hasattr(self, "lastAppInstance") and self.lastAppInstance:
            points = self.getSkylinePoints()

            if not points:
                messagebox.showinfo("Skyline Points", "No skyline points found or algorithm did not produce output.")
                return

            window = tk.Toplevel(self.root)
            window.title("Skyline Points")
            window.geometry("600x400")

            textArea = tk.Text(window, wrap="word")
            textArea.pack(expand=True, fill="both")

            for point in points:
                textArea.insert(tk.END, str(point) + "\n")
        else:
            messagebox.showwarning("Warning", "No results available. Please run an algorithm first.")


# Main entry point
if __name__ == "__main__":
    rootWindow = tk.Tk()
    appUI = AppUI(rootWindow)
    rootWindow.mainloop()
