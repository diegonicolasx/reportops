import polars as pl
from src.etl.etl import Park
from src.utils.cell_formats import *

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet


def data_g1(
        workbook: Workbook,
        worksheet: Worksheet,
        park: Park
    ):

    worksheet.set_zoom(100)
    worksheet.hide_gridlines(2)

    anchos = [
        7, 18, 17, 17, 14, 14, 12, 12, 13, 12, 12, 12, 11, 
        15, 12, 13, 13, 13, 9, 29, 12, 12, 12, 12, 12, 12, 13, 12
    ]

    for col_idx, ancho in enumerate(anchos):
        worksheet.set_column(col_idx, col_idx, ancho)

    worksheet.set_row(2,45)
    worksheet.set_row(7,75)

    fmt_str = {k: workbook.add_format(v) for k, v in COMBINACIONES_BORDES_STR.items()}
    fmt_int = {k: workbook.add_format(v) for k, v in COMBINACIONES_BORDES_INT.items()}

    worksheet.merge_range("B2:G2", park.om_name, fmt_str["borde_todos_negrita"])
    worksheet.merge_range("B3:D3", "Meter Information", fmt_str["borde_negrita_top_left_right"])
    worksheet.write("E3", "Nominal DC Plant Power", fmt_str["borde_negrita_top_left"])
    worksheet.write("F3", "Irradiance Treshold", fmt_str["borde_negrita_top"])
    worksheet.write("G3", "Temperature Coefficient", fmt_str["borde_negrita_top_right"])
    worksheet.write("B4", "Distributor", fmt_str["borde_negrita_bottom_left"])
    worksheet.write("C4", "Substation", fmt_str["borde_negrita_bottom"])
    worksheet.write("D4", "Feeder", fmt_str["borde_negrita_bottom_right"])
    worksheet.write("E4", "[kWp]", fmt_str["borde_negrita_bottom_left"])
    worksheet.write("F4", "[W/m2]", fmt_str["borde_negrita_bottom"])
    worksheet.write("G4", "[%/°C]", fmt_str["borde_negrita_bottom_right"])
    worksheet.write("B5", park.plant_info["distributor"].item(), fmt_str["borde_negrita_bottom_left"])
    worksheet.write("C5", park.plant_info["substation"].item(), fmt_str["borde_negrita_top_bottom"])
    worksheet.write("D5", park.plant_info["feeder"].item(), fmt_str["borde_negrita_top_bottom_right"])
    worksheet.write("E5", park.plant_info["installed_capacity_mwp"].item()*1000, fmt_int["borde_negrita_top_bottom_left"])
    worksheet.write("F5", park.plant_info["irradiance_treshold_w_m2"].item(), fmt_int["borde_negrita_top_bottom"])
    worksheet.write("G5", park.plant_info["temperature_coefficient_pct_c"].item())

