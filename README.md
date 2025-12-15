# Breaking News Scraper

A Python-based news scraping system that collects articles from Bangladeshi news websites and automatically detects breaking news using AI-powered similarity analysis with local embedding models.

## Features

- **Multi-source scraping**: Jamuna TV, Somoy TV, Independent TV
- **Breaking news detection**: AI-powered classification using local sentence transformers
- **International news filtering**: Automatic filtering of international news
- **Database storage**: MySQL integration with duplicate prevention and pending status tracking
- **WhatsApp integration**: Automatic breaking news notifications

## Project Structure

```
Scrapping Codes/
├── models/              # Local AI models
├── scrappers/           # News scraper modules
│   ├── chrome_driver.py # Selenium WebDriver utilities
│   ├── scrape_jamuna.py # Jamuna TV scraper
│   ├── scrape_somoy.py  # Somoy TV scraper
│   ├── scrape_independent.py # Independent TV scraper
│   └── scrape_channel24.py # Channel 24 scraper
├── utils/               # Utility functions
│   ├── db.py           # Database operations
│   ├── news_detector.py # Breaking news detection logic
│   ├── filters.py      # Country/region filters and breaking keywords
│   ├── is_break.py     # Core breaking news detection with embeddings
│   ├── news_filter.py  # International news filtering
│   ├── send_breaking_news.py # Breaking news sender
│   └── send_message.py # WhatsApp message utilities
├── main.py             # Main application entry point
├── is_break.py         # Breaking news detection (root level)
├── save_model.py       # Model saving utilities
├── main.sh             # Shell script for automation
├── pyproject.toml      # Project dependencies
├── uv.lock            # UV lock file
├── .env.example       # Environment variables example
└── .python-version    # Python version specification
```

## Setup

### Prerequisites

- Python 3.13+
- MySQL Server
- Chrome Browser
- CUDA-compatible GPU (optional, for faster inference)
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Scrapping Codes"
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Setup MySQL database**
   ```bash
   mysql -u root -p < news_automation.sql
   ```

4. **Download embedding models**

   Download the embedding model from hugging face repository and save it to local device for future usage.

5. **Setup environment variables**
   create a .env file similar to [.env.example](.env.example) and update the .env file name to [send_message]](utils/send_message.py) function.

6. **Configure database connection**
   Update `utils/db.py` with your MySQL credentials:
   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="your_username", 
       password="your_password",
       database="news_automation"
   )
   ```

## Usage

### Run All Scrapers with Breaking News Detection
```bash
python main.py
```

### Run Individual Scrapers
```bash
python -m scrappers.scrape_somoy
python -m scrappers.scrape_jamuna
python -m scrappers.scrape_independent
python -m scrappers.scrape_channel24
```

### Send Breaking News to WhatsApp
```bash
python -m utils.send_breaking_news
```

### Query Database
```bash
python test_functions/query_db.py
```

### Test Breaking News Detection
```bash
python test_functions/test_breaking_news.py
```

### Run with Shell Script
```bash
./main.sh
```

## Breaking News Detection

The system uses AI-powered similarity analysis to detect breaking news:

- **Threshold**: Configurable similarity score (default: 0.85)
- **Keywords**: Predefined Bengali keywords for critical events
- **Models**: Local sentence transformers (e5-small, bengali-sentence-similarity-sbert)
- **Processing**: Batch processing with GPU acceleration when available
- **Filtering**: International news filtering to focus on local breaking news
- **Output**: Returns 1 (breaking) or 0 (normal)

### Breaking News Keywords
- হত্যা (murder), দুর্ঘটনা (accident), মৃত্যু (death)
- আগুন (fire), বিস্ফোরণ (explosion), ভূমিকম্প (earthquake)
- গ্রেফতার (arrest), বিক্ষোভ (protest), সংঘর্ষ (clash)
- বন্যা (flood), ঝড় (storm), জরুরি (emergency)

## Database Schema

```sql
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    full_content LONGTEXT,
    category VARCHAR(100),
    link VARCHAR(500) NOT NULL UNIQUE,
    thumbnail VARCHAR(500),
    publish_time VARCHAR(500),
    is_breaking TINYINT DEFAULT 0,
    sent_status TINYINT DEFAULT 0,
    pending TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Dependencies

- **selenium**: Web scraping automation
- **sentence-transformers**: Local AI embeddings for breaking news detection
- **beautifulsoup4**: HTML parsing
- **webdriver-manager**: Automatic WebDriver management
## Environment Configuration

The project supports multiple environments:
- `.env.dep`: Development environment
- `.env.test`: Testing environment
- `.env.example`: Template for environment variables

## Automation

- **Cron Integration**: Use `main.sh` for scheduled execution
- **Logging**: Comprehensive logging in `cron.log`
- **Model Management**: Local model storage in `models/` directory



