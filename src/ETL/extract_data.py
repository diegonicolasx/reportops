import polars as pl
import datetime
from pathlib import Path

from src.etl.utils import temperature_processing, events_filter

import os
import psycopg2
from psycopg2.extensions import connection  # <--- AGREGAS ESTA LÍNEA
from dotenv import load_dotenv

load_dotenv()

def get_dwh_conninfo() -> str:
    """Construye la cadena de conexión desde variables individuales del .env"""
    user = os.getenv("db_user")
    password = os.getenv("db_password")
    host = os.getenv("db_host")
    port = os.getenv("db_port")
    dbname = os.getenv("db_name")

    # Verifica que existan todas
    if not all([user, password, host, port, dbname]):
        raise RuntimeError(
            "Faltan variables de entorno para la conexión a PostgreSQL."
        )

    # psycopg acepta formato diccionarios/keyword strings sin necesidad de codificar caracteres especiales
    return f"host={host} port={port} dbname={dbname} user={user} password={password}"

def _to_polars_dataframe(data: list[dict]) -> pl.DataFrame:
    """Convierte la lista de diccionarios a un DataFrame de Polars."""
    return pl.DataFrame(data, infer_schema_length=None)

def _get_the_plantdb(conn: connection) -> list[dict]:
    """Obtiene los datos de la tabla plantdb desde la base de datos DYR."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM ods.plant_db
            WHERE om_status = 'Active'; 
            """)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
    return _to_polars_dataframe(data)

def _get_plant_poa_irradiance(conn: connection,year:int, month:int):

    """Obtiene los datos de la tabla plant_poa_irradiance desde la base de datos DYR."""

    query = """
        SELECT id_parq as id, fch_dato as timestamp, rad_valor, id_compensacion
        FROM ods.plant_poa_irradiance
        WHERE EXTRACT(MONTH FROM fch_dato) = %s 
        AND EXTRACT(YEAR FROM fch_dato) = %s
        ORDER BY id_parq ASC, fch_dato ASC;
    """
    with conn.cursor() as cur:
        cur.execute(query, (month, year))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]

    return _to_polars_dataframe(data)

def _get_panel_temperature(conn: connection,year:int, month:int):

    """Obtiene los datos de la tabla plant_poa_irradiance desde la base de datos DYR."""
    
    query = """
        SELECT id_parq AS id, fch_dato AS timestamp, temp_valor, id_compensacion
        FROM ods.plant_panel_temperature
        WHERE EXTRACT(MONTH FROM fch_dato) = %s 
        AND EXTRACT(YEAR FROM fch_dato) = %s
        ORDER BY id_parq ASC, fch_dato ASC;
    """
    with conn.cursor() as cur:
        cur.execute(query, (month, year))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
    
    return _to_polars_dataframe(data)


def _get_ambient_temperature(conn: connection, year:int, month:int):

    """Obtiene los datos de la tabla plant_ambient_temperature desde la base de datos DYR."""
    
    query = """
        SELECT id_parq AS id, fch_dato AS timestamp, temp_valor, id_compensacion
        FROM ods.plant_ambient_temperature
        WHERE EXTRACT(MONTH FROM fch_dato) = %s 
        AND EXTRACT(YEAR FROM fch_dato) = %s
        ORDER BY id_parq ASC, fch_dato ASC;
    """
    with conn.cursor() as cur:
        cur.execute(query, (month, year))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
    
    return _to_polars_dataframe(data)

def _get_prmte(conn: connection, year:int, month:int):

    """ Obtiene los datos del prmte, dicha tabla se encuentran en la base de datos DYR"""

    query = """
        SELECT 
            id_parq AS id, 
            date_time AS timestamp, 
            kwh_del_int, 
            kvarh_del_int, 
            kwh_rec_int, 
            kvarh_rec_int
        FROM ods.prmte
        WHERE EXTRACT(MONTH FROM date_time) = %s 
            AND EXTRACT(YEAR FROM date_time) = %s
        ORDER BY id ASC, timestamp ASC;
    """

    with conn.cursor() as cur:
        cur.execute(query, (month, year))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
        
    return _to_polars_dataframe(data)

