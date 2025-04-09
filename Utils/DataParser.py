from Utils.DisplayHelpers import beauty_print


class DataParser:
    '''
    Class that converts data from SQL to Python dictionnary
    '''

    def __init__(self, sql_r):
        self.sql_r = sql_r
        self.r_dict = self.convert()

    def convert(self):
        """
        Dictionnairy comprehension that browse all value of sql data as rows
        and says:
        for each row, set the first item (the rowId) as dict key and
        set all the others items as values of the dict (as tuple)
        :return: a dict
        """
        return {row[0]: tuple(row[1:]) for row in self.sql_r}


if __name__ == '__main__':
    sql_mocked_data = [
        (113, 2.338051603173262, 10.0, 8.0, 0.9994496256117908),
        (36, 21.724758982092293, 14.0, 1.0, 0.9993371656483069),
        (107, 1.5110941873035157, 28.0, 35.0, 0.99927561806547),
        (24, 9.263094251670024, 16.0, 2.0, 0.9991351226476496),
        (9, 2.8212050762655942, 26.0, 5.0, 0.9988719431546644),
        (93, 3.4203354154576897, 29.0, 4.0, 0.99881053840203),
        (60, 9.075909010000602, 84.0, 2.0, 0.9986403889153475),
        (21, 8.234437316470686, 341.0, 1.0, 0.9985313707781033),
        (43, 4.987318221841807, 2.0, 5.0, 0.997989306525854),
        (142, 1.7881435389547091, 12.0, 91.0, 0.9683268163963421),
        (151, 70.1199889839427, 3.0, 1.0, 0.8794678649829318),
        (173, 693.781687617284, 1.0, 16.0, 0.09626256217786015),
        (172, 41.198923823374265, 1.0, 970.0, 0.06641218581234878),
        (101, 4.834603099880525, 3.0, 3204.0, 0.06302910115594923),
        (55, 6782.825861471301, 2.0, 4.0, 0.04981822323506108),
        (32, 3.56779018094784, 1.0, 7799.0, 0.04246159650684594)
    ]

    data_parser_obj = DataParser(sql_mocked_data)
    #beauty_print("converted data from sql format",data_parser_obj.r_dict)
