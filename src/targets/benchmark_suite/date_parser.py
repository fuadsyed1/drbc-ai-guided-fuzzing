from datetime import datetime


SUPPORTED_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%m/%d/%Y",
]


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Date cannot be empty")

    for date_format in SUPPORTED_FORMATS:
        try:
            parsed_date = datetime.strptime(input_string, date_format)
            return {
                "valid": True,
                "year": parsed_date.year,
                "month": parsed_date.month,
                "day": parsed_date.day,
                "format": date_format,
            }
        except ValueError:
            continue

    raise ValueError("Invalid date format or invalid date value")