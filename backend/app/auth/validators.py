import re

def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """Very lenient for development"""
    if not password or len(password) < 6:
        return False
    return True
