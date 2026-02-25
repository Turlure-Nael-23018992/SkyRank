"""
SkyRank GUI (PyQt5)
===================

Graphical user interface for the SkyRank project, built with PyQt5.
Supports data loading from JSON, SQLite, and dictionary sources,
execution of Skyline ranking algorithms, 3D visualization of results
via Matplotlib, and export to CSV or JSON formats.
"""
import os, sys, ast, sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QComboBox, QTextEdit, QLineEdit, QMessageBox,
    QFrame, QMainWindow, QStackedWidget, QInputDialog
)
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.App import App

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
from Utils.DataModifier.DataUnifier import DataUnifier
from Utils.DisplayHelpers import beauty_print

class AppUIPyQt(QMainWindow):
    """
    Main window of the SkyRank application.

    Provides a graphical interface for selecting datasets, algorithms,
    and output formats, and for visualizing Skyline results in 3D.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyRank - Algorithm Runner [PyQt]")
        self.setGeometry(100, 100, 1200, 800)
        self.selectedDataPath = None
        self.lastAppInstance = None
        self.tableName = "Pokemon"
        self.initUI()

    def initUI(self):
        """
        Builds and arranges all UI components: data type selector, algorithm
        selector, output format selector, action buttons, status label,
        and the embedded Matplotlib canvas with its navigation toolbar.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        control_layout = QVBoxLayout()
        control_layout.setAlignment(Qt.AlignTop)

        control_layout.addWidget(QLabel("Choose Data Type:"))
        self.dataCombo = QComboBox()
        self.dataCombo.addItems(["Database", "JSON", "Dictionary", "Generate Random Database"])
        self.dataCombo.currentIndexChanged.connect(self.on_data_type_changed)
        control_layout.addWidget(self.dataCombo)

        self.fileFrame = QVBoxLayout()
        control_layout.addLayout(self.fileFrame)

        control_layout.addWidget(QLabel("Choose Algorithm:"))
        self.algoCombo = QComboBox()
        self.algoCombo.addItems(["SkyIR", "DpIdpDh", "CoskyAlgorithme", "CoskySQL", "RankSky"])
        control_layout.addWidget(self.algoCombo)

        control_layout.addWidget(QLabel("Choose Output Format:"))
        self.outputCombo = QComboBox()
        self.outputCombo.addItems(["CSV", "JSON"])
        control_layout.addWidget(self.outputCombo)

        run_button = QPushButton("Run Algorithm")
        run_button.clicked.connect(self.run_algorithm)
        control_layout.addWidget(run_button)

        view_button = QPushButton("View Skyline Points")
        view_button.clicked.connect(self.view_skyline_points)
        control_layout.addWidget(view_button)

        self.statusLabel = QLabel("")
        control_layout.addWidget(self.statusLabel)

        main_layout.addLayout(control_layout, 1)

        # Matplotlib canvas and navigation toolbar for 3D visualization
        viz_layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        viz_layout.addWidget(self.toolbar)
        viz_layout.addWidget(self.canvas)
        main_layout.addLayout(viz_layout, 3)

        self.on_data_type_changed()

    def list_files(self, dtype):
        roots = {
            "Database": os.path.join("Assets", "Databases"),
            "JSON": os.path.join("Assets", "AlgoExecution", "JsonFiles"),
            "Dictionary": os.path.join("Assets", "AlgoExecution", "JsonFiles")
        }
        ext = ".db" if dtype == "Database" else ".json"
        folder = roots[dtype]
        return [f for f in os.listdir(folder) if f.endswith(ext)] if os.path.exists(folder) else []

    def on_data_type_changed(self):
        # Removes all existing widgets from the fileFrame layout before rebuilding it
        while self.fileFrame.count():
            child = self.fileFrame.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

        choice = self.dataCombo.currentText()
        self.selectedDataPath = None

        if choice == "Generate Random Database":
            self.columnEntry = QLineEdit();
            self.columnEntry.setPlaceholderText("Columns (3/6/9)")
            self.rowEntry = QLineEdit();
            self.rowEntry.setPlaceholderText("Rows")
            self.fileFrame.addWidget(self.columnEntry)
            self.fileFrame.addWidget(self.rowEntry)

        elif choice in ("Database", "JSON", "Dictionary"):
            self.fileSelectCombo = QComboBox()
            self.fileSelectCombo.addItems(self.list_files(choice))
            self.fileSelectCombo.currentTextChanged.connect(self.on_file_selected)
            self.fileFrame.addWidget(self.fileSelectCombo)

            browse_btn = QPushButton("Import File")
            browse_btn.clicked.connect(self.import_file)
            self.fileFrame.addWidget(browse_btn)

            if choice == "Dictionary":
                self.dictTextArea = QTextEdit()
                self.dictTextArea.setPlaceholderText("Enter dictionary manually")
                self.fileFrame.addWidget(self.dictTextArea)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def on_file_selected(self, filename):
        dtype = self.dataCombo.currentText()
        roots = {
            "Database": os.path.join("Assets", "Databases"),
            "JSON": os.path.join("Assets", "AlgoExecution", "JsonFiles"),
            "Dictionary": os.path.join("Assets", "AlgoExecution", "JsonFiles")
        }
        if filename:
            self.selectedDataPath = os.path.normpath(os.path.join(roots[dtype], filename))

    def import_file(self):
        dtype = self.dataCombo.currentText()
        ftype = "Database Files (*.db)" if dtype == "Database" else "JSON Files (*.json)"
        path, _ = QFileDialog.getOpenFileName(self, "Choose File", "", ftype)
        if path:
            self.selectedDataPath = path

    def load_data(self, dtype):
        if dtype == "Database": return DbObject(self.selectedDataPath)
        if dtype == "JSON": return JsonObject(self.selectedDataPath)
        if dtype == "Dictionary":
            txt = self.dictTextArea.toPlainText().strip()
            return DictObject(ast.literal_eval(txt)) if txt else DictObject(readJson(self.selectedDataPath))
        if dtype == "Generate Random Database":
            cols, rows = int(self.columnEntry.text()), int(self.rowEntry.text())
            dbp = "Assets/AlgoExecution/DbFiles/TestExecution.db"
            Database(dbp, cols, rows); return DbObject(dbp)
        raise ValueError("Unsupported data type")

    def count_columns(self, obj, dtype):
        if isinstance(obj, DictObject): return len(next(iter(obj.r.values())))
        if isinstance(obj, JsonObject): return len(next(iter(readJson(obj.fp).values())))
        if isinstance(obj, DbObject):
            con = sqlite3.connect(obj.fp); cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.tableName}"); n = len(cur.fetchall()[0]) - 1
            con.close(); return n
        if dtype == "Generate Random Database": return int(self.columnEntry.text())
        raise ValueError("Cannot count columns")

    def run_algorithm(self):
        """
        Loads the selected dataset, collects user preferences if required,
        instantiates the chosen algorithm and exporter, runs the App pipeline,
        and triggers a graph update. Displays the execution time on success
        or an error message on failure.
        """
        try:
            dtype = self.dataCombo.currentText()
            algo_name = self.algoCombo.currentText()
            out_fmt = self.outputCombo.currentText()

            data = self.load_data(dtype)
            nb_cols = self.count_columns(data, dtype)

            prefs = None
            if algo_name in ("RankSky", "CoskyAlgorithme", "CoskySQL"):
                prompt_msg = (
                    f"{nb_cols} columns detected.\n"
                    "For each column, enter 'min' (lower is better) or 'max' (higher is better),\n"
                    "separated by commas.\n\n"
                    "Example: " + ",".join(["min" if i % 2 == 0 else "max" for i in range(min(3, nb_cols))]) + (",..." if nb_cols > 3 else "") + "\n\n"
                    f"Enter {nb_cols} values:"
                )
                s, ok = QInputDialog.getText(self, "Preferences", prompt_msg)
                if not ok or not s: return
                parts = [p.strip().lower() for p in s.split(",")]
                if len(parts) != nb_cols or any(p not in ("min", "max") for p in parts):
                    QMessageBox.critical(self, "Error", "Incorrect preference list.")
                    return
                prefs = [Preference.MIN if p == "min" else Preference.MAX for p in parts]

            algo_cls = {"SkyIR": SkyIR, "DpIdpDh": DpIdpDh,
                        "CoskyAlgorithme": CoskyAlgorithme, "CoskySQL": CoskySQL,
                        "RankSky": RankSky}[algo_name]

            exporter = CsvExporterImpl("Assets/Export/CSVFiles/Results.csv") if out_fmt == "CSV" \
                      else JsonExporterImpl("Assets/Export/JsonFiles/Result.json")

            app = App(data, algo_cls, exporter=exporter,
                      input_type=dtype, input_file=self.selectedDataPath or "inline",
                      preferences=prefs)
            self.lastAppInstance = app
            self.statusLabel.setText(f"Done in {app.execution_time}s")
            
            all_pts = self.get_all_points()
            sky_pts = self.get_skyline_points()
            
            self.display_graph(all_pts, sky_pts)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.statusLabel.setText(f"Error: {e}")

    def _extract_all_points(self, data_obj):
        """
        Extracts all data points from a DictObject, JsonObject, or DbObject
        and returns them as a dictionary mapping each point ID to its list of coordinates.
        """
        if isinstance(data_obj, DictObject): 
            return {k: list(v) for k, v in data_obj.r.items()}
        if isinstance(data_obj, JsonObject): 
            return {k: list(v) for k, v in readJson(data_obj.fp).items()}
        if isinstance(data_obj, DbObject):
            con = sqlite3.connect(data_obj.fp)
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.tableName}")
            rows = {row[0]: list(row[1:]) for row in cur.fetchall()}
            con.close()
            return rows
        return {}


    def get_all_points(self) -> dict:
        """
        Returns all dataset points in unified coordinate space as a dict
        mapping each point ID to its list of coordinates ``{id: [coords...]}``.  
        For RankSky, re-applies the original preferences via ``DataUnifier``
        to ensure consistency with the coordinate space used for skyline points.
        Returns an empty dict if no algorithm has been run yet.
        """
        if not self.lastAppInstance: return {}
        
        algo_name = getattr(self.lastAppInstance, 'algo', None)
        inst = getattr(self.lastAppInstance, 'algo_instance', None)
        
        # CoskyAlgorithme stores a pre-unified dataset in inst.r; use it directly
        # to guarantee coordinate consistency with the skyline points.
        if algo_name in ("CoskyAlgorithme",) and inst and hasattr(inst, 'r'):
            return {k: list(v) for k, v in inst.r.items()}
        
        if algo_name == "RankSky" and inst:
            # RankSky mutates inst.pref to [MAX, MAX, ...] after execution.
            # prefInit and rTupleInit preserve the original values and are used
            # here to re-apply the "auto" unification mode for correct display.
            raw = {k: list(v) for k, v in getattr(inst, 'rTupleInit', {}).items()}
            prefs_orig = list(getattr(inst, 'prefInit', []))
            if raw and prefs_orig:
                unifier = DataUnifier(raw, prefs_orig, mode="auto")
                return unifier.unify()
            return raw

        # For all other algorithms, raw data is loaded and unified using the stored preferences.
        data_obj = getattr(self.lastAppInstance, 'r', None)
        
        if data_obj is None:
            dtype = self.dataCombo.currentText()
            data_wrapper = self.load_data(dtype)
            all_pts = self._extract_all_points(data_wrapper)
        else:
            all_pts = {k: list(v) for k, v in data_obj.items()}

        prefs = getattr(self.lastAppInstance, 'pref', None)
        
        if prefs:
            unifier = DataUnifier(all_pts, list(prefs), mode="auto")
            all_pts = unifier.unify()
            
        return all_pts

    def get_skyline_points(self):
        """
        Returns the skyline points produced by the last algorithm run,
        normalized to a common format: ``{id: {'coords': [v1, v2, ...], 'score': value}}``.
        Each algorithm exposes its results through a different attribute;
        this method handles the extraction for SkyIR, DpIdpDh, CoskyAlgorithme,
        CoskySQL, and RankSky. Returns an empty dict if no algorithm has been run.
        """
        if not self.lastAppInstance: return {}
        algo = self.lastAppInstance.algo
        inst = self.lastAppInstance.algo_instance
        
        result_data = {}
        
        if algo == "SkyIR":
            # SkyIR stores results as [(id, score), ...] in inst.result
            for item in getattr(inst, 'result', []):
                p_id, score = item[0], item[1]
                coords = list(inst.r.get(p_id) or inst.r.get(str(p_id)) or [])
                result_data[p_id] = {'coords': coords, 'score': score}

        elif algo == "DpIdpDh":
            # DpIdpDh stores scores as {id: score} in inst.score
            for p_id, score in getattr(inst, 'score', {}).items():
                coords = list(inst.r.get(p_id) or inst.r.get(str(p_id)) or [])
                result_data[p_id] = {'coords': coords, 'score': score}

        elif algo == "CoskyAlgorithme":
            # CoskyAlgorithme stores scores as {id: [..., score]} in inst.s
            s_dict = getattr(inst, "s", {})
            for p_id in s_dict:
                coords = list(inst.r.get(p_id) or inst.r.get(str(p_id)) or [])
                result_data[p_id] = {'coords': coords, 'score': s_dict[p_id][-1]}

        elif algo == "CoskySQL":
            # CoskySQL stores results as {id: [coords..., score]} in inst.dict
            for p_id, vals in getattr(inst, 'dict', {}).items():
                result_data[p_id] = {'coords': vals[:-1], 'score': vals[-1]}

        elif algo == "RankSky":
            # RankSky internally unifies to MIN space; rTupleInit and prefInit
            # are used to re-apply "auto" unification and match the coordinate
            # space of all_pts for consistent visualization.
            s_dict = getattr(inst, 'score', {})
            raw = {k: list(v) for k, v in getattr(inst, 'rTupleInit', {}).items()}
            prefs_list = list(getattr(inst, 'prefInit', []))
            if raw and prefs_list:
                unifier = DataUnifier(raw, prefs_list, mode="auto")
                raw = unifier.unify()
            for p_id in s_dict:
                coords = list(raw.get(p_id) or raw.get(str(p_id)) or [])
                result_data[p_id] = {'coords': coords, 'score': s_dict[p_id][-1]}

        return result_data

    def view_skyline_points(self):
        if not self.lastAppInstance: return
        pts = self.get_skyline_points()
        all_pts = self.get_all_points()
        
        if not pts:
            QMessageBox.information(self, "Skyline", "No points found.")
            return
        self.skyline_win = QWidget()
        self.skyline_win.setWindowTitle("Skyline Points")
        layout = QVBoxLayout(self.skyline_win)
        
        info_label = QLabel(f"Total Points in Dataset (Unified): {len(all_pts)} | Skyline Points: {len(pts)}")
        layout.addWidget(info_label)
        
        ta = QTextEdit()
        ta.setReadOnly(True)
        
        # Formats each point as a readable line showing its ID, coordinates, and score
        lines = []
        for p_id, data in pts.items():
            lines.append(f"ID: {p_id} | Coords: {data['coords']} | Score: {data['score']}")
        
        ta.setText("\n".join(lines))
        layout.addWidget(ta)
        self.skyline_win.setLayout(layout)
        self.skyline_win.resize(800, 500)
        self.skyline_win.show()

    def display_graph(self, all_pts, sky_pts):
        """
        Renders a 3D scatter plot of the unified dataset on the embedded Matplotlib canvas.
        Skyline points are drawn in red (with a Pareto front surface when at least 4 points
        are available); all other points are drawn in blue. Only 3D datasets are supported;
        a message is displayed for other dimensionalities.
        """
        if not all_pts:
            return

        dim = len(next(iter(all_pts.values())))
        if dim != 3:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f"Visualization only supported for 3D data\n(Current: {dim}D)",
                    ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        # String-key normalization ensures consistent lookups across algorithms
        all_pts_str = {str(k): v for k, v in all_pts.items()}
        sky_ids_str = {str(k) for k in sky_pts.keys()}
        all_ids_str = set(all_pts_str.keys())
        other_ids_str = all_ids_str - sky_ids_str

        if other_ids_str:
            other_coords = np.array([all_pts_str[i] for i in other_ids_str])
            ax.scatter(other_coords[:, 0], other_coords[:, 1], other_coords[:, 2],
                       c='blue', label='Others', s=20, alpha=0.6)

        if sky_ids_str:
            sky_coords = np.array([all_pts_str[i] for i in sky_ids_str if i in all_pts_str])
            if sky_coords.size > 0:
                ax.scatter(sky_coords[:, 0], sky_coords[:, 1], sky_coords[:, 2],
                           c='red', label='Skyline', s=50, edgecolors='black')

                # Pareto front surface via Delaunay triangulation; requires at least 4 non-collinear points
                if len(sky_coords) >= 4:
                    try:
                        ax.plot_trisurf(sky_coords[:, 0], sky_coords[:, 1], sky_coords[:, 2],
                                        color='red', alpha=0.3)
                    except Exception as e:
                        print(f"Pareto surface plotting failed (triangulation): {e}")

        # Axis labels and title
        ax.set_xlabel('Dim 1')
        ax.set_ylabel('Dim 2')
        ax.set_zlabel('Dim 3')
        ax.set_title(f'Skyline Visualization (3D)')
        ax.legend()
        
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    win = AppUIPyQt()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AppUIPyQt()
    win.show()
    sys.exit(app.exec_())
