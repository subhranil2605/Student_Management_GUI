"""General utility helper functions."""

from datetime import datetime, date
from typing import Optional, List, Tuple


def format_date(date_obj: date, format_string: str = "%d/%m/%Y") -> str:
    """
    Format date object to string.

    Args:
        date_obj: Date object to format
        format_string: Format string (default: DD/MM/YYYY)

    Returns:
        Formatted date string
    """
    if not isinstance(date_obj, date):
        raise ValueError("Input must be a date object")
    return date_obj.strftime(format_string)


def parse_date(date_string: str, format_string: str = "%d/%m/%Y") -> date:
    """
    Parse date string to date object.

    Args:
        date_string: Date string to parse
        format_string: Format string (default: DD/MM/YYYY)

    Returns:
        Parsed date object

    Raises:
        ValueError: If date string doesn't match format
    """
    try:
        return datetime.strptime(date_string, format_string).date()
    except ValueError as e:
        raise ValueError(f"Failed to parse date: {str(e)}")


def get_age(birth_date: date) -> int:
    """
    Calculate age from birth date.

    Args:
        birth_date: Birth date as date object

    Returns:
        Age in years
    """
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def format_currency(amount: float, currency_symbol: str = "₹") -> str:
    """
    Format amount as currency string.

    Args:
        amount: Amount to format
        currency_symbol: Currency symbol (default: ₹)

    Returns:
        Formatted currency string
    """
    return f"{currency_symbol}{amount:,.2f}"


def parse_currency(currency_string: str, currency_symbol: str = "₹") -> float:
    """
    Parse currency string to float.

    Args:
        currency_string: Currency string to parse
        currency_symbol: Currency symbol to remove

    Returns:
        Parsed amount as float

    Raises:
        ValueError: If currency string is invalid
    """
    try:
        # Remove currency symbol and whitespace
        clean_string = currency_string.replace(currency_symbol, "").replace(",", "").strip()
        return float(clean_string)
    except ValueError as e:
        raise ValueError(f"Failed to parse currency: {str(e)}")


def calculate_cgpa(
    gpa_list: List[float], credit_hours: Optional[List[int]] = None
) -> float:
    """
    Calculate CGPA from GPA list.

    Args:
        gpa_list: List of GPA values
        credit_hours: Optional list of credit hours for weighted CGPA

    Returns:
        Calculated CGPA (0-4.0)

    Raises:
        ValueError: If inputs are invalid
    """
    if not gpa_list:
        raise ValueError("GPA list cannot be empty")

    # Remove None values
    valid_gpas = [gpa for gpa in gpa_list if gpa is not None]
    if not valid_gpas:
        raise ValueError("No valid GPA values provided")

    if credit_hours is None:
        # Simple average
        return round(sum(valid_gpas) / len(valid_gpas), 2)

    # Weighted average
    if len(valid_gpas) != len(credit_hours):
        raise ValueError("GPA list and credit_hours list must have same length")

    total_credits = sum(credit_hours)
    if total_credits == 0:
        raise ValueError("Total credit hours cannot be zero")

    weighted_sum = sum(gpa * credits for gpa, credits in zip(valid_gpas, credit_hours))
    return round(weighted_sum / total_credits, 2)


def percentage_to_gpa(percentage: float, scale: float = 4.0) -> float:
    """
    Convert percentage to GPA.

    Args:
        percentage: Percentage value (0-100)
        scale: GPA scale (default: 4.0)

    Returns:
        Converted GPA value

    Raises:
        ValueError: If percentage is invalid
    """
    if not (0 <= percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100")

    return round((percentage / 100) * scale, 2)


def gpa_to_percentage(gpa: float, scale: float = 4.0) -> float:
    """
    Convert GPA to percentage.

    Args:
        gpa: GPA value
        scale: GPA scale (default: 4.0)

    Returns:
        Converted percentage value

    Raises:
        ValueError: If GPA is invalid
    """
    if not (0 <= gpa <= scale):
        raise ValueError(f"GPA must be between 0 and {scale}")

    return round((gpa / scale) * 100, 2)


def assign_grade(percentage: float) -> str:
    """
    Assign letter grade based on percentage.

    Args:
        percentage: Percentage value (0-100)

    Returns:
        Letter grade (A, B, C, D, E, F)

    Raises:
        ValueError: If percentage is invalid
    """
    if not (0 <= percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100")

    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    elif percentage >= 50:
        return "E"
    else:
        return "F"


def get_grade_description(grade: str) -> str:
    """
    Get description for letter grade.

    Args:
        grade: Letter grade (A-F)

    Returns:
        Grade description

    Raises:
        ValueError: If grade is invalid
    """
    grade_descriptions = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Satisfactory",
        "E": "Pass",
        "F": "Fail",
    }

    if grade.upper() not in grade_descriptions:
        raise ValueError(f"Invalid grade: {grade}")

    return grade_descriptions[grade.upper()]


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def capitalize_name(name: str) -> str:
    """
    Capitalize name properly (handles hyphenated names).

    Args:
        name: Name to capitalize

    Returns:
        Properly capitalized name
    """
    if not name:
        return ""

    # Handle hyphenated names
    parts = name.split("-")
    return "-".join(part.capitalize() for part in parts)


def format_phone(phone: str) -> str:
    """
    Format phone number to standard format.

    Args:
        phone: Phone number string

    Returns:
        Formatted phone number

    Raises:
        ValueError: If phone number is invalid
    """
    # Remove non-digits
    digits = "".join(c for c in phone if c.isdigit())

    if len(digits) != 10:
        raise ValueError("Phone number must have 10 digits")

    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"


def get_initials(full_name: str) -> str:
    """
    Get initials from full name.

    Args:
        full_name: Full name string

    Returns:
        Initials string
    """
    if not full_name:
        return ""

    parts = full_name.strip().split()
    return "".join(part[0].upper() for part in parts if part)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide with default value on error.

    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if denominator is zero

    Returns:
        Division result or default
    """
    if denominator == 0:
        return default
    return numerator / denominator


def format_decimal(value: float, decimal_places: int = 2) -> str:
    """
    Format decimal number with specified places.

    Args:
        value: Numeric value
        decimal_places: Number of decimal places

    Returns:
        Formatted string
    """
    return f"{value:.{decimal_places}f}"
