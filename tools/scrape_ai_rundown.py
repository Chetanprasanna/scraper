#!/usr/bin/env python3
"""
AI Rundown Scraper
Scrapes latest AI news from therundown.ai

Output: .tmp/scraped_data/ai_rundown.json
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import hashlib
import time
import os
import re

def generate_article_id(url):
    """Generate unique ID from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def scrape_ai_rundown():
    """Scrape The AI Rundown newsletter site"""
    url = "https://www.therundown.ai"
    
    print(f"🔍 Scraping The AI Rundown: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        current_time = datetime.now()
        
        # Find article containers - looking for h3 headers which contain article titles
        article_headers = soup.find_all('h3')
        
        for header in article_headers:
            # Get the title text
            title_text = header.get_text(strip=True)
            
            # Skip if empty or too short
            if not title_text or len(title_text) < 5:
                continue
            
            # Find the link
            article_link = header.find('a', href=True)
            if not article_link:
                # Check parent for link
                parent = header.find_parent('a', href=True)
                if parent:
                    article_link = parent
                else:
                    continue
            
            article_url = article_link.get('href', '')
            
            # Make absolute URL
            if article_url.startswith('/'):
                article_url = f"https://www.therundown.ai{article_url}"
            
            # Skip if not a valid article URL
            if not article_url or 'therundown.ai' not in article_url:
                continue
            
            # Look for description/subtitle nearby
            description = ""
            next_elem = header.find_next_sibling()
            if next_elem:
                desc_text = next_elem.get_text(strip=True)
                # The AI Rundown uses "PLUS:" format for tool highlights
                if desc_text and len(desc_text) > 10:
                    description = desc_text
            
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
                "source": "ai_rundown",
                "title": title_text,
                "description": description,
                "url": article_url,
                "image_url": image_url,
                "published_date": current_time.isoformat(),
                "scraped_date": current_time.isoformat(),
                "tags": ["AI", "newsletter"],
                "saved": False
            }

            
            articles.append(article)
        
        # Remove duplicates
        unique_articles = []
        seen_urls = set()
        for article in articles:
            if article['url'] not in seen_urls:
                unique_articles.append(article)
                seen_urls.add(article['url'])
        
        # Limit to recent articles
        articles = unique_articles[:15]
        
        print(f"✅ Found {len(articles)} articles from The AI Rundown")
        
        # Save to file
        output_dir = os.path.join('.tmp', 'scraped_data')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'ai_rundown.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {output_path}")
        
        return {
            "success": True,
            "article_count": len(articles),
            "last_scraped": current_time.isoformat()
        }
        
    except requests.RequestException as e:
        print(f"❌ Error scraping The AI Rundown: {e}")
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
    result = scrape_ai_rundown()
    print(json.dumps(result, indent=2))
