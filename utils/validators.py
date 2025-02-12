import re

def validate_ci(ci: str) -> bool:
    """Valida el formato de la cédula de identidad (V-XXXXXXXX)"""
    pattern = r"^[V|E]-\d{8}$"
    return bool(re.match(pattern, ci))

def validate_section(section: str) -> bool:
    """Valida el formato de la sección (DCM/DCN0[1-4]0[1-4])"""
    pattern = r"^(DCM|DCN)0[1-4]0[1-4]$"
    return bool(re.match(pattern, section))
