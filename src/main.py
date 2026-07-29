import polars as pl
import os
from pathlib import Path
import datetime

from src.etl.etl import Extractor, Park
from src.group_1.group1_report import G1_report

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


extractor = Extractor(year, month).run()

plant_db = extractor.plant_db

parque = Park(id=54, extractor=extractor)

example = G1_report(parque)

example.run()



