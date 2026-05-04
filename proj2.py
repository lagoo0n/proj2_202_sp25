import csv
import math
from dataclasses import dataclass
from typing import *

import sys
sys.setrecursionlimit(10_000)

@dataclass(frozen=True)
class Row:
    data: str

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None

def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        head: Node | None = None
        for fields in reader:
            row = parse_row(fields)
            head = Node(row, head)
        return head

def parse_row(fields:list[str]) -> Row:
    return Row(float(fields[0]))

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

