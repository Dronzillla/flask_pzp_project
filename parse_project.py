from dataclasses import dataclass
from openpyxl import Workbook
from collections import namedtuple


Ratios = namedtuple(
    "Ratios", ["enis", "egdv", "evgn", "sva", "da", "fgdv", "fvgn", "fnis"]
)
Project = namedtuple("Project", ["code", "name"])
General = namedtuple(
    "General",
    [
        "start_date",
        "reference_period",
        "analysis_method",
        "analysis_principle",
        "main_sector",
        "no_alternatives",
        "da_analysis",
        "version",
    ],
)


@dataclass
class ProjectParser:
    workbook: Workbook

    def __post_init__(self):
        self.sheet_pradzia = self.workbook["Pradžia"]
        self.sheet_rezultatai = self.workbook["Rezultatai"]
        # Check if optimal alternative was selected.
        opt_alterantive = self.get_opt_alternative_name()
        if opt_alterantive is not None:
            self.sheet_alternatyva = self.workbook[self.get_opt_alternative_name()]
        self.sheet_scenariju_analize = self.workbook["Scenarijų analizė"]
        self.sheet_data1 = self.workbook["Data1"]

    def get_opt_alternative_name(self) -> str:
        optimal_alternative = self.sheet_rezultatai["F6"].value
        return optimal_alternative

    """
    MAIN functions do fetch data for database operations
    """

    def fetch_project_info(self) -> Project:
        code = self.sheet_pradzia["E4"].value
        name = self.sheet_pradzia["E6"].value
        result = Project(code=code, name=name)
        print(result)
        return result

    def fetch_general_info(self) -> General:
        pass

    def fetch_ratios(self) -> Ratios:
        pass
