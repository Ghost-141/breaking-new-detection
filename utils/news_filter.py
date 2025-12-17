import re
from utils.filters import COUNTRIES, CAPITALS, INTERNATIONAL_REGIONS, INTERNATIONAL_ORGS, INTERNATIONAL_ADJECTIVES, extras

def filter_international_news(text: str) -> bool:
    """
    Detect international news using regex with Bengali suffixes
    
    Args:
        text (str): News title/text
        
    Returns:
        bool: True if international news detected
    """
    # Combine all location words
    all_locations = COUNTRIES + CAPITALS + INTERNATIONAL_REGIONS + INTERNATIONAL_ORGS + INTERNATIONAL_ADJECTIVES + extras
    
    # Common Bengali suffixes for locations
    suffixes = r"(য়|ে|তে|র|এর|কে|দের|সহ|ভিত্তিক)?"
    
    # Create regex pattern for each location with optional suffixes
    patterns = []
    for location in all_locations:
        # Escape special regex characters and add suffix pattern
        escaped_location = re.escape(location)
        pattern = escaped_location + suffixes
        patterns.append(pattern)
    
    # Combine all patterns with word boundaries
    full_pattern = r'\b(' + '|'.join(patterns) + r')\b'
    
    # Search for matches
    return bool(re.search(full_pattern, text))