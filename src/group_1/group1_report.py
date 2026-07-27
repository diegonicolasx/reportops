import polars as pl
import os
from src.etl.etl import Park
from src.group_1.data import data_g1
from xlsxwriter import Workbook
from src.utils.utils import month_map, folder_names
# Grupo 1 (G1) hace referencia a Blue Elephant: condor solar y aguila solar


class G1_report:

    def __init__(self, park: Park):

        self.report = None
        self.park   = park
        self.file_name = self._file_name()
        self.result_path = self._path_dir()

        print(self.result_path)

    def run(self):

        os.makedirs(self.result_path, exist_ok= True)

        with Workbook(os.path.join(self.result_path, self.file_name)) as wb:

            ws_data = wb.add_worksheet("Data")

            data_g1(workbook= wb,
                    worksheet= ws_data,
                    park= self.park)


    def _path_dir(self):

        path = self.park.path
        month_file = folder_names[self.park.month]
        path = os.path.join(path, self.park.portfolio, str(self.park.year), month_file)

        return path

    def _file_name(self) -> str:

        month_name = month_map[self.park.month]
        file_name = f"Generation Report {month_name} {self.park.year} - {self.park.om_name}.xlsx"

        return file_name


    
