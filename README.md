# AI News Scraper & Dashboard

A web scraping tool that aggregates the latest AI news from multiple sources and displays them in a beautiful, interactive dashboard.

## 🌟 Features

- **Multi-Source Scraping**: Scrapes AI news from:
  - [The AI Rundown](https://www.therundown.ai)
  - [Ben's Bites](https://news.bensbites.co)
- **Data Aggregation**: Combines articles from all sources into a unified JSON payload
- **Interactive Dashboard**: View all scraped articles in a sleek, modern web interface
- **Image Extraction**: Automatically fetches article images and logos
- **Duplicate Detection**: Filters out duplicate articles
- **Save Functionality**: Mark and save your favorite articles

## 📁 Project Structure

```
.
├── tools/                          # Scraping scripts
│   ├── scrape_ai_rundown.py       # The AI Rundown scraper
│   ├── scrape_bens_bites.py       # Ben's Bites scraper
│   └── aggregate_data.py          # Data aggregation script
├── dashboard/                      # Web dashboard
│   ├── index.html                 # Dashboard UI
│   ├── app.js                     # Dashboard JavaScript
│   ├── styles.css                 # Dashboard styles
│   └── assets/                    # Source logos
├── .tmp/                          # Temporary data storage
│   ├── scraped_data/              # Raw scraped data
│   └── aggregated_articles.json  # Aggregated output
└── requirements.txt               # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chetanprasanna/scraper.git
   cd scraper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Step 1: Scrape Data from Sources

Run the individual scrapers to fetch the latest articles:

```bash
# Scrape The AI Rundown
python tools/scrape_ai_rundown.py

# Scrape Ben's Bites
python tools/scrape_bens_bites.py
```

Each scraper will save data to `.tmp/scraped_data/` directory.

### Step 2: Aggregate the Data

Combine all scraped data into a single file:

```bash
python tools/aggregate_data.py
```

This creates `.tmp/aggregated_articles.json` with all articles combined.

### Step 3: View in Dashboard

Open the dashboard in your browser:

```bash
# Option 1: Open directly (if using macOS)
open dashboard/index.html

# Option 2: Use Python's built-in server
cd dashboard
python -m http.server 8000
# Then visit http://localhost:8000 in your browser
```

### Run All Steps at Once

You can also run a complete scraping workflow:

```bash
# Run all scrapers and aggregate
python tools/scrape_ai_rundown.py && \
python tools/scrape_bens_bites.py && \
python tools/aggregate_data.py && \
echo "✅ Scraping complete! Open dashboard/index.html to view results."
```

## 🎨 Dashboard Features

The dashboard provides:
- **Article Cards**: Visual cards showing article title, source, and image
- **Source Filtering**: Filter articles by source
- **Save Articles**: Mark articles to save for later
- **Responsive Design**: Works on desktop and mobile devices
- **Direct Links**: Click any article to open the full story

## 📊 Data Structure

Each article in the aggregated JSON contains:

```json
{
  "id": "unique-hash",
  "source": "ai_rundown",
  "title": "Article Title",
  "description": "Article description",
  "url": "https://example.com/article",
  "image_url": "https://example.com/image.jpg",
  "published_date": "2026-02-13T21:00:00",
  "scraped_date": "2026-02-13T21:00:00",
  "tags": ["AI", "newsletter"],
  "saved": false
}
```

## 🛠️ Technical Details

### Dependencies

- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing and scraping

### How It Works

1. **Scrapers** fetch HTML from news sources
2. **BeautifulSoup** parses the HTML to extract article data
3. **Data Aggregator** combines all sources into one JSON file
4. **Dashboard** loads and displays the JSON data with JavaScript

## 🔧 Customization

### Adding New Sources

To add a new news source:

1. Create a new scraper in `tools/scrape_source_name.py`
2. Follow the same structure as existing scrapers
3. Update `aggregate_data.py` to include the new source
4. Add source logo to `dashboard/assets/`

### Modifying Scraping Logic

Each scraper can be customized:
- Change the number of articles: Modify the slice value (e.g., `[:15]`)
- Add new fields: Extend the article dictionary
- Change URL patterns: Update the filtering logic

## 📝 Notes

- The scrapers respect website structure as of February 2026
- Website structure changes may require scraper updates
- Rate limiting is implemented to be respectful to source websites
- Images are fetched using Open Graph and Twitter Card meta tags

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📜 License

This project is open source and available for educational purposes.

## ⚠️ Disclaimer

This tool is for educational purposes. Please respect the terms of service of the websites you scrape and use this responsibly.
