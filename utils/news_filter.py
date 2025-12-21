import re
from utils.filters import COUNTRIES, CAPITALS, INTERNATIONAL_REGIONS, INTERNATIONAL_ORGS, INTERNATIONAL_ADJECTIVES, extras


import unicodedata

def build_international_pattern():
    all_locations = (
        COUNTRIES
        + CAPITALS
        + INTERNATIONAL_REGIONS
        + INTERNATIONAL_ORGS
        + INTERNATIONAL_ADJECTIVES
        + extras
    )

    suffixes = r"(য়|ে|ি|ী|তে|র|এর|কে|দের|সহ|ভিত্তিক)?"

    patterns = [
        re.escape(loc) + suffixes
        for loc in all_locations
    ]

    return re.compile(
        r'(?<!\S)(' + '|'.join(patterns) + r')(?!\S)',
        flags=re.UNICODE
    )

INTL_PATTERN = build_international_pattern()


def filter_international_news(text: str) -> bool:
    text = unicodedata.normalize("NFKC", text)
    return bool(INTL_PATTERN.search(text))


