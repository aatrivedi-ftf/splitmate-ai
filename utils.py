import re

TRAILING_KEYWORDS = {"unevenly", "evenly", "equally", "randomly", "fairly"}

def clean_name(name: str) -> str:
    name = name.strip()
    for word in TRAILING_KEYWORDS:
        pattern = rf'\b{word}\b[.,;:]?$'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE).strip()
    return name
