import csv
from io import StringIO


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("CSV input cannot be empty")

    try:
        reader = csv.reader(StringIO(input_string))
        rows = list(reader)
    except csv.Error as error:
        raise ValueError(f"Invalid CSV format: {error}")

    if not rows:
        raise ValueError("CSV contains no rows")

    for row in rows:
        if len(row) < 2:
            raise ValueError("CSV row must contain at least two columns")

        if any(cell.strip() == "" for cell in row):
            raise ValueError("CSV contains empty cell")

    return {
        "valid": True,
        "rows": len(rows),
        "columns_first_row": len(rows[0]),
    }