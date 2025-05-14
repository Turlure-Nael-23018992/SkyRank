import os, sys, ast, sqlite3, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.simpledialog import askstring

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.App import App
from Core.Styles.StyleManager import StyleManager
from Utils.Preference import Preference
from Utils.Exporter.CsvExporterImpl import CsvExporterImpl
from Utils.Exporter.JsonExporterImpl import JsonExporterImpl
from Utils.DataTypes.DbObject import DbObject
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DictObject import DictObject
from Utils.DataModifier.JsonUtils import readJson
from Database.DatabaseHelpers import Database
from Algorithms.CoskySql import CoskySQL
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR


class AppUI:
    """
    Graphical User Interface for SkyRank - Algorithm Runner.
    Allows users to select data, run different algorithms, and export results.
    """

    def __init__(self, master: tk.Tk):
        """
        Initialize the AppUI.

        :param master: The root Tkinter window
        """
        self.root = master
        self.root.title("SkyRank - Algorithm Runner")
        self.root.geometry("600x750")
        StyleManager.apply_styles(self.root)
        self._build_widgets()
        self.selectedDataPath = None
        self.lastAppInstance = None

    def _build_widgets(self):
        """
        Build all UI widgets such as dropdowns, buttons, and labels.
        """
        ttk.Label(self.root, text="Choose Data Type:").pack(pady=5)
        self.dataVar = tk.StringVar()
        self.dataDropdown = ttk.Combobox(
            self.root, textvariable=self.dataVar, state="readonly",
            values=("Database", "JSON", "Dictionary", "Generate Random Database")
        )
        self.dataDropdown.pack(pady=5)
        self.dataDropdown.bind("<<ComboboxSelected>>", self._data_choice_changed)

        self.fileFrame = ttk.Frame(self.root); self.fileFrame.pack(pady=5)
        self.fileVar = tk.StringVar()

        ttk.Label(self.root, text="Choose Algorithm:").pack(pady=5)
        self.algoVar = tk.StringVar()
        self.algoDropdown = ttk.Combobox(
            self.root, textvariable=self.algoVar, state="readonly",
            values=("SkyIR", "DpIdpDh", "CoskyAlgorithme", "CoskySQL", "RankSky")
        ); self.algoDropdown.pack(pady=5)

        ttk.Label(self.root, text="Choose Output Format:").pack(pady=5)
        self.outputVar = tk.StringVar()
        self.outputDropdown = ttk.Combobox(
            self.root, textvariable=self.outputVar, state="readonly", values=("CSV", "JSON")
        ); self.outputDropdown.current(0); self.outputDropdown.pack(pady=5)

        ttk.Button(self.root, text="Run Algorithm", command=self._run_algorithm).pack(pady=20)
        ttk.Button(self.root, text="View Skyline Points", command=self._view_skyline_points).pack(pady=5)
        self.statusLabel = ttk.Label(self.root, text=""); self.statusLabel.pack(pady=5)

    def _data_choice_changed(self, _):
        """
        Handle changes to the data type selection and update the UI accordingly.

        :param _: Event object (not used)
        """
        for w in self.fileFrame.winfo_children():
            w.destroy()

        choice = self.dataVar.get()
        self.selectedDataPath = None

        if choice == "Generate Random Database":
            ttk.Label(self.fileFrame, text="Columns (3/6/9):").pack(side="left", padx=5)
            self.columnEntry = ttk.Entry(self.fileFrame, width=5); self.columnEntry.pack(side="left", padx=5)
            ttk.Label(self.fileFrame, text="Rows:").pack(side="left", padx=5)
            self.rowEntry = ttk.Entry(self.fileFrame, width=10); self.rowEntry.pack(side="left", padx=5)

        elif choice in ("Database", "JSON"):
            files = self._list_files(choice)
            if files:
                ttk.Combobox(self.fileFrame, textvariable=self.fileVar,
                             state="readonly", values=files).pack(side="left", padx=5)
            ttk.Button(self.fileFrame, text="Import", command=self._import_file).pack(side="left", padx=5)

        elif choice == "Dictionary":
            ttk.Label(self.fileFrame, text="Enter Dictionary:").pack()
            self.dictTextArea = tk.Text(self.fileFrame, height=10, width=60); self.dictTextArea.pack(pady=5)
            ttk.Label(self.fileFrame, text="Or import JSON:").pack(pady=5)
            ttk.Combobox(self.fileFrame, textvariable=self.fileVar,
                         state="readonly", values=self._list_files("Dictionary")
                         ).pack(side="left", padx=5)
            ttk.Button(self.fileFrame, text="Import", command=self._import_file).pack(side="left", padx=5)

    def _import_file(self):
        """
        Open a file dialog to import a database or JSON file based on selected type.
        """
        choice = self.dataVar.get()
        types = [("Database Files", "*.db")] if choice == "Database" else [("JSON Files", "*.json")]
        path = filedialog.askopenfilename(filetypes=types)
        if path:
            self.selectedDataPath = path
            self.fileVar.set(os.path.basename(path))

    @staticmethod
    def _list_files(dtype):
        """
        List all available files for the given data type.

        :param dtype: Type of the data (Database, JSON, Dictionary)
        :return: List of matching filenames
        """
        roots = {"Database": "../Assets/Databases",
                 "JSON": "../Assets/AlgoExecution/JsonFiles",
                 "Dictionary": "../Assets/AlgoExecution/JsonFiles"}
        ext = ".db" if dtype == "Database" else ".json"
        folder = roots[dtype]
        return [f for f in os.listdir(folder) if f.endswith(ext)] if os.path.exists(folder) else []

    def _load_data(self, dtype):
        """
        Load the selected data depending on its type.

        :param dtype: Type of the data to load
        :return: A data object (DbObject, JsonObject, or DictObject)
        """
        if dtype == "Database":
            p = self.selectedDataPath or os.path.join("../Assets/Databases", self.fileVar.get())
            return DbObject(p)
        if dtype == "JSON":
            p = self.selectedDataPath or os.path.join("../Assets/AlgoExecution/JsonFiles", self.fileVar.get())
            return JsonObject(p)
        if dtype == "Dictionary":
            txt = getattr(self, "dictTextArea", tk.Text()).get("1.0", tk.END).strip()
            return DictObject(ast.literal_eval(txt)) if txt else DictObject(
                readJson(os.path.join("../Assets/AlgoExecution/JsonFiles", self.fileVar.get())))
        if dtype == "Generate Random Database":
            cols, rows = int(self.columnEntry.get()), int(self.rowEntry.get())
            dbp = "../Assets/AlgoExecution/DbFiles/TestExecution.db"
            Database(dbp, cols, rows); return DbObject(dbp)
        raise ValueError("Unsupported data type")

    def _count_columns(self, data_obj, dtype):
        """
        Count the number of columns in the given data object.

        :param data_obj: The data object loaded
        :param dtype: The data type string
        :return: Number of columns
        """
        if isinstance(data_obj, DictObject):
            return len(next(iter(data_obj.r.values())))
        if isinstance(data_obj, JsonObject):
            raw = readJson(data_obj.fp)
            return len(next(iter(raw.values())))
        if isinstance(data_obj, DbObject):
            con = sqlite3.connect(data_obj.fp); cur = con.cursor()
            cur.execute("PRAGMA table_info(Pokemon)"); n = len(cur.fetchall()) - 1
            con.close(); return n
        if dtype == "Generate Random Database":
            return int(self.columnEntry.get())
        raise ValueError("Cannot count columns")

    def _run_algorithm(self):
        """
        Execute the selected algorithm on the loaded data and export results.
        """
        dtype, algo_name, out_fmt = self.dataVar.get(), self.algoVar.get(), self.outputVar.get()
        if not dtype or not algo_name:
            messagebox.showerror("Error", "Select data type and algorithm."); return
        try:
            data = self._load_data(dtype)
            nb_cols = self._count_columns(data, dtype)

            requires_pref = algo_name in ("RankSky", "CoskyAlgorithme", "CoskySQL")
            prefs = None
            if requires_pref:
                s = askstring("Preferences",
                              f"{nb_cols} columns detected.\nEnter {nb_cols} values (min/max) comma‑separated:")
                if not s: return
                parts = [p.strip().lower() for p in s.split(",")]
                if len(parts) != nb_cols or any(p not in ("min", "max") for p in parts):
                    messagebox.showerror("Error", "Incorrect preference list."); return
                prefs = [Preference.MIN if p == "min" else Preference.MAX for p in parts]

            algo_cls = {"SkyIR": SkyIR, "DpIdpDh": DpIdpDh,
                        "CoskyAlgorithme": CoskyAlgorithme, "CoskySQL": CoskySQL,
                        "RankSky": RankSky}[algo_name]

            exporter = CsvExporterImpl("../Assets/Export/CSVFiles/Results.csv") if out_fmt == "CSV" \
                      else JsonExporterImpl("../Assets/Export/JsonFiles/Result.json")

            app = App(data, algo_cls, exporter=exporter,
                      input_type=dtype, input_file=self.fileVar.get() or "inline",
                      preferences=prefs)
            self.lastAppInstance = app
            self.statusLabel.config(text=f"Done in {app.execution_time}s", foreground="green")
        except Exception as e:
            self.statusLabel.config(text=f"Error: {e}", foreground="red")
            messagebox.showerror("Error", str(e))

    def _get_skyline_points(self):
        """
        Get the computed skyline points from the last executed algorithm.

        :return: List of skyline points
        """
        algo = self.lastAppInstance.algo
        inst = self.lastAppInstance.algo_instance

        if algo == "SkyIR":
            return inst.result
        elif algo == "DpIdpDh":
            return inst.score
        elif algo == "CoskyAlgorithme":
            return getattr(inst, "s", [])
        elif algo == "CoskySQL":
            return inst.rows_res
        elif algo == "RankSky":
            return inst.score
        else:
            return []

    def _view_skyline_points(self):
        """
        Open a new window displaying the skyline points, if any.
        """
        if not self.lastAppInstance: return
        pts = self._get_skyline_points()
        if not pts:
            messagebox.showinfo("Skyline", "No points."); return
        win = tk.Toplevel(self.root); win.title("Skyline Points")
        ta = tk.Text(win, wrap="word"); ta.pack(expand=True, fill="both")
        for p in pts: ta.insert(tk.END, str(p) + "\n")



if __name__ == "__main__":
    root = tk.Tk()
    AppUI(root)
    root.mainloop()
