import pandas as pd
from pandas.core.frame import DataFrame


class CsvUtils:
    data: DataFrame = None

    def __init__(self, path):
        self.data = pd.read_csv(path, encoding="utf8")

    def get_rows_count(self) -> int:
        return self.data.index.stop

class ExcelUtils:
    data: DataFrame = None

    def __init__(self, path):
        self.data = pd.read_excel(path, encoding="utf8")

    def get_rows_count(self) -> int:
        return self.data.index.stop


