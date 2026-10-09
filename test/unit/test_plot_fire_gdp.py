import os
import sys
import tempfile
import unittest

import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import plot_fire_gdp  # noqa: E402

DATA = os.path.join(HERE, "..", "data")
EMISSIONS = os.path.join(DATA, "Agrofood_co2_emission.csv")
GDP = os.path.join(DATA, "IMF_GDP.csv")

# [year, forest_fires, gdp] entries, as returned by get_fire_gdp_year_data
DATA_ROWS = [[1990, 1.0, 10.0], [1991, 2.0, 20.0]]


class TestPlotCountry(unittest.TestCase):

    def setUp(self):
        self.fig, self.ax = plt.subplots()

    def tearDown(self):
        plt.close(self.fig)

    def test_title_is_country(self):
        plot_fire_gdp.plot_country(self.ax, "Brazil", DATA_ROWS)
        self.assertEqual(self.ax.get_title(), "Brazil")

    def test_points_are_gdp_vs_fires(self):
        plot_fire_gdp.plot_country(self.ax, "Brazil", DATA_ROWS)
        points = self.ax.collections[0].get_offsets().tolist()
        self.assertEqual(points, [[10.0, 1.0], [20.0, 2.0]])

    def test_labels_and_spines(self):
        plot_fire_gdp.plot_country(self.ax, "Brazil", DATA_ROWS)
        self.assertIn("GDP", self.ax.get_xlabel())
        self.assertIn("Forest fire", self.ax.get_ylabel())
        self.assertFalse(self.ax.spines["top"].get_visible())
        self.assertFalse(self.ax.spines["right"].get_visible())

    def test_no_data_draws_no_points(self):
        plot_fire_gdp.plot_country(self.ax, "Cuba", [])
        self.assertEqual(len(self.ax.collections), 0)
        self.assertEqual(self.ax.get_title(), "Cuba")


class TestMakePlot(unittest.TestCase):

    def test_creates_image_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "plot.png")
            plot_fire_gdp.make_plot(EMISSIONS, GDP, ["Albania", "Cuba"], out)
            self.assertTrue(os.path.getsize(out) > 0)


if __name__ == '__main__':
    unittest.main()