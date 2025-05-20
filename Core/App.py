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
        self.exporter = exporter
        self.algo_instance = None
        self.execution_time = 0
        self.pref = preferences
        self.input_type = input_type or "Unknown"
        self.input_file = input_file or "generated"

        if isinstance(data, DictObject):
            self.r, self.dataName = data.r, "DictObject"
            self.cardinality = len(next(iter(self.r.values())))
            self.tuples = len(self.r)
        elif isinstance(data, JsonObject):
            self.jsonFp, self.dataName = data.fp, "JsonObject"
            self.cardinality = len(data.data[next(iter(data.data))])
            self.tuples = len(data.data)
        elif isinstance(data, DbObject):
            self.dbFp, self.dataName = data.fp, "DbObject"
            self.cardinality = self._count_db_columns(self.dbFp) - 1
            self.tuples = self._count_db_rows(self.dbFp)
        else:
            raise ValueError("Unsupported data type")

        if self.pref is not None and len(self.pref) != self.cardinality:
            raise ValueError(
                f"Preference list length ({len(self.pref)}) "
                f"does not match column count ({self.cardinality})"
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
        match self.algo:
            case "CoskyAlgorithme": self._start_cosky_algorithme()
            case "CoskySQL":        self._start_cosky_sql()
            case "DpIdpDh":         self._start_dp_idp_dh()
            case "RankSky":         self._start_ranksky()
            case "SkyIR":           self._start_skyir()
            case _:                 raise ValueError("Unknown algorithm")

    def _start_cosky_sql(self):
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
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("PRAGMA table_info(Pokemon)")
        n = len(cur.fetchall())
        con.close()
        return n

    @staticmethod
    def _count_db_rows(db_path):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Pokemon")
        n = cur.fetchone()[0]
        con.close()
        return n
