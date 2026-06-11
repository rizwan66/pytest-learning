import re

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def is_valid_password(password: str) -> bool:
    """Password must be 8+ chars, with at least one digit and one uppercase."""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def is_valid_age(age) -> bool:
    try:
        age = int(age)
        return 0 <= age <= 150
    except (ValueError, TypeError):
        return False

def classify_temperature(celsius: float) -> str:
    if celsius < 0:
        return "freezing"
    elif celsius < 10:
        return "cold"
    elif celsius < 20:
        return "cool"
    elif celsius < 30:
        return "warm"
    else:
        return "hot"
