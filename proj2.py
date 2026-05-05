import csv
import math
from dataclasses import dataclass
from typing import *

import sys
sys.setrecursionlimit(10_000)

@dataclass(frozen=True)
class Row:
    country: str
    year: int | None
    electricity_and_heat_co2_emissions: float | None
    electricity_and_heat_co2_emissions_per_capita: float | None
    energy_co2_emissions: float | None
    energy_co2_emissions_per_capita: float | None
    total_co2_emissions_excluding_lucf: float | None
    total_co2_emissions_excluding_lucf_per_capita: float | None

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None
    

def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, newline = "") as csvfile:
        reader = csv.reader(csvfile)

        header = next(reader)
        if header != columns:
            raise ValueError("Invalid Header")
        
        rows = list(reader)
    
    return build(rows, 0)

def build(rows: list[list[str]], index: int = 0) -> Optional[Node]:
    if index >= len(rows):
        return None
    row = parse_row(rows[index])
    return Node(row, build(rows, index + 1))

def parse_row(fields:list[str]) -> Row:
    return Row(
        country=fields[0],
        year=int(fields[1]) if fields[1] else None,
        electricity_and_heat_co2_emissions=float(fields[2]) if fields[2] else None,
        electricity_and_heat_co2_emissions_per_capita=float(fields[3]) if fields[3] else None,
        energy_co2_emissions=float(fields[4]) if fields[4] else None,
        energy_co2_emissions_per_capita=float(fields[5]) if fields[5] else None,
        total_co2_emissions_excluding_lucf=float(fields[6]) if fields[6] else None,
        total_co2_emissions_excluding_lucf_per_capita=float(fields[7]) if fields[7] else None
    )

def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0
    else:
        return 1 + listlen(data.next)
    

columns = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]

numbers = set(columns) - {"country"}

def filter_rows(data:Optional[Node], 
                field_name:str,
                comparison: str,
                value: Union[str,float,int]
                ) -> Optional[Node]:
    
    if data is None:
        return None
    if field_name not in columns:
        raise ValueError("Invalid Field Name")
    if comparison not in ["less_than", "greater_than", "equal"]:
        raise ValueError("Invalid Comparison")
    if field_name == "country" and comparison != "equal":
        raise ValueError("Invalid Comparison for country")

    filtered_next = filter_rows(data.next, field_name, comparison, value)
    
    field_value = getattr(data.value, field_name)
    correct = False

    if field_value is None:
        return filtered_next
    
    if field_name in numbers:
        field_value = float(field_value)
        value = float(value)

    if comparison == "equal":
        if field_value == value:
            correct = True

    elif comparison == "less_than":
        if field_value < value:
            correct = True

    else:
        if field_value > value:
            correct = True

    if correct:
        return Node(data.value, filtered_next)
    
    return filtered_next