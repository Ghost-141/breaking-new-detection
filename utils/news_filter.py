import re
from utils.filters import COUNTRIES, CAPITALS, INTERNATIONAL_REGIONS, INTERNATIONAL_ORGS, INTERNATIONAL_ADJECTIVES

country_set = set(COUNTRIES)
capital_set = set(CAPITALS)
int_region = set(INTERNATIONAL_REGIONS)
int_org = set(INTERNATIONAL_ORGS)
int_adj = set(INTERNATIONAL_ADJECTIVES)

all_locations = country_set | capital_set | int_region | int_org | int_adj
pattern = re.compile("|".join(map(re.escape, all_locations)))

def filter_international_news(text: str) -> bool:
    return bool(pattern.search(text))