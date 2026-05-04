import csv
import math
from dataclasses import dataclass
from typing import *

import sys
sys.setrecursionlimit(10_000)

@dataclass(frozen=True)
class Row:
    data: float

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None

def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0
    else:
        return 1 + listlen(data.next)
    
def filter_rows(data:Optional[Node], 
                field_name:str,
                comparison: str)