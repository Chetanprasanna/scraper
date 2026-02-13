#!/usr/bin/env python3
"""
Data Aggregator
Combines all scraped sources into a single unified payload

Input: .tmp/scraped_data/*.json
Output: .tmp/aggregated_articles.json
"""

import json
import os
import glob
from datetime import datetime

def aggregate_data():
    """Combine all scraped data sources"""
    print("🔄 Aggregating data from all sources...")
    
    scraped_dir = os.path.join('.tmp', 'scraped_data')
    
    all_articles = []
    sources_status = {
        "ben_bites": {"last_scraped": None, "article_count": 0, "status": "not_run"},
        "ai_rundown": {"last_scraped": None, "article_count": 0, "status": "not_run"}
    }
    
    # Read Ben's Bites data
    bens_bites_path = os.path.join(scraped_dir, 'bens_bites.json')
    if os.path.exists(bens_bites_path):
        try:
            with open(bens_bites_path, 'r', encoding='utf-8') as f:
                bens_articles = json.load(f)
                all_articles.extend(bens_articles)
                sources_status["ben_bites"] = {
                    "last_scraped": datetime.now().isoformat(),
                    "article_count": len(bens_articles),
                    "status": "success"
                }
                print(f"✅ Loaded {len(bens_articles)} articles from Ben's Bites")
        except Exception as e:
            print(f"❌ Error loading Ben's Bites data: {e}")
            sources_status["ben_bites"]["status"] = "error"
    
    # Read AI Rundown data
    ai_rundown_path = os.path.join(scraped_dir, 'ai_rundown.json')
    if os.path.exists(ai_rundown_path):
        try:
            with open(ai_rundown_path, 'r', encoding='utf-8') as f:
                rundown_articles = json.load(f)
                all_articles.extend(rundown_articles)
                sources_status["ai_rundown"] = {
                    "last_scraped": datetime.now().isoformat(),
                    "article_count": len(rundown_articles),
                    "status": "success"
                }
                print(f"✅ Loaded {len(rundown_articles)} articles from The AI Rundown")
        except Exception as e:
            print(f"❌ Error loading AI Rundown data: {e}")
            sources_status["ai_rundown"]["status"] = "error"
    
    # Sort by published date (newest first)
    all_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
    
    # Create aggregated payload
    payload = {
        "last_updated": datetime.now().isoformat(),
        "total_articles": len(all_articles),
        "articles": all_articles,
        "sources": sources_status
    }
    
    # Save aggregated data
    output_path = os.path.join('.tmp', 'aggregated_articles.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Aggregated {len(all_articles)} total articles")
    print(f"💾 Saved to {output_path}")
    
    return payload

if __name__ == "__main__":
    result = aggregate_data()
    print(f"\n📊 Summary:")
    print(f"Total articles: {result['total_articles']}")
    print(f"Sources: {json.dumps(result['sources'], indent=2)}")
