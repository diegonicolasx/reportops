import polars as pl
from src.utils.utils import events_filter, filter_year_month

class ReportETL :


    def __init__(self,
                 poa         : pl.DataFrame,
                 panel_temp  : pl.DataFrame,
                 amb_temp    : pl.DataFrame,
                 prmte       : pl.DataFrame,
                 projected   : pl.DataFrame,
                 reco        : pl.DataFrame,
                 equipment   : pl.DataFrame,
                 curtailment : pl.DataFrame,
                 year: int,
                 month: int
                 ):
        
        self.poa_irradiation      = filter_year_month(poa, year, month)
        self.panel_temperature    = filter_year_month(panel_temp, year, month)
        self.ambient_temperature  = filter_year_month(amb_temp, year, month)
        self.prmte_generation     = filter_year_month(prmte, year, month)
        self.projected_generation = filter_year_month(projected, year, month)
        self.reconectador         = events_filter(reco, year, month)
        self.equipment            = events_filter(equipment, year, month)
        self.curtailment          = events_filter(curtailment, year, month)