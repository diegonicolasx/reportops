import polars as pl
from dateutil.relativedelta import relativedelta
from datetime import datetime

def temperature_processing(temp: pl.DataFrame, type:str):

    assert type in ["panel","ambient"]

    columns_name = ["panel_temperature_(°C)"]

    if type == "panel":
        columns_name.append("cell_panel_temperature_(°C)")
    else: 
        pass

    

    if "id_disp" in temp.columns:

        temp = temp.with_columns(
            pl.mean_horizontal(columns_name).alias("temp_valor")
        ).select(["timestamp","id", "id_disp", "temp_valor"])

        temp = temp.group_by(["id", "timestamp"]).agg(
                    pl.col("temp_valor").mean().alias("temp_avg")
                ).sort(by=["id", "timestamp"])

    return temp


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
                     "Reconectador Comunicando con Normalidad", "ST (Estado última revisión)","Descripción Fracttal", "Comentarios Adicionales","Estado Ajuste", "ST",
                     "Hora Correo","Creación del registro", "Fracttal: Activo / Grupo / Clasificación 1 / Clasidficación 2","Realiza el Ajuste"]

    return df_events.drop(sacar_columna,strict=False)