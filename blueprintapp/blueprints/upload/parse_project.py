from dataclasses import dataclass
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string
from collections import namedtuple
from datetime import datetime
from collections import Counter
from typing import Union


Benefit_tuple = namedtuple("Benefit_tuple", ["name", "values"])
Cashflow_tuple = namedtuple("Cashflow_tuple", ["category", "values"])
General_tuple = namedtuple(
    "General_tuple",
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
Harm_tuple = namedtuple("Harm_tuple", ["name", "values"])
Project_tuple = namedtuple("Project_tuple", ["code", "name"])
Ratios_tuple = namedtuple(
    "Ratios_tuple", ["enis", "egdv", "evgn", "sva", "da", "fgdv", "fvgn", "fnis"]
)


class MyNumbers:
    def __init__(self, start=1):
        self.start = start
        self.a = start

    def __iter__(self):
        self.a = self.start
        return self

    def __next__(self):
        b = self.a
        self.a += 1
        return b


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
    Get data for function fetch_general_info
    """

    def get_start_date(self) -> datetime:
        start_date = self.sheet_pradzia["E10"].value
        return start_date

    def get_reference_period(self) -> int:
        reference_period = self.sheet_pradzia["E12"].value
        return reference_period

    def get_start_year(self) -> int:
        return self.get_start_date().year

    def get_analysis_method(self) -> str:
        return self.sheet_rezultatai["B4"].value

    def get_main_sector(self) -> str:
        main_sector_index = self.sheet_data1["H2"].value
        main_sector_cell = f"B{main_sector_index + 1}"
        main_sector = self.sheet_data1[main_sector_cell].value
        return main_sector

    def get_no_alterantives(self) -> int:
        non_empty_cell_count = 0
        for cell in self.sheet_data1["I"]:
            if cell.value is not None:
                non_empty_cell_count += 1
        # Minus one for name row
        return non_empty_cell_count - 1

    def get_is_da_analysis_selected(self) -> bool:
        if self.sheet_rezultatai["B5"].value == None:
            return False
        return True

    """
    Get data for fetching cash flows

    """

    def sum_budget_lines_values(self, data: list[dict]) -> dict:
        result = Counter()
        # Iterate over the list of dictionaries and update the Counter
        for d in data:
            result.update(d)
        # Convert back to a regular dictionary if needed
        result = dict(result)
        return result

    def get_budget_line_values(self, type: str, index: int = None) -> list[dict]:
        result_dict: dict = {}
        # Get reference period and start year of a project
        period = self.get_reference_period()
        start_year = self.get_start_year()
        # Make an iterator
        myclass = MyNumbers(start=start_year)
        myiter = iter(myclass)
        # Define data row based on budget line type
        if type == "capex":
            row = 9
        elif type == "reinvestment":
            row = 8
        elif type == "opex":
            row = 90 + index
        elif type == "revenue":
            row = 100
        elif type == "tax_revenue":
            row = 111
        elif type == "vat":
            row = 112
        elif type == "private_cf_cost":
            row = 95 + index
        elif type == "private_cf_revenue":
            row = 106 + index
        elif type == "benefit":
            row = 119 + index
        elif type == "harm":
            row = 127 + index
        # Define the starting column "H" for start year
        start_col_letter = "H"
        start_col_index = column_index_from_string(start_col_letter)
        # Define a relative ending column index (e.g., 10 columns after "H")
        relative_end_index = period
        # Calculate the absolute ending column index
        end_col_index = start_col_index + relative_end_index
        # Iterate over the range
        for col in self.sheet_alternatyva.iter_cols(
            min_row=row, max_row=row, min_col=start_col_index, max_col=end_col_index
        ):
            for cell in col:
                # record = {next(myiter): round(cell.value, 2)}
                # result.append(record)
                result_dict[next(myiter)] = round(cell.value, 2)
        # print(result_dict)
        return result_dict

    def get_multiple_budget_line_values(self, type: str, lines: int) -> dict:
        list_budget_lines: list[dict] = []
        # Iterate over
        for i in range(lines):
            budget_line = self.get_budget_line_values(type=type, index=i)
            list_budget_lines.append(budget_line)
        result = self.sum_budget_lines_values(list_budget_lines)
        # print(result)
        return result

    def get_sector_name(self, index) -> str:
        sector_cell = f"B{index + 1}"
        sector_name = self.sheet_data1[sector_cell].value
        return sector_name

    """
    MAIN functions do fetch data for database operations
    """

    def fetch_project_info(self) -> Project_tuple:
        """Extracts project name and code from uploaded excel file. Project name and code should be unique in database.

        Returns:
            Project_tuple: named tuple with two two attributes 'name' and 'code'.
        """
        code = self.sheet_pradzia["E4"].value
        name = self.sheet_pradzia["E6"].value
        name = name.strip().lower().capitalize()
        result = Project_tuple(code=code, name=name)
        # print(result)
        return result

    def fetch_general_info(self) -> General_tuple:
        start_date = self.get_start_date()
        reference_period = self.get_reference_period()
        analysis_method = self.get_analysis_method()
        analysis_principle = self.sheet_rezultatai["B3"].value
        main_sector = self.get_main_sector()
        no_alterantives = self.get_no_alterantives()
        da_analysis = self.get_is_da_analysis_selected()
        version = self.sheet_pradzia["C45"].value
        result = General_tuple(
            start_date=start_date,
            reference_period=reference_period,
            analysis_method=analysis_method,
            analysis_principle=analysis_principle,
            main_sector=main_sector,
            no_alternatives=no_alterantives,
            da_analysis=da_analysis,
            version=version,
        )
        # print(result)
        return result

    @staticmethod
    def round_ratio(ratio: Union[int, float], ratio_name: str) -> float:
        """Try to round a ratio and map number of digits to round based on ratio name"

        Args:
            ratio (Union[int, float]): ratio value
            ratio_name (str): ratio name in db

        Returns:
            float: ratio rounded to given precision, -9999 if ratio rounding was unsuccessful.
        """
        # Map ratios to ndigits to round
        ratio_ndigits_map = {
            "enis": 2,
            "egdv": 0,
            "evgn": 4,
            "sva": 2,
            "da": 2,
            "fgdv": 0,
            "fvgn": 4,
            "fnis": 2,
        }

        try:
            ratio = round(ratio, ratio_ndigits_map[ratio_name])
            # if ratio_name == "evgn" or ratio == "fvgn":
            #     ratio = round(ratio * 100, ratio_ndigits_map[ratio_name])
            # else:
            #     ratio = round(ratio, ratio_ndigits_map[ratio_name])
        except:
            ratio = -9999
        return ratio

    def fetch_ratios(self) -> Ratios_tuple:
        if self.get_analysis_method() == "Sąnaudų ir naudos analizė":
            sva = None
            enis = ProjectParser.round_ratio(
                ratio=self.sheet_scenariju_analize["G271"].value,
                ratio_name="enis",
            )
            egdv = ProjectParser.round_ratio(
                ratio=self.sheet_scenariju_analize["G272"].value,
                ratio_name="egdv",
            )
            evgn = ProjectParser.round_ratio(
                ratio=self.sheet_scenariju_analize["G273"].value,
                ratio_name="evgn",
            )
        else:
            sva = ProjectParser.round_ratio(
                ratio=self.sheet_scenariju_analize["G274"].value,
                ratio_name="sva",
            )
            enis = None
            egdv = None
            evgn = None
        # If multicriteria analysis is selected
        if self.get_is_da_analysis_selected():
            da = ProjectParser.round_ratio(
                ratio=self.sheet_scenariju_analize["G275"].value,
                ratio_name="da",
            )
        else:
            da = None
        # Financial ratios
        fgdv = ProjectParser.round_ratio(
            ratio=self.sheet_scenariju_analize["G277"].value,
            ratio_name="fgdv",
        )
        fvgn = ProjectParser.round_ratio(
            ratio=self.sheet_scenariju_analize["G278"].value,
            ratio_name="fvgn",
        )
        fnis = ProjectParser.round_ratio(
            ratio=self.sheet_scenariju_analize["G279"].value,
            ratio_name="fnis",
        )
        result = Ratios_tuple(
            enis=enis,
            egdv=egdv,
            evgn=evgn,
            sva=sva,
            da=da,
            fgdv=fgdv,
            fvgn=fvgn,
            fnis=fnis,
        )
        # print(result)
        return result

    def fetch_capex(self) -> Cashflow_tuple:
        cf_name = "capex"
        values = self.get_budget_line_values(cf_name)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_reinvestment(self) -> Cashflow_tuple:
        cf_name = "reinvestment"
        values = self.get_budget_line_values(cf_name)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_opex(self) -> Cashflow_tuple:
        cf_name = "opex"
        # Public opex
        # Opex is recorded on 5 lines
        values = self.get_multiple_budget_line_values(type=cf_name, lines=5)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_revenue(self) -> Cashflow_tuple:
        cf_name = "revenue"
        values = self.get_budget_line_values(cf_name)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_tax_revenue(self) -> Cashflow_tuple:
        cf_name = "tax_revenue"
        values = self.get_budget_line_values(cf_name)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_vat(self) -> Cashflow_tuple:
        cf_name = "vat"
        values = self.get_budget_line_values("vat")
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_private_cost(self) -> Cashflow_tuple:
        # Private capex and opex 95:99
        # Cost is recorded on 5 lines
        cf_name = "private_cf_cost"
        values = self.get_multiple_budget_line_values(type=cf_name, lines=5)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_private_revenue(self) -> Cashflow_tuple:
        # Private revenue 106:110
        # Revenue is recorded on 5 lines
        cf_name = "private_cf_revenue"
        values = self.get_multiple_budget_line_values(type=cf_name, lines=5)
        result = Cashflow_tuple(category=cf_name, values=values)
        return result

    def fetch_cashflows(self) -> list[Cashflow_tuple]:
        result = []
        # Append cashflows
        result.extend(
            [
                self.fetch_capex(),
                self.fetch_reinvestment(),
                self.fetch_opex(),
                self.fetch_revenue(),
                self.fetch_tax_revenue(),
                self.fetch_vat(),
                self.fetch_private_cost(),
                self.fetch_private_revenue(),
            ]
        )
        # For debugging
        # print(result)
        return result

    def fetch_benefits(self) -> list[Benefit_tuple]:
        result = []
        # Maximum amount of benefit categories are 7
        for i in range(7):
            benefit_component = self.sheet_alternatyva[f"C{119+i}"].value
            benefit_component_total_values = self.sheet_alternatyva[f"G{119+i}"].value
            # Check if benefit or total values for benefit is blank
            if benefit_component == None or benefit_component_total_values == 0:
                continue
            values = self.get_budget_line_values("benefit", index=i)
            benefit = Benefit_tuple(name=benefit_component.strip(), values=values)
            result.append(benefit)
        # print(result)
        return result

    def fetch_harms(self) -> list[Harm_tuple]:
        result = []
        # Maximum amount of harm categories are 3
        for i in range(3):
            harm_component = self.sheet_alternatyva[f"C{127+i}"].value
            harm_component_total_values = self.sheet_alternatyva[f"G{127+i}"].value
            # Check if harm or total values for harm is blank
            if harm_component == None or harm_component_total_values == 0:
                continue
            values = self.get_budget_line_values("harm", index=i)
            harm = Harm_tuple(name=harm_component, values=values)
            result.append(harm)
        # print(result)
        return result

    def fetch_economic_sectors(self) -> list[str]:
        # Get all indices referencing to names of sectors
        sector_indices = []
        for cell in self.sheet_data1["H"][1:]:
            if cell.value is None:
                break
            sector_indices.append(cell.value)
        # Get all sector names
        # if len(sector_indices) == 0:
        #     return []
        economic_sectors = [(self.get_sector_name(index)) for index in sector_indices]
        # print(economic_sectors)
        return economic_sectors
