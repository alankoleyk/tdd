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
    pass