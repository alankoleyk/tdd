import csv


def get_data(file_name, query_column=None, query_value=None,
             return_header=False):
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
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    co2_rows, co2_header = get_data(co2_file, "Area", country,
                                    return_header=True)
    gdp_rows, gdp_header = get_data(gdp_file, "Country", country,
                                    return_header=True)
    gdp_row = gdp_rows[0]
    fire_index = get_column_index(co2_header, "Forest fires")

    result = []
    for row in co2_rows:
        gdp_index = get_column_index(gdp_header, row[1])
        result.append([int(row[1]), float(row[fire_index]),
                       float(gdp_row[gdp_index])])
    return result