import polars as pl
import os
from pathlib import Path
import datetime

from src.ETL.etl import ReportETL

current_date = datetime.datetime.today()

print("\n")

## parte del codigo que obtiene el año del reporte
while True:

    try:
        year = int(input(f"Ingrese año del reporte ({current_date.year - 1} o {current_date.year}): "))
        print("\n")

        if current_date.year -1 <= year <= current_date.year:
            break
        else:
            print(f"Año no disponible, debe ser entre {current_date.year -1} y {current_date.year} \n")

    except ValueError:
        print("Error en el formato \n")

## obtención del mes

while True:

    try:
        month = int(input("Ingrese el numero del mes del reporte deseado (mm): "))
        print("\n")

        if year == current_date.year and month >= current_date.month:

            if month > 12 or month <1:
                print("Numero de mes fuera de rango. Debe estar entre 1 y 12 \n")
                continue

            if year == current_date.year and month >= current_date.month:
                print(f"Error: Los datos de {month}/{year} aún no están disponibles.\n")

        else:
            break
    
    except ValueError:
        print("Error en el formato \n")


## Traer los datos de las bases de datos. La Radiación de los pira, la temperatura de panel, los datos del prmte, los datos de inyeccion,
## datos proyectados
## Los datos del RCC, datos de curtailment

path_1 = Path(r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results")
path_2 = Path()

plant_db     = pl.read_parquet(path_1 / "plant_db.parquet")

poa          = pl.read_parquet(path_1 / "parks_poa_irradiance.parquet")

temp_panel   = pl.read_parquet(path_1 / "parks_panel_temperature.parquet")

temp_amb     = pl.read_parquet(path_1 / "parks_ambient_temperature.parquet")

prmte        = pl.read_parquet(path_1 / "prmte_consolidado.parquet")

projected    = pl.read_parquet(path_1 / "projected_data.parquet")

reco_events  = pl.read_parquet(path_1 / "rcc_recloser_events.parquet")

equip_events = pl.read_parquet(path_1 / "rcc_events.parquet")

curtailments = pl.read_parquet(path_1 / "rcc_limitations.parquet")

Data = ReportETL(poa, temp_panel, temp_amb, prmte, projected, reco_events, equip_events, curtailments, year, month)

print(Data.poa_irradiation)