def _sensor_exclusion(conn: connection, year:int, month):

    query = """
        SELECT id_sensor, id_parq, variable, inicio, fin 
        FROM ods.sensor_exclusions
        WHERE inicio < (MAKE_DATE(%s, %s, 1) + INTERVAL '1 month')
        AND (fin >= MAKE_DATE(%s, %s, 1) OR fin IS NULL);
    """
    with conn.cursor() as cur:
        cur.execute(query, (year, month, year, month))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]

    return _to_polars_dataframe(data)

###################################################################################################################

def extract_parks(conn: connection = None,year:int = None, month:int = None) -> list[pl.DataFrame, pl.DataFrame]:

    '''
    Retorna una lista con 2 Dataframes de polars, con datos de Irradiancia inclinada y generación (en Kwh).

    Parametros
    ----------

    option
        Determina se extraen los datos de manera local o del servidor.
        1. Carga los datos desde la carpeta results de stage
        2. Consulta SQL con datos del servidor DYR

    year
        filtra el año de parks, debe ser menor o igual al año actual

    month
        filtra el mes de interes. 
 
    '''
    assert year is not None and month is not None, "Debe ingresar valor para año y mes"

    path = Path(r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\parks.parquet")

    today = datetime.date.today()



    assert 1 <= month <= 12, "El mes debe estar entre 1 y 12"
    assert (year, month) <= (today.year, today.month), "La fecha no puede ser futura"

    parks = pl.read_parquet(path)

    parks = (
        parks.filter(
            (pl.col("timestamp").dt.year()==year) &
            (pl.col("timestamp").dt.month() == month)
            )
        )

    injection = parks.select(["id", "timestamp", "injection_kWh"])

    if conn is None:

        poa = parks.select(["id", "timestamp", "plane_of_array_irradiance_(W/m2)"])
        
    

    else: # opcion 2

        poa = _get_plant_poa_irradiance(conn,year,month)

    return poa, injection


def extract_panel_temperature(conn: connection = None,year:int = None, month:int = None) -> pl.DataFrame:

    '''
    Retorna un dataframe con la temperatura de panel o ambiente de los parques.

    Parametros
    ----------

    option
        Determina se extraen los datos de manera local o del servidor.
        1. Carga los datos desde la carpeta results de stage
        2. Consulta SQL con datos del servidor DYR

    year
        filtra el año de parks, debe ser menor o igual al año actual

    month
        filtra el mes de interes. 

    type
        Permite seleccionar temperatura de panel o ambiente
 
    '''

    path = Path(r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\parks_panel_temperature.parquet")

    today = datetime.date.today()
    assert year is not None and month is not None, "El año y mes no tienen valores"

    assert 1 <= month <= 12, "El mes debe estar entre 1 y 12"
    assert (year, month) <= (today.year, today.month), "La fecha no puede ser futura"


    if conn is None :

        temperature = pl.read_parquet(path)
        temperature = (
            temperature.filter(
                (pl.col("timestamp").dt.year()==year) &
                (pl.col("timestamp").dt.month() == month)
            )
        )
        temperature = temperature_processing(temperature, "panel")

    else: 

        temperature = _get_panel_temperature(conn,year,month)
    #print(_sensor_exclusion(conn, year, month))

    return temperature

def extract_ambient_temperature(conn: connection = None,year:int = None, month:int = None):

    '''
        Retorna un dataframe con la temperatura de panel o ambiente de los parques.

        Parametros
        ----------

        option
            Determina se extraen los datos de manera local o del servidor.
            1. Carga los datos desde la carpeta results de stage
            2. Consulta SQL con datos del servidor DYR

        year
            filtra el año de parks, debe ser menor o igual al año actual

        month
            filtra el mes de interes. 

        type
            Permite seleccionar temperatura de panel o ambiente
    
    '''
    path = Path(r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\parks_ambient_temperature.parquet")

    today = datetime.date.today()

    assert year is not None
    assert month is not None

    assert 1 <= month <= 12, "El mes debe estar entre 1 y 12"
    assert (year, month) <= (today.year, today.month), "La fecha no puede ser futura"


    if connection is None :

        temperature = pl.read_parquet(path)
        temperature = (
            temperature.filter(
                (pl.col("timestamp").dt.year()==year) &
                (pl.col("timestamp").dt.month() == month)
            )
        )

    else: # opcion 2

        temperature = _get_ambient_temperature(conn,year,month)


    temperature = temperature_processing(temperature, "ambient")

    return temperature

    
def extract_projected(conn: connection = None,year:int = None, month:int = None) -> pl.DataFrame:

    path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\projected_data.parquet"

    if conn is None:

        projected_data = pl.read_parquet(path)

        projected_data = (
            projected_data.filter(
                (pl.col("hour_interval").dt.year()==year) & (pl.col("hour_interval").dt.month()==month)
            )
            .select(["id", "hour_interval", "projected_plane_of_array_irradiation_(kWh/m2)", "projected_injection_(kWh)"])
            .rename({
                "hour_interval":"timestamp",
                "projected_plane_of_array_irradiation_(kWh/m2)": "poa_irradiation_projected",   
                })
            .sort(["id", "timestamp"])
        )

    #else: # option 2 aca se hace la consulta SQL

        ## Codigo por escribir, no existe tabla en el servidor de proyectados

    return projected_data
    
def plant_db(conn: connection = None) -> pl.DataFrame:

    path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\plant_db.parquet"

    if connection is None:

        plant_db = pl.read_parquet(path)
    
    else: #option 2

        plant_db = _get_the_plantdb(conn)

    return plant_db

def portfolio(conn:connection= None) -> pl.DataFrame:

    if conn == None:
        return None

    query = """SELECT id, portfolio_name, project_manager FROM ods.portfolio"""

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
            
    return _to_polars_dataframe(data)
    

def extract_prmte(conn: connection = None,year:int = None, month:int = None):

    assert year is not None
    assert month is not None

    today = datetime.date.today()
    
    assert 1 <= month <= 12, "El mes debe estar entre 1 y 12"
    assert (year, month) <= (today.year, today.month), "La fecha no puede ser futura"

    path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\prmte_consolidado.parquet"

    if conn is None:

        prmte = pl.read_parquet(path)
        prmte = (
            prmte.filter(
            (pl.col("Date/Time").dt.year()==year) & (pl.col("Date/Time").dt.month()==month)
        )
        .select(["Measure Point","Date/Time","kWh del int","kVARh del int","kWh rec int","kVARh rec int"])
        .rename({"Date/Time":"timestamp"})
        )

    else: # option 2

        prmte = _get_prmte(conn, year, month)

    return prmte


def extract_rcc(conn: connection = None,year:int = None, month:int = None, type:str = None) -> pl.DataFrame:

    assert year is not None
    assert month is not None

    assert type in ["recloser", "inverter", "limitations", "restrictions"], "tipo no valido"

    if type == "recloser":

        path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\rcc_recloser_events.parquet"

    elif type == "inverter":

        path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\rcc_events.parquet"

    elif type == "limitations":

        path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\rcc_limitations.parquet"
    
    else: #restrictions

        path = r"C:\OENERGY Dropbox\0600-O&M\611 - Datos y reportería\projects\stage\results\rcc_restrictions.parquet"

    if conn is None:

        df_event = pl.read_parquet(path)

        df_event = events_filter(df_event, year, month)

    
    #else : ## option 2

        # implementar como consulta SQL

    return df_event

    