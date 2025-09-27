import re
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_not_empty(value: str) -> bool:
    return bool(value and value.strip())


def is_valid_username(username: str) -> bool:
    return len(username) >= 4


def is_valid_password(password: str) -> bool:
    return len(password) >= 6