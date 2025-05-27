import os, sys, ast, sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QComboBox, QTextEdit, QLineEdit, QMessageBox,
    QFrame, QMainWindow, QStackedWidget, QInputDialog
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial import ConvexHull
import numpy as np

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

class AppUIPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyRank - Algorithm Runner [PyQt]")
        self.setGeometry(100, 100, 1200, 800)
        self.selectedDataPath = None
        self.lastAppInstance = None
        self.tableName = "Pokemon"
        self.initUI()

    def initUI(self):
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

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        main_layout.addLayout(control_layout, 1)
        main_layout.addWidget(self.canvas, 2)

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
        # Nettoie complètement le layout fileFrame
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
        try:
            dtype = self.dataCombo.currentText()
            algo_name = self.algoCombo.currentText()
            out_fmt = self.outputCombo.currentText()

            data = self.load_data(dtype)
            nb_cols = self.count_columns(data, dtype)

            prefs = None
            if algo_name in ("RankSky", "CoskyAlgorithme", "CoskySQL"):
                s, ok = QInputDialog.getText(self, "Preferences", f"{nb_cols} columns detected.\nEnter {nb_cols} values (min/max) comma-separated:")
                if not ok or not s: return
                parts = [p.strip().lower() for p in s.split(",")]
                if len(parts) != nb_cols or any(p not in ("min", "max") for p in parts):
                    QMessageBox.critical(self, "Error", "Incorrect preference list.")
                    return
                prefs = [Preference.MIN if p == "min" else Preference.MAX for p in parts]

            algo_cls = {"SkyIR": SkyIR, "DpIdpDh": DpIdpDh,
                        "CoskyAlgorithme": CoskyAlgorithme, "CoskySQL": CoskySQL,
                        "RankSky": RankSky}[algo_name]

            exporter = CsvExporterImpl("../Assets/Export/CSVFiles/Results.csv") if out_fmt == "CSV" \
                      else JsonExporterImpl("../Assets/Export/JsonFiles/Result.json")

            app = App(data, algo_cls, exporter=exporter,
                      input_type=dtype, input_file=self.selectedDataPath or "inline",
                      preferences=prefs)
            self.lastAppInstance = app
            self.statusLabel.setText(f"Done in {app.execution_time}s")

            all_data = self._extract_all_points(data)
            skyline = self.get_skyline_points()
            self.display_graph(all_data, skyline)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.statusLabel.setText(f"Error: {e}")

    def _extract_all_points(self, data_obj):
        if isinstance(data_obj, DictObject): return list(data_obj.r.values())
        if isinstance(data_obj, JsonObject): return list(readJson(data_obj.fp).values())
        if isinstance(data_obj, DbObject):
            con = sqlite3.connect(data_obj.fp)
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.tableName}")
            rows = [list(row[1:]) for row in cur.fetchall()]
            con.close()
            return rows
        return []

    def get_skyline_points(self):
        algo = self.lastAppInstance.algo
        inst = self.lastAppInstance.algo_instance
        result = []
        if algo == "SkyIR": result = inst.result
        elif algo == "DpIdpDh": result = inst.score
        elif algo == "CoskyAlgorithme": result = getattr(inst, "s", [])
        elif algo == "CoskySQL": result = inst.dict
        elif algo == "RankSky": result = inst.score
        if isinstance(result, dict): return [v[:3] for v in result.values()]
        return [r[:3] if isinstance(r, (list, tuple)) and len(r) > 3 else r for r in result]

    def display_graph(self, all_points, skyline_points):
        self.figure.clear()
        n_dim = len(all_points[0]) if all_points else 0
        all_array = np.array(all_points)
        sky_indices = []
        for i, pt in enumerate(all_points):
            for sp in skyline_points:
                if np.allclose(pt[:3], sp[:3], atol=1e-6):
                    sky_indices.append(i)
                    break

        if n_dim == 3:
            ax = self.figure.add_subplot(111, projection='3d')
            max_vals = np.max(all_array, axis=0)
            norm_all = all_array / max_vals
            norm_sky = norm_all[sky_indices]
            ax.scatter(norm_all[:, 0], norm_all[:, 1], norm_all[:, 2], color='lightgray', label='All Points')
            ax.scatter(norm_sky[:, 0], norm_sky[:, 1], norm_sky[:, 2], color='blue', label='Skyline')

            # Message informatif sur l'enveloppe
            ax.text2D(0.05, 0.95, "⚠️ Pareto envelope display under development",
                      transform=ax.transAxes, fontsize=9, color='red')

            ax.set_xlabel("Dim 1")
            ax.set_ylabel("Dim 2")
            ax.set_zlabel("Dim 3")
            ax.set_title("Skyline 3D (normalized by max of each dimension)")
            ax.legend()
        else:
            ax = self.figure.add_subplot(111)
            """reduced = PCA(n_components=2).fit_transform(StandardScaler().fit_transform(all_array))
            all_x, all_y = reduced[:, 0], reduced[:, 1]
            sky_x, sky_y = reduced[sky_indices, 0], reduced[sky_indices, 1]
            ax.scatter(all_x, all_y, color='lightgray', label='All Points')
            ax.scatter(sky_x, sky_y, color='blue', label='Skyline')

            # Ligne reliant les points Skyline (approximation visuelle)
            skyline_proj = np.column_stack((sky_x, sky_y))
            skyline_sorted = skyline_proj[np.argsort(skyline_proj[:, 0])]
            ax.plot(skyline_sorted[:, 0], skyline_sorted[:, 1], color='red', linestyle='--')"""

            # Message informatif
            ax.text(0.05, 0.95,
                    "🔧 Work in progress: visualization for n > 3\n⚠️ Pareto envelope display under development",
                    transform=ax.transAxes, fontsize=9, color='darkred', verticalalignment='top')

            """ax.set_title("Skyline (blue) vs All Points")
            ax.set_xlabel("Component 1")
            ax.set_ylabel("Component 2")
            ax.legend()"""

        self.canvas.draw()

    def view_skyline_points(self):
        if not self.lastAppInstance: return
        pts = self.get_skyline_points()
        if not pts:
            QMessageBox.information(self, "Skyline", "No points.")
            return
        win = QWidget(); win.setWindowTitle("Skyline Points")
        layout = QVBoxLayout(win)
        ta = QTextEdit(); ta.setReadOnly(True)
        ta.setText("\n".join(str(p) for p in pts))
        layout.addWidget(ta)
        win.setLayout(layout)
        win.resize(600, 400)
        win.show()

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
