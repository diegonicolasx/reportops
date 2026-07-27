import polars as pl
from src.utils.utils import events_filter, filter_year_month, add_portfolio
from src.etl.extract_data import *

from dotenv import load_dotenv

load_dotenv()


class Extractor:

    def __init__(self, year: int, month: int, option: int = 2):
        self.year = year
        self.month = month
        self.option = option

        self.poa = None
        self.generation = None
        self.panel_temperature = None
        self.ambient_temperature = None
        self.plant_db = None
        self.prmte = None
        self.recloser = None
        self.inverter = None
        self.limitations = None
        self.restrictions = None

    def run(self):

        if self.option == 1:
            self._extract_all(conn=None)

        elif self.option == 2:
            with psycopg2.connect(get_dwh_conninfo()) as conn:
                self._extract_all(conn=conn)

        return self

    def _extract_all(self, conn):

        raw_plant_db = plant_db(conn)
        self.portfolio = portfolio(conn)

        self.plant_db = raw_plant_db.join(
            self.portfolio,
            left_on="id_portfolio", 
            right_on="id",          
            how="left"              
        )

        self.poa, self.generation = extract_parks(conn=conn, year=self.year, month=self.month)
        self.panel_temperature    = extract_panel_temperature(conn=conn, year=self.year, month=self.month)
        self.ambient_temperature  = extract_ambient_temperature(conn=conn, year=self.year, month=self.month)
        self.prmte                = extract_prmte(conn=conn, year=self.year, month=self.month)
        self.projected            = extract_projected(conn=None, year=self.year, month=self.month)
        self.recloser             = extract_rcc(conn=None, year=self.year, month=self.month, type="recloser")
        self.inverter             = extract_rcc(conn=None, year=self.year, month=self.month, type="inverter")
        self.limitations          = extract_rcc(conn=None, year=self.year, month=self.month, type="limitations")
        self.restrictions         = extract_rcc(conn=None, year=self.year, month=self.month, type="restrictions")

    
class Park:

    def __init__(self, id: int, extractor: Extractor):
    
        self.plant_info                = extractor.plant_db.filter(pl.col("id")==id)
        self.year                      = extractor.year
        self.month                     = extractor.month

        self.om_name = self._get_om_name()
        self.rcc_name = self._get_rcc_name()
        self.portfolio = self._get_portfolio()


        self.plant_poa                 = extractor.poa.filter(pl.col("id")==id)
        self.plant_panel_temperature   = extractor.panel_temperature.filter(pl.col("id")==id)
        self.plant_ambient_temperature = extractor.ambient_temperature.filter(pl.col("id")==id)
        self.plant_prmte               = extractor.prmte.filter(pl.col("id")==id)
        self.plant_projected           = extractor.projected.filter(pl.col("id")==id)
        self.plant_recloser            = extractor.recloser.filter(pl.col("Parque")==self.rcc_name)
        self.plant_inverter            = extractor.inverter.filter(pl.col("Parque")==self.rcc_name)
        self.plant_limitations         = extractor.limitations.filter(pl.col("Parque")==self.rcc_name)
        self.plant_restrictions        = extractor.restrictions.filter(pl.col("Parque")==self.rcc_name)
        self.path                      = os.getenv("DYR_REPORTS_PATH")

    def _get_om_name(self) -> str:
        return self.plant_info["om_name"].item()

    def _get_rcc_name(self) -> str:
        return self.plant_info["rcc_name"].item()

    def _get_portfolio(self) -> str:
        return self.plant_info["portfolio_name"].item()