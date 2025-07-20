# Configuration Hub for FDA Food Safety Monitor
# This file holds all the important variables that control the script's behavior


# Search Parameters - Date Range
SEARCH_START_DATE = "2025-01-01"
SEARCH_END_DATE = "2025-12-31"

# Legacy configuration (kept for backward compatibility)
TARGETS = {
    'UK': {
        'authority': 'BBC Health',
        'rss_feed_url': 'http://feeds.bbci.co.uk/news/health/rss.xml'
    }
}

PHARMA_KEYWORDS = [
    'buprenorphine',
    'naloxone',
    'risperidone',
    'nalmefene',
    'sublocade',
    'suboxone',
    'subutex',
    'perseris',
    'opvee',
    'mhra', # UK Regulatory Agency
    'fda'   # US Regulatory Agency
] 