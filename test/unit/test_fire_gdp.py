import os
import sys
import unittest
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import fire_gdp  # noqa: E402

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

    def test_empty_cell_is_empty_string(self):
        rows = fire_gdp.get_data(EMISSIONS, "Area", "Algeria")
        self.assertEqual(rows[1][3], "")  # Algeria 1991 Forest fires


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        header = ["Area", "Year", "Forest fires"]
        self.assertEqual(fire_gdp.get_column_index(header, "Year"), 1)

    def test_name_absent(self):
        self.assertIsNone(fire_gdp.get_column_index(["a", "b"], "z"))

    def test_empty_header(self):
        self.assertIsNone(fire_gdp.get_column_index([], "a"))

    def test_year_is_a_string(self):
        header = ["Country", "1990", "1991"]
        self.assertEqual(fire_gdp.get_column_index(header, "1991"), 2)


class TestGetFireGdpYearData(unittest.TestCase):

    def test_complete_country(self):
        result = fire_gdp.get_fire_gdp_year_data(EMISSIONS, GDP, "Albania")
        self.assertEqual(result, [[1990, 12.5, 1000.0],
                                  [1991, 10.0, 1100.0],
                                  [1992, 8.0, 1250.0]])
        self.assertIsInstance(result[0][2], float)

    def test_skips_empty_values(self):
        # Algeria 1991 has no forest fire value and no GDP value
        result = fire_gdp.get_fire_gdp_year_data(EMISSIONS, GDP, "Algeria")
        self.assertEqual(result, [[1990, 3.1, 5000.0], [1992, 2.9, 5600.0]])

    def test_skips_year_not_in_gdp_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            co2 = os.path.join(tmp, "co2.csv")
            gdp = os.path.join(tmp, "gdp.csv")
            with open(co2, "w") as f:
                f.write("Area,Year,Forest fires\nX,1990,1.5\nX,1800,9.9\n")
            with open(gdp, "w") as f:
                f.write("Country,1990,1991\nX,100,200\n")
            result = fire_gdp.get_fire_gdp_year_data(co2, gdp, "X")
        self.assertEqual(result, [[1990, 1.5, 100.0]])

    def test_country_missing_from_a_file(self):
        # Cuba is only in the CO2 file, Kosovo only in the GDP file
        self.assertEqual(
            fire_gdp.get_fire_gdp_year_data(EMISSIONS, GDP, "Cuba"), [])
        self.assertEqual(
            fire_gdp.get_fire_gdp_year_data(EMISSIONS, GDP, "Kosovo"), [])


if __name__ == '__main__':
    unittest.main()
