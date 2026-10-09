
"""Plot forest fire emissions against GDP, one panel per country."""
 
import argparse
import sys
 
import matplotlib.pyplot as plt
 
import fire_gdp
 
DEFAULT_COUNTRIES = [
    "Brazil",
    "Zambia",
    "Australia",
    "Canada",
    "Mexico",
    "United States of America",
]
PANELS_PER_ROW = 3
 
 
def plot_country(ax, country, data):
    """Scatter GDP (x) against forest fire emissions (y) for one country."""
    ax.set_title(country)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if not data:
        ax.text(0.5, 0.5, "no data", ha="center", va="center",
                transform=ax.transAxes)
        return
    gdp = [row[2] for row in data]
    fires = [row[1] for row in data]
    ax.scatter(gdp, fires)
    ax.set_xlabel("GDP (millions, local currency)")
    ax.set_ylabel("Forest fire emissions (kt CO2eq)")
 
 
def make_plot(co2_file, gdp_file, countries, out_file):
    """Save one scatter panel per country to out_file."""
    rows = (len(countries) + PANELS_PER_ROW - 1) // PANELS_PER_ROW
    fig, axes = plt.subplots(rows, PANELS_PER_ROW, squeeze=False,
                             figsize=(5 * PANELS_PER_ROW, 4 * rows))
    axes = axes.flatten()
    for ax, country in zip(axes, countries):
        data = fire_gdp.get_fire_gdp_year_data(co2_file, gdp_file, country)
        plot_country(ax, country, data)
    for ax in axes[len(countries):]:
        ax.set_visible(False)
    fig.tight_layout()
    fig.savefig(out_file, bbox_inches="tight")
    plt.close(fig)
 
 
def parse_args(argv=None):
    """Read the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Plot forest fire emissions against GDP per country.")
    parser.add_argument("--co2_file",
                        default="data/Agrofood_co2_emission.csv")
    parser.add_argument("--gdp_file", default="data/IMF_GDP.csv")
    parser.add_argument("--countries", nargs="+",
                        default=DEFAULT_COUNTRIES)
    parser.add_argument("--out", default="fire_gdp.png")
    return parser.parse_args(argv)
 
 
def main():
    """Make the plot and return an exit code."""
    args = parse_args()
    try:
        make_plot(args.co2_file, args.gdp_file, args.countries, args.out)
    except FileNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
 
 
if __name__ == "__main__":
    sys.exit(main())
