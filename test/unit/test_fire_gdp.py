import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import fire_gdp

DATA = os.path.join(HERE, "..", "data")
EMISSIONS = os.path.join(DATA, "Agrofood_co2_emission.csv")
GDP = os.path.join(DATA, "IMF_GDP.csv")


class TestGetData(unittest.TestCase):
    def test_all_rows_no_header(self):
        rows = fire_gdp.get_data(EMISSIONS)
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[0][:2], ["Albania", "1990"])

    def test_return_header(self):
        rows, header = fire_gdp.get_data(EMISSIONS, return_header=True)
        self.assertEqual(header[:2], ["Area", "Year"])
        self.assertEqual(len(rows), 12)

    def test_query_match(self):
        rows = fire_gdp.get_data(EMISSIONS, "Area", "Albania")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][0], "Albania")


if __name__ == '__main__':
    unittest.main()