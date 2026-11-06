import csv
import argparse
import os


def get_data(file_name, query_column=None, query_value=None,
             return_header=False):
    """Return data rows, optionally only those matching a column value."""
    with open(file_name, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    if query_column is not None:
        index = header.index(query_column)
        rows = [row for row in rows if row[index] == query_value]
    if return_header:
        return rows, header
    return rows


def get_column_index(header, column_name):
    """Return the position of column_name in header, or None if absent."""
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    """Return [year, forest_fires, gdp] for each year with both values."""
    co2_rows, co2_header = get_data(co2_file, "Area", country,
                                    return_header=True)
    gdp_rows, gdp_header = get_data(gdp_file, "Country", country,
                                    return_header=True)
    if not co2_rows or not gdp_rows:
        return []

    gdp_row = gdp_rows[0]
    fire_index = get_column_index(co2_header, "Forest fires")

    result = []
    for row in co2_rows:
        gdp_index = get_column_index(gdp_header, row[1])
        if gdp_index is None:
            continue
        if row[fire_index] == "" or gdp_row[gdp_index] == "":
            continue
        result.append([int(row[1]), float(row[fire_index]),
                       float(gdp_row[gdp_index])])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--co2_file", required=True)
    parser.add_argument("--gdp_file", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--out_file", required=True)
    args = parser.parse_args()

    data = get_fire_gdp_year_data(args.co2_file, args.gdp_file, args.country)
    if not data:
        raise SystemExit(f"No data found for {args.country}")

    out_dir = os.path.dirname(args.out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out_file, "w") as f:
        for year, fires, gdp in data:
            f.write(f"{year}\t{fires}\t{gdp}\n")


if __name__ == "__main__":
    main()
