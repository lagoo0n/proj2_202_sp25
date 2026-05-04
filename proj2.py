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
    
    parts = data.value.data.split(",")
    field_index = columns.index(field_name)
    field_value = parts[field_index]

    correct = False

    if field_value == "":
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