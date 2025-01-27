def parse_month_year(mm_yyyy):
    """
    Given "02-2023" => (2, 2023).
    If month is invalid (<1 or >12), return (0, 0).
    """
    try:
        parts = mm_yyyy.split('-')
        month = int(parts[1])
        year = int(parts[0])

        if month < 1 or month > 12:
            return (0, 0)
        return (month, year)
    except (IndexError, ValueError):
        return (0, 0)


def parse_full_date(dd_mm_yyyy):
    """
    Given "03-11-2023" => (3, 11, 2023).
    If day, month, or year is invalid, return (0, 0, 0).
    For simplicity:
      - month must be 1..12
      - day must be 1..31
    """
    try:
        y, m, d = dd_mm_yyyy.split('-')
        day = int(d)
        month = int(m)
        year = int(y)

        # Minimal checks
        if month < 1 or month > 12:
            return (0, 0, 0)
        if day < 1 or day > 31:
            return (0, 0, 0)

        return (day, month, year)
    except:
        return (0, 0, 0)


def generate_month_range(start_month, start_year, end_month, end_year):
    """
    Creates a list of (month, year) pairs from (start_month, start_year)
    up to (end_month, end_year) inclusive.
    """
    months = []
    current_m = start_month
    current_y = start_year

    while (current_y < end_year) or (current_y == end_year and current_m <= end_month):
        months.append((current_m, current_y))
        current_m += 1
        if current_m == 13:
            current_m = 1
            current_y += 1
    
    return months