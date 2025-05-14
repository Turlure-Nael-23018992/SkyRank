import os, sys, sqlite3, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algorithms.CoskySql import CoskySQL
from Algorithms.CoskyAlgorithme import CoskyAlgorithme
from Algorithms.DpIdpDh import DpIdpDh
from Algorithms.RankSky import RankSky
from Algorithms.SkyIR import SkyIR

from Database.DatabaseHelpers import Database
from Utils.Preference import Preference
from Utils.DataModifier.DataConverter import DataConverter
from Utils.DataTypes.JsonObject import JsonObject
from Utils.DataTypes.DbObject import DbObject
from Utils.DataTypes.DictObject import DictObject
from Utils.DisplayHelpers import print_red


class App:
    """
    Unified interface to execute Skyline algorithms on various data types
    (Dictionary, JSON, or Database) and optionally export the results.
    """

    def __init__(self, data, algo, exporter=None,
                 input_type=None, input_file=None, preferences=None):
        """
        Initialize the App and run the selected algorithm.

        :param data: Input data object (DictObject, JsonObject, or DbObject)
        :param algo: Algorithm class to execute
        :param exporter: Exporter object (CSV or JSON)
        :param input_type: Type of input (for logging or metadata)
        :param input_file: Input file name or identifier
        :param preferences: List of preferences (MIN or MAX) for each column
        """
        self.exporter = exporter
        self.algo_instance = None
        self.execution_time = 0
        self.pref = preferences
        self.input_type = input_type or "Unknown"
        self.input_file = input_file or "generated"

        if isinstance(data, DictObject):
            self.r, self.dataName = data.r, "DictObject"
            nb_cols = len(next(iter(self.r.values())))
        elif isinstance(data, JsonObject):
            self.jsonFp, self.dataName = data.fp, "JsonObject"
            nb_cols = len(data.data[next(iter(data.data))])
        elif isinstance(data, DbObject):
            self.dbFp, self.dataName = data.fp, "DbObject"
            nb_cols = self._count_db_columns(self.dbFp) - 1
        else:
            raise ValueError("Unsupported data type")

        if self.pref is not None and len(self.pref) != nb_cols:
            raise ValueError(
                f"Preference list length ({len(self.pref)}) "
                f"does not match column count ({nb_cols})"
            )

        self.algo = algo.__name__

        start = time.perf_counter()
        self._dispatch()
        self.execution_time = round(time.perf_counter() - start, 6)

        if self.algo_instance and not hasattr(self.algo_instance, "time"):
            self.algo_instance.time = self.execution_time
        if self.exporter:
            self.exporter.export(self)

    def _dispatch(self):
        """
        Dispatch the algorithm execution based on its name.
        """
        match self.algo:
            case "CoskyAlgorithme": self._start_cosky_algorithme()
            case "CoskySQL":        self._start_cosky_sql()
            case "DpIdpDh":         self._start_dp_idp_dh()
            case "RankSky":         self._start_ranksky()
            case "SkyIR":           self._start_skyir()
            case _:                 raise ValueError("Unknown algorithm")

    def _start_cosky_sql(self):
        """
        Launch the CoskySQL algorithm based on the data format.
        """
        print_red("Starting CoskySQL")
        if self.dataName == "DbObject":
            self.algo_instance = CoskySQL(self.dbFp, self.pref)
        elif self.dataName == "JsonObject":
            DataConverter(self.jsonFp).jsonToDb()
            self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db", self.pref)
        else:
            DataConverter(self.r).relationToDb()
            self.algo_instance = CoskySQL("../Assets/AlgoExecution/DbFiles/TestExecution.db", self.pref)

    def _start_cosky_algorithme(self):
        """
        Launch the CoskyAlgorithme algorithm based on the data format.
        """
        print_red("Starting CoskyAlgorithme")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = CoskyAlgorithme(rel, self.pref)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = CoskyAlgorithme(rel, self.pref)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = CoskyAlgorithme(self.r, self.pref)

    def _start_dp_idp_dh(self):
        """
        Launch the DpIdpDh algorithm based on the data format.
        """
        print_red("Starting DpIdpDh")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = DpIdpDh(rel)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = DpIdpDh(rel)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = DpIdpDh(self.r)

    def _start_ranksky(self):
        """
        Launch the RankSky algorithm based on the data format.
        """
        print_red("Starting RankSky")
        if self.pref is None:
            raise ValueError("RankSky requires a preference list")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = RankSky(rel, self.pref)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = RankSky(rel, self.pref)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = RankSky(self.r, self.pref)

    def _start_skyir(self):
        """
        Launch the SkyIR algorithm based on the data format.
        """
        print_red("Starting SkyIR")
        if self.dataName == "DbObject":
            rel = DataConverter(self.dbFp).dbToRelation()
            self.algo_instance = SkyIR(rel); self.algo_instance.skyIR(10)
        elif self.dataName == "JsonObject":
            rel = DataConverter(self.jsonFp).jsonToRelation()
            self.algo_instance = SkyIR(rel); self.algo_instance.skyIR(10)
        else:
            self.r = {k: tuple(v) for k, v in self.r.items()}
            self.algo_instance = SkyIR(self.r); self.algo_instance.skyIR(10)

    @staticmethod
    def _count_db_columns(db_path):
        """
        Count the number of columns in a database table.

        :param db_path: Path to the SQLite database
        :return: Number of columns
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("PRAGMA table_info(Pokemon)")
        n = len(cur.fetchall())
        con.close()
        return n


if __name__ == "__main__":
    from Utils.DataTypes.DictObject import DictObject

    relation = {
        1: (5, 20, 70),
        2: (4, 60, 50),
        3: (7, 30, 40),
        4: (6, 80, 60)
    }
    prefs = [Preference.MIN, Preference.MAX, Preference.MIN]

    print(">>> Test RankSky on DictObject")
    app_test = App(DictObject(relation), RankSky,
                   input_type="Dictionary",
                   preferences=prefs)
    print("Scores:", app_test.algo_instance.score)
    print("Time  :", app_test.execution_time, "s\n")

    print(">>> Test CoskyAlgorithme on DictObject")
    app_test2 = App(DictObject(relation), CoskyAlgorithme,
                    input_type="Dictionary",
                    preferences=prefs)
    print("Result:", app_test2.algo_instance.s)
    print("Time  :", app_test2.execution_time, "s")
