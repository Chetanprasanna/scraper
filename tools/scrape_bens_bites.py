#!/usr/bin/env python3
"""
Ben's Bites Scraper
Scrapes latest AI news from news.bensbites.co

Output: .tmp/scraped_data/bens_bites.json
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import hashlib
import time
import os

def generate_article_id(url):
    """Generate unique ID from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def scrape_bens_bites():
    """Scrape Ben's Bites news feed"""
    url = "https://news.bensbites.co"
    
    print(f"🔍 Scraping Ben's Bites: {url}")
    
    try:
        # Add headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=24)
        
        # Find article links - Ben's Bites uses a custom structure
        # Looking for links to posts
        post_links = soup.find_all('a', href=True)
        
        seen_urls = set()
        
        for link in post_links:
            href = link.get('href', '')
            
            # Filter for actual article/post links
            if '/posts/' in href or href.startswith('http'):
                # Make absolute URL
                if href.startswith('/'):
                    article_url = f"https://news.bensbites.co{href}"
                else:
                    article_url = href
                
                # Skip if already seen or not relevant
                if article_url in seen_urls or article_url == url:
                    continue
                
                # Skip internal navigation links
                if '/tags/' in article_url or '/out' in article_url:
                    # Extract actual external URL from /out links
                    if '/out' in article_url:
                        continue
                
                seen_urls.add(article_url)
                
                # Get title from link text
                title = link.get_text(strip=True)
                
                # Skip empty or very short titles
                if not title or len(title) < 3:
                    continue
                
                # Look for tags nearby
                tags = []
                parent = link.find_parent()
                if parent:
                    tag_elements = parent.find_all('a', href=lambda x: x and '/tags/' in x)
                    tags = [tag.get_text(strip=True) for tag in tag_elements]
                
                # Try to get image for this article
                image_url = None
                try:
                    article_response = requests.get(article_url, headers=headers, timeout=5)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        
                        # Try og:image first
                        og_image = article_soup.find('meta', property='og:image')
                        if og_image and og_image.get('content'):
                            image_url = og_image.get('content')
                        
                        # Fallback to twitter:image
                        if not image_url:
                            twitter_image = article_soup.find('meta', attrs={'name': 'twitter:image'})
                            if twitter_image and twitter_image.get('content'):
                                image_url = twitter_image.get('content')
                        
                        # Fallback to first image
                        if not image_url:
                            first_img = article_soup.find('img', src=True)
                            if first_img:
                                img_src = first_img.get('src')
                                if img_src and img_src.startswith('http'):
                                    image_url = img_src
                except:
                    pass  # Skip image if fetching fails
                
                article = {
                    "id": generate_article_id(article_url),
                    "source": "ben_bites",
                    "title": title,
                    "description": "",  # Ben's Bites doesn't show descriptions on main page
                    "url": article_url,
                    "image_url": image_url,
                    "published_date": current_time.isoformat(),  # Use current time as approximation
                    "scraped_date": current_time.isoformat(),
                    "tags": tags if tags else [],
                    "saved": False
                }
                
                articles.append(article)
        
        # Remove duplicates by URL
        unique_articles = []
        seen_urls = set()
        for article in articles:
            if article['url'] not in seen_urls:
                unique_articles.append(article)
                seen_urls.add(article['url'])
        
        # Limit to reasonable number
        articles = unique_articles[:20]
        
        print(f"✅ Found {len(articles)} articles from Ben's Bites")
        
        # Save to file
        output_dir = os.path.join('.tmp', 'scraped_data')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'bens_bites.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {output_path}")
        
        return {
            "success": True,
            "article_count": len(articles),
            "last_scraped": current_time.isoformat()
        }
        
    except requests.RequestException as e:
        print(f"❌ Error scraping Ben's Bites: {e}")
        return {
            "success": False,
            "error": str(e),
            "article_count": 0,
            "last_scraped": current_time.isoformat()
        }
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {
            "success": False,
            "error": str(e),
            "article_count": 0,
            "last_scraped": current_time.isoformat()
        }

if __name__ == "__main__":
    result = scrape_bens_bites()
    print(json.dumps(result, indent=2))
