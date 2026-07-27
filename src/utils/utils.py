import polars as pl
from dateutil.relativedelta import relativedelta
from datetime import datetime


def events_filter(df_events: pl.DataFrame, year: int, month: int) -> pl.DataFrame: 

    date_init = datetime(year, month, 1, 0, 0, 0)
    date_end  = date_init + relativedelta(months= 1) - relativedelta(minutes=1)

    df_events = df_events.filter(
        ((pl.col("Inicio") <= date_end)) &
        ((pl.col("Fin") >= date_init) | pl.col("Fin").is_null())
    )

    df_events = df_events.with_columns(
        (pl.when(pl.col("Inicio")< date_init).then(date_init).otherwise(pl.col("Inicio"))).alias("Inicio"),
        (pl.when(pl.col("Fin").is_null()).then(date_end).otherwise(pl.col("Fin"))).alias("Fin")
    )

    sacar_columna = ["Umbral [W/m2]", "N° ST", "ST: Activo / Grupo / Clasificación 1 / Clasificación 2", "ST: Observaciones", "Medidor Comunicando con Normalidad (SCADA y PRMTE)",
                     "NCU(s) Encendidas y Comunicando", "Crea registro", "Cierra registro","Creación del Registro", "Se puede acceder al Servidor con Normalidad",
                     "Fracttal: Clasificación 1 / Clasificación 2", "Inicia Registro", "Cierra Registro", "Idioma", "Descripción reporte Bluetree", "Fila", "Estado",
                     "Observaciones posterior a la apertura", "Sensores de Radiación, Temperatura y Viento Comunicando con Normalidad", 
                     "Trackers comunicando y realizando Seguimiento con Normalidad","Inversores Comunicando y Generando con Normalidad",
                     "Reconectador Comunicando con Normalidad", "ST (Estado última revisión)","Descripción Fracttal", "Comentarios Adicionales"]

    return df_events.drop(sacar_columna,strict=False)

def filter_year_month(df: pl.DataFrame, year:int, month: int) -> pl.DataFrame:

    date_column_name = ["timestamp", "Date/Time", "hour_interval"]

    for time in date_column_name:

        try:
            df = df.filter((pl.col(time).dt.year()==year) & 
                           (pl.col(time).dt.month()==month))
            break
            
        except pl.exceptions.ColumnNotFoundError:
            continue
    
    return df


def add_portfolio(df: pl.DataFrame, plant_db: pl.DataFrame):


    portfolio = plant_db.select(["id","portfolio", "measure_point", "rcc_name", "OM_name"])

    portfolio = portfolio.rename({"measure_point":"Measure Point"})

    if "id" in df.columns:

        df = df.join(
            other= portfolio,
            on= "id",
            how="left"
        )

    elif "Measure Point" in df.columns:

        df = df.join(
            other= portfolio,
            on = "Measure Point",
            how= "left"
        )

    elif "Portafolio" in df.columns and "Parque" in df.columns:

        df = df.rename({"Parque": "rcc_name"}).drop("Portafolio")

        df = df.join(
            other=portfolio,
            on = "rcc_name",
            how="left"
        )


    df = df.drop(["Measure Point", "rcc_name"])

    return df

month_map = {
    1 : "Enero",
    2 : "Febrero",
    3 : "Marzo",
    4 : "Abril",
    5 : "Mayo",
    6 : "Junio",
    7 : "Julio",
    8 : "Agosto",
    9 : "Septiembre",
    10 : "Octubre",
    11 : "Noviembre",
    12 : "Diciembre"
}

folder_names = {
    1 : "01. Enero",
    2 : "02. Febrero",
    3 : "03. Marzo",
    4 : "04. Abril",
    5 : "05. Mayo",
    6 : "06. Junio",
    7 : "07. Julio",
    8 : "08. Agosto",
    9 : "09. Septiembre",
    10 : "10. Octubre",
    11 : "11. Noviembre",
    12 : "12. Diciembre"
}