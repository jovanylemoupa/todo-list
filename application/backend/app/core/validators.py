"""
Validateurs personnalisés
"""
import re
from datetime import datetime, date
from typing import Any

def validate_hex_color(color: str) -> bool:
    """Valider un code couleur hexadécimal"""
    pattern = r"^#[0-9A-Fa-f]{6}$"
    return bool(re.match(pattern, color))

def validate_future_date(date_value: datetime) -> bool:
    """Valider qu'une date est dans le futur"""
    return date_value.date() > date.today()

def validate_title_length(title: str, min_length: int = 3) -> bool:
    """Valider la longueur minimale d'un titre"""
    return len(title.strip()) >= min_length if title else False

def validate_email(email: str) -> bool:
    """Valider un format d'email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))