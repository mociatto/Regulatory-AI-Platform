# Autonomous Regulatory Change Find and Report AI System

An automated system designed to monitor FDA press announcements and extract key food safety information using AI-powered analysis.

## Overview

The FDA Food Safety Monitor is a comprehensive tool that:
- Scrapes FDA press announcements for food safety-related news
- Uses AI/NLP techniques to extract structured information
- Generates detailed reports in CSV and JSON formats
- Provides summary statistics and insights

## Features

- **Automated Web Scraping**: Monitors FDA press announcements within specified date ranges
- **Content Verification Logging**: Logs raw HTML content from the first article for verification
- **Keyword Filtering**: Identifies relevant articles using configurable keywords
- **AI-Powered Extraction**: Extracts structured information including:
  - Product names
  - Contaminants/recall reasons
  - Affected regions
  - Company names
- **Multiple Output Formats**: Generates both CSV and JSON reports
- **Summary Statistics**: Provides insights on companies, contaminants, and trends
- **Organized Output**: All files automatically saved to `/report` folder

## Project Structure

```
09-Indivior/
├── config.py              # Configuration settings
├── main.py                # Main orchestrator
├── website_scraper.py     # Web scraping module
├── ai_processor.py        # AI processing module
├── requirements.txt       # Dependencies
├── README.md             # This file
└── report/               # Output folder for all generated files
    ├── scraped_articles.json
    ├── final_report_YYYYMMDD_HHMMSS.csv
    └── final_report_YYYYMMDD_HHMMSS.json
```

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python main.py
   ```

## Configuration

Edit `config.py` to customize the monitoring parameters:

```python
# URLs to monitor
URL_LIST = ["https://www.fda.gov/news-events/fda-newsroom/press-announcements"]

# Date range for article search
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

# Keywords to identify relevant articles
KEYWORDS = ["food", "recall", "outbreak", "salmonella", "listeria", "e. coli", "allergen"]
```

## Usage

### Quick Start

Run the complete automated workflow:
```bash
python main.py
```

### Individual Components

**Web Scraping Only**:
```bash
python website_scraper.py
```
- Generates: `scraped_articles.json`

**AI Processing Only** (requires scraped articles):
```bash
python ai_processor.py
```
- Generates: `final_report_YYYYMMDD_HHMMSS.csv` and `final_report_YYYYMMDD_HHMMSS.json`

## Output Files

**All output files are saved in the `/report` folder**

### report/scraped_articles.json
Contains raw scraped article data:
```json
[
  {
    "title": "Voluntary Recall of Specific Cheese Brand Due to Listeria Concerns",
    "url": "https://www.fda.gov/example-article-1",
    "publication_date": "2024-07-15",
    "full_text": "The full text of the press release..."
  }
]
```

### report/final_report_YYYYMMDD_HHMMSS.csv/json
Contains structured extracted information:
- Title
- URL
- Publication Date
- Product Name
- Contaminant/Reason
- Affected Regions
- Company Name
- Processing Date

## Content Verification Logging

The system includes content verification logging that:
- Captures the raw HTML content from the first article found during scraping
- Displays the first 500 characters of the HTML for verification
- Stops execution after the first article to prevent console flooding
- Helps verify that the scraping process is working correctly

**Example output:**
```
--- Verifying Content for URL: https://www.fda.gov/example-article ---
First 500 characters of raw HTML content:
<!DOCTYPE html>
<html lang="en">
<head>
    <title>FDA Recall Notice</title>
</head>
<body>
    <div class="field-item">
        <p>Company XYZ is voluntarily recalling products due to contamination...</p>
--- End of Content Verification ---

*** Stopping execution after first article for content verification ***
```

## AI Processing Features

The AI processor uses advanced pattern matching and NLP techniques to extract:

### Product Names
- Identifies specific food products mentioned in recalls
- Handles various naming conventions and formats

### Contaminants
- Detects common foodborne pathogens (Listeria, Salmonella, E. coli)
- Identifies allergens and contamination types
- Recognizes foreign material contamination

### Company Names
- Extracts manufacturer and distributor information
- Handles various company naming formats

### Affected Regions
- Identifies US states and regions affected by recalls
- Parses distribution information

## Example Workflow

1. **Configuration**: Set date range to monitor last 6 months
2. **Scraping**: System finds 50 food safety articles
3. **Processing**: AI extracts structured data from each article
4. **Reporting**: Generate comprehensive reports showing:
   - Top companies with recalls
   - Most common contaminants
   - Geographic distribution of issues

## Error Handling

The system includes robust error handling for:
- Network connectivity issues
- Malformed HTML content
- Missing article data
- File I/O errors

## Dependencies

- **requests**: Web scraping and HTTP requests
- **beautifulsoup4**: HTML parsing
- **pandas**: Data processing and analysis
- **Standard Python libraries**: datetime, json, csv, re, os, sys

## Troubleshooting

### Common Issues

1. **FDA Website Blocking (404 Error)**:
   - The FDA website may block automated requests
   - **Solution**: Set `TEST_MODE = True` in `config.py` to use sample data
   - Alternative: Try running the script later or from a different network

2. **No articles found**: Check date range and keywords in config.py

3. **Network errors**: Verify internet connection and FDA website availability

4. **Processing errors**: Ensure scraped_articles.json exists and is valid

### Test Mode

When the FDA website is blocking requests, you can use test mode:

```python
# In config.py
TEST_MODE = True  # Use sample data instead of scraping
```

This will generate realistic sample data for testing the AI processing functionality.

### Debug Mode

For detailed debugging information, run individual components:
```bash
python website_scraper.py  # Check scraping results
python ai_processor.py     # Check processing results
```

## Customization

### Adding New Keywords
```python
KEYWORDS = ["food", "recall", "outbreak", "new_keyword"]
```

### Monitoring Additional URLs
```python
URL_LIST = [
    "https://www.fda.gov/news-events/fda-newsroom/press-announcements",
    "https://additional-url.gov/announcements"
]
```

### Extending AI Processing
Modify `ai_processor.py` to add new extraction patterns or improve existing ones.

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is intended for educational and research purposes. Please review FDA website terms of use before extensive scraping.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the project repository.

---

**Note**: This system is designed to monitor publicly available FDA press announcements. Always verify critical information with official FDA sources. 

---
