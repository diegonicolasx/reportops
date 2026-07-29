import polars as pl
from src.etl.etl import Park
from src.utils.cell_formats import *
import datetime
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
    fmt_float_2d = {k: workbook.add_format(v) for k, v in COMBINACIONES_BORDES_FLOAT_2D.items()}
    fmt_float_3d = {k: workbook.add_format(v) for k, v in COMBINACIONES_BORDES_FLOAT_3D.items()}
    fmt_date  = {k: workbook.add_format(v) for k, v in COMBINACIONES_BORDES_DATE.items()}
    #### Tabla Con la información del parque

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
    worksheet.write("G5", park.plant_info["temperature_coefficient_pct_c"].item()*100, fmt_float_2d["borde_negrita_bottom_right"])

    #### 15 minutes Series ####

    worksheet.merge_range("B7:M7", "15 Minute Series", fmt_str["borde_todos_negrita"])
    worksheet.merge_range("B8:B9", "Timestamp", fmt_str["borde_todos_negrita"])
    worksheet.write("C8", "Plane of Array Irradiance", fmt_str["borde_negrita_top_left"])
    worksheet.write("C9", "[W/m2]", fmt_str["borde_negrita_bottom_left"])
    worksheet.write("D8", "Plane of Array Irradiation", fmt_str["borde_negrita_top"])
    worksheet.write("D9","[kWh/m2]", fmt_str["borde_negrita_bottom"])
    worksheet.write("E8", "Horizontal Irradiance", fmt_str["borde_negrita_top"])
    worksheet.write("E9", "[W/m2]", fmt_str["borde_negrita_bottom"])
    worksheet.write("F8", "Horizontal Irradiation", fmt_str["borde_negrita_top_right"])
    worksheet.write("F9", "[kWh/m2]", fmt_str["borde_negrita_bottom_right"])

    worksheet.write("G8", "Panel Temperature", fmt_str["borde_negrita_top_left"])
    worksheet.write("G9", "[°C]", fmt_str["borde_negrita_bottom_left"])
    worksheet.write("H8", "Ambient Temperature", fmt_str["borde_negrita_top_right"])
    worksheet.write("H9", "[°C]", fmt_str["borde_negrita_bottom_right"])
    worksheet.write("I8", "Consumption", fmt_str["borde_negrita_top_left"])
    worksheet.write("I9", "[kWh]", fmt_str["borde_negrita_bottom_left"])
    worksheet.write("J8", "Generation", fmt_str["borde_negrita_top"])
    worksheet.write("J9", "[kWh]", fmt_str["borde_negrita_bottom"])
    worksheet.write("K8", "Mean Power", fmt_str["borde_negrita_top"])
    worksheet.write("K9", "[kWh]", fmt_str["borde_negrita_bottom"])
    worksheet.write("L8", "Theorical Generation", fmt_str["borde_negrita_top_right"])
    worksheet.write("L9", "[kWh]", fmt_str["borde_negrita_bottom_right"])
    worksheet.write("M8", "Effective Nominal Plant Power", fmt_str["borde_negrita_top_left_right"])
    worksheet.write("M9", "[kWp]", fmt_str["borde_negrita_bottom_left_right"])

    start_dt = datetime.datetime(park.year, park.month,1,0,0)

    for i in range(park.num_days * 96):

        row_idx = 9 + i
        current_dt = start_dt + datetime.timedelta(minutes=15*i)

        poa        = park.plant_poa["rad_valor"].item(i)
        ghi        = park.plant_ghi["rad_valor"].item(i)
        panel_t    = park.plant_panel_temperature["temp_valor"].item(i)
        amb_t      = park.plant_ambient_temperature["temp_valor"].item(i)
        injection  = park.plant_prmte["kwh_rec_int"].item(i)
        consumo    = park.plant_prmte["kwh_del_int"].item(i)

        if i == 0:
            worksheet.write_datetime(row_idx, 1, current_dt, fmt_date["borde_negrita_top_left_right"])
            worksheet.write(row_idx, 2, poa, fmt_int["borde_negrita_top_left"])
            worksheet.write(row_idx, 4, ghi, fmt_int["borde_negrita_top"])
            worksheet.write(row_idx, 6, panel_t, fmt_float_2d["borde_negrita_top_left"])
            worksheet.write(row_idx, 7, amb_t, fmt_float_2d["borde_negrita_top_right"])
            worksheet.write(row_idx, 8, consumo, fmt_float_3d["borde_negrita_top_left"])
            worksheet.write(row_idx, 9, injection, fmt_float_3d["borde_negrita_top"])

        elif i == (park.num_days*96 -1):
            worksheet.write_datetime(row_idx, 1, current_dt, fmt_date["borde_negrita_bottom_left_right"])
            worksheet.write(row_idx, 2, poa, fmt_int["borde_negrita_bottom_left"])
            worksheet.write(row_idx, 4, ghi, fmt_int["borde_negrita_bottom"])
            worksheet.write(row_idx, 6, panel_t, fmt_float_2d["borde_negrita_bottom_left"])
            worksheet.write(row_idx, 7, amb_t, fmt_float_2d["borde_negrita_bottom_right"])
            worksheet.write(row_idx, 8, consumo, fmt_float_3d["borde_negrita_bottom_left"])
            worksheet.write(row_idx, 9, injection, fmt_float_3d["borde_negrita_bottom"])
            
        else :
            worksheet.write_datetime(row_idx, 1, current_dt, fmt_date["borde_negrita_left_right"])
            worksheet.write(row_idx, 2, poa, fmt_int["borde_negrita_left"])
            worksheet.write(row_idx, 4, ghi, fmt_int["borde_ninguno_negrita"])
            worksheet.write(row_idx, 6, panel_t, fmt_float_2d["borde_negrita_left"])
            worksheet.write(row_idx, 7, amb_t, fmt_float_2d["borde_negrita_right"])
            worksheet.write(row_idx, 8, consumo, fmt_float_3d["borde_negrita_left"])
            worksheet.write(row_idx, 9, injection, fmt_float_3d["borde_ninguno_negrita"])