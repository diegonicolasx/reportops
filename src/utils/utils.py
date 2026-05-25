import polars as pl
from dateutil.relativedelta import relativedelta
from datetime import datetime

def events_filter(df_events: pl.DataFrame, year: int, month: int) -> pl.DataFrame: 

    date_init = datetime(year, month, 1, 0, 0, 0)
    date_end  = date_init + relativedelta(months= 1) 

    df_events = df_events.filter(
        ((pl.col("Inicio") < date_end)) &
        ((pl.col("Fin") >= date_init) | pl.col("Fin").is_null())
    )

    return df_events

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