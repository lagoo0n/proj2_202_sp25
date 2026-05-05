import unittest
from typing import Optional, Union
from proj2 import (
    Row,
    Node,
    read_csv_lines,
    listlen,
    filter_rows,
    parse_row
)

class TestStructureBasics(unittest.TestCase):

    def test_read_csv_lines(self):
        data = read_csv_lines("sample.csv")
        self.assertIsInstance(data, Node)

    def test_parse_row(self):
        row = parse_row([
            "Africa", "1990", "241.97", "0.37916967", "594.79", "0.9320425", "617.56", "0.96772337"
        ])
        self.assertEqual(row, Row("Africa", 1990, 241.97, 0.37916967, 594.79, 0.9320425, 617.56, 0.96772337))

    def test_listlen(self):
        data = read_csv_lines("sample.csv")
        length = listlen(data)
        self.assertEqual(length, 10)

    def test_filter_rows(self):
        data = read_csv_lines("sample.csv")
        filtered = filter_rows(data, "country", "equal", "Africa")
        self.assertEqual(filtered.value.country, "Africa")

if __name__ == "__main__":
    unittest.main()

