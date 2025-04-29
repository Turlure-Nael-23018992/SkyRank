import time
import humanize
from datetime import timedelta


class TimeCalc:
    """
    Classe qui calcule le temps d'exécution
    """

    def __init__(self, samples_count, algo_type):
        self.samples_count=samples_count
        self.algo_type=algo_type
        self.start_time=time.time()
        self.ratio=1

    @staticmethod
    def format_time(time_to_format):

        if time_to_format>3600:
            h=time_to_format/3600
            pre_minutes=(time_to_format%3600)
            m = int(pre_minutes / 60)
            s = int(pre_minutes % 60)
            return " - ".join([str(x[0]) + x[1] for i, x in enumerate(((h, "h"), (m, "mins"), (s, "secs"))) if x[0] > 0])
        else:
            if time_to_format>60:
                m = int(time_to_format / 60)
                s = int(time_to_format % 60)
                return " - ".join([str(x[0]) + x[1] for i, x in enumerate(((m, "mins"), (s, "secs"))) if x[0] > 0])
            else:
                s=time_to_format
                return str(s)+" s"

    def get_formated_data(self):
        return f"\t[{self.algo_type}]:\n\t\t[temps]:{TimeCalc.format_time(round(self.execution_time, 10))}\n\t\t[temps/samples]:{self.ratio}"

    def stop(self):
        self.stop_time=time.time()
        self.execution_time=self.stop_time-self.start_time
        self.ratio=self.execution_time/self.samples_count
        #print(self.get_formated_data())

    @staticmethod
    def humanizeTime(time):
        """
        Convert the time to a human-readable format (Hour, Min, secs)
        """
        return humanize.precisedelta(time, minimum_unit="seconds")

if __name__ == '__main__':
    time = TimeCalc(100, "CoskySQL")
    t = 267.63728548
    print(time.humanizeTime(t))



