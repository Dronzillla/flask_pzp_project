from dataclasses import dataclass
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string
from collections import namedtuple
from datetime import datetime
from collections import Counter

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
Benefit = namedtuple("Benefit", ["category", "values"])
Harm = namedtuple("Harm", ["category", "values"])


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
        # result: list[dict] = []
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
        # print(result)
        # print(result_dict)
        return result_dict

    def get_multiple_budget_line_values(self, type: str, lines: int) -> dict:
        list_budget_lines: list[dict] = []
        # Revenue is recorded on 5 lines
        for i in range(lines):
            budget_line = self.get_budget_line_values(type, index=i)
            list_budget_lines.append(budget_line)
        result = self.sum_budget_lines_values(list_budget_lines)
        print(result)
        return result

    def get_sector_name(self, index) -> str:
        sector_cell = f"B{index + 1}"
        sector_name = self.sheet_data1[sector_cell].value
        return sector_name

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
        start_date = self.get_start_date()
        reference_period = self.get_reference_period()
        analysis_method = self.get_analysis_method()
        analysis_principle = self.sheet_rezultatai["B3"].value
        main_sector = self.get_main_sector()
        no_alterantives = self.get_no_alterantives()
        da_analysis = self.get_is_da_analysis_selected()
        version = self.sheet_pradzia["C45"].value
        result = General(
            start_date=start_date,
            reference_period=reference_period,
            analysis_method=analysis_method,
            analysis_principle=analysis_principle,
            main_sector=main_sector,
            no_alternatives=no_alterantives,
            da_analysis=da_analysis,
            version=version,
        )
        print(result)
        return result

    def fetch_ratios(self) -> Ratios:
        if self.get_analysis_method() == "Sąnaudų ir naudos analizė":
            sva = None
            enis = round(self.sheet_scenariju_analize["G271"].value, 2)
            egdv = round(self.sheet_scenariju_analize["G272"].value, 0)
            evgn = round(self.sheet_scenariju_analize["G273"].value, 4)
        else:
            sva = round(self.sheet_scenariju_analize["G274"].value, 2)
            enis = None
            egdv = None
            evgn = None

        if self.get_is_da_analysis_selected():
            da = round(self.sheet_scenariju_analize["G275"].value, 2)
        else:
            da = None
        fgdv = round(self.sheet_scenariju_analize["G277"].value, 0)
        fvgn = round(self.sheet_scenariju_analize["G278"].value, 4)
        fnis = round(self.sheet_scenariju_analize["G279"].value, 2)
        result = Ratios(
            enis=enis,
            egdv=egdv,
            evgn=evgn,
            sva=sva,
            da=da,
            fgdv=fgdv,
            fvgn=fvgn,
            fnis=fnis,
        )
        print(result)
        return result

    def fetch_capex(self) -> dict:
        result = self.get_budget_line_values("capex")
        return result

    def fetch_reinvestment(self) -> dict:
        result = self.get_budget_line_values("reinvestment")
        return result

    def fetch_opex(self) -> dict:
        # Public opex
        # Opex is recorded on 5 lines
        result = self.get_multiple_budget_line_values(type="opex", lines=5)
        return result

    def fetch_revenue(self) -> dict:
        result = self.get_budget_line_values("revenue")
        return result

    def fetch_tax_revenue(self) -> dict:
        result = self.get_budget_line_values("tax_revenue")
        return result

    def fetch_vat(self) -> dict:
        result = self.get_budget_line_values("vat")
        return result

    def fetch_private_cost(self) -> dict:
        # Private capex and opex 95:99
        # Cost is recorded on 5 lines
        result = self.get_multiple_budget_line_values(type="private_cf_cost", lines=5)
        return result

    def fetch_private_revenue(self) -> dict:
        # Private revenue 106:110
        # Revenue is recorded on 5 lines
        result = self.get_multiple_budget_line_values(
            type="private_cf_revenue", lines=5
        )
        return result

    def fetch_benefits(self) -> list[Benefit]:
        result = []
        # Maximum amount of benefit categories are 7
        for i in range(7):
            benefit_category = self.sheet_alternatyva[f"C{119+i}"].value
            benefit_category_total_values = self.sheet_alternatyva[f"G{119+i}"].value
            # Check if benefit or total values for benefit is blank
            if benefit_category == None or benefit_category_total_values == 0:
                continue
            values = self.get_budget_line_values("benefit", index=i)
            benefit = Benefit(category=benefit_category, values=values)
            result.append(benefit)
        print(result)
        return result

    def fetch_harms(self) -> list[Harm]:
        result = []
        # Maximum amount of harm categories are 3
        for i in range(3):
            harm_category = self.sheet_alternatyva[f"C{127+i}"].value
            harm_category_total_values = self.sheet_alternatyva[f"G{127+i}"].value
            # Check if harm or total values for harm is blank
            if harm_category == None or harm_category_total_values == 0:
                continue
            values = self.get_budget_line_values("harm", index=i)
            harm = Harm(category=harm_category, values=values)
            result.append(harm)
        print(result)
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
        print(economic_sectors)
        return economic_sectors
