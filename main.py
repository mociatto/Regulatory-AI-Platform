"""
FDA Food Safety Monitor - Main Orchestrator
============================================

This is the main entry point for the automated FDA Food Safety Monitor system.
It orchestrates the entire workflow from web scraping to AI-powered analysis.

Workflow:
1. Scrape FDA press announcements for food safety-related articles
2. Process articles with AI to extract structured information
3. Generate comprehensive reports in CSV and JSON formats

Author: FDA Food Safety Monitor System
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import time
import google.generativeai as genai
from config import TARGETS, PHARMA_KEYWORDS, SEARCH_START_DATE, SEARCH_END_DATE
from ai_processor import analyze_article_with_ai
from flask import Flask
from google.cloud import storage

app = Flask(__name__)

def fetch_and_parse_rss(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        articles = []
        for item in items:
            title_tag = item.find('title')
            link_tag = item.find('link')
            pub_date_tag = item.find('pubDate')
            title = title_tag.text.strip() if title_tag else ''
            link = link_tag.text.strip() if link_tag else ''
            pub_date = pub_date_tag.text.strip() if pub_date_tag else ''
            articles.append({'title': title, 'link': link, 'pub_date': pub_date})
        return articles
    except Exception as e:
        print(f"Error fetching or parsing RSS feed: {e}")
        return []

def fetch_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        main = soup.find('main', id='main-content')
        if not main:
            print("Could not find <main id='main-content'> in the article.")
            return ''
        paragraphs = main.find_all('p')
        if not paragraphs:
            print("No <p> tags found in the main content.")
            return ''
        text = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        return text
    except Exception as e:
        print(f"Error fetching or parsing article text: {e}")
        return ''

def parse_rss_date(date_string):
    """Parses date strings from RSS feeds into datetime objects."""
    try:
        # Format for dates like 'Fri, 18 Jul 2025 17:03:25 GMT'
        return datetime.strptime(date_string.strip(), '%a, %d %b %Y %H:%M:%S %Z')
    except ValueError:
        return None

def is_article_relevant(text, keywords):
    """
    Check if any keyword is present in the article text (case-insensitive).
    Returns (is_relevant, found_keywords_list).
    """
    text_lower = text.lower()
    found_keywords = []
    for keyword in keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    if found_keywords:
        return True, found_keywords
    else:
        return False, []

def save_report(report_data, bucket_name, filename):
    """Save report data to a JSON file in a Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        report_json_string = json.dumps(report_data, indent=2, ensure_ascii=False)
        blob.upload_from_string(report_json_string, content_type='application/json')
        print(f"Report saved to: gs://{bucket_name}/{filename}")
    except Exception as e:
        print(f"Error saving report to GCS: {e}")

@app.route('/')
def trigger_pipeline():
    # This is the entry point when the service is called
    return run_analysis_pipeline()

def run_analysis_pipeline():
    # All the logic that was previously in if __name__ == "__main__" goes here
    # Configure the Vertex AI model using Application Default Credentials
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        # Initialize Vertex AI. It will automatically use the service account's permissions.
        project_id = os.environ.get('GCP_PROJECT')
        location = 'us-central1' # Or your preferred region
        vertexai.init(project=project_id, location=location)
        # Initialize Vertex AI model
        model = GenerativeModel("text-bison@001")
        print("Vertex AI model configured successfully.")
    except Exception as e:
        print(f"Error initializing Vertex AI: {e}")
        return f"Error: Could not configure AI model. {e}"
    
    rss_url = TARGETS['UK']['rss_feed_url']
    print(f"Parsing BBC Health RSS feed: {rss_url}")
    articles = fetch_and_parse_rss(rss_url)
    if articles:
        print(f"\nSuccess! Found {len(articles)} articles.")
        relevant_articles = []
        ai_findings = []
        # Convert config date strings to datetime objects
        start_date = datetime.strptime(SEARCH_START_DATE, '%Y-%m-%d')
        end_date = datetime.strptime(SEARCH_END_DATE, '%Y-%m-%d')
        for i, article in enumerate(articles, 1):
            print(f"Processing article {i}/{len(articles)}: {article['title']}")
            # Parse the publication date
            parsed_date = parse_rss_date(article['pub_date'])
            if parsed_date is None or not (start_date <= parsed_date <= end_date):
                print("   -> Skipping article (out of date range).")
                continue
            full_text = fetch_article_text(article['link'])
            is_relevant, matched_keywords = is_article_relevant(full_text, PHARMA_KEYWORDS)
            if is_relevant:
                relevant_articles.append({
                    'title': article['title'],
                    'link': article['link'],
                    'pub_date': article['pub_date'],
                    'matched_keywords': matched_keywords
                })
                print(f"Found relevant article! (Matches: {matched_keywords})")
                
                # AI Analysis for the relevant article
                print("\n--- AI Analysis ---")
                ai_analysis = analyze_article_with_ai(full_text, model)
                print("AI Analysis Result:")
                print(ai_analysis)
                print("--- End AI Analysis ---")
                
                # Add delay to be respectful to the API
                time.sleep(1)
                
                # Create complete analysis dictionary
                analysis_dict = {
                    'title': article['title'],
                    'link': article['link'],
                    'pub_date': article['pub_date'],
                    'matched_keywords': matched_keywords,
                    'ai_analysis': ai_analysis
                }
                ai_findings.append(analysis_dict)
        print("\n---")
        print(f"Processing Complete. Found {len(relevant_articles)} relevant articles out of {len(articles)} total.")
        
        # Save AI findings to Google Cloud Storage
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        if bucket_name:
            # Create a timestamp for a unique filename
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"report_{timestamp}.json"
            save_report(ai_findings, bucket_name, filename)
        else:
            print("GCS_BUCKET_NAME environment variable not set. Skipping report save.")
        
        if relevant_articles:
            print("\nCollected Relevant Articles:")
            for i, article in enumerate(relevant_articles, 1):
                print(f"{i}. {article['title']}")
                print(f"   Link: {article['link']}")
                print(f"   Published: {article['pub_date']}")
                print(f"   Matched Keywords: {article['matched_keywords']}")
                print()
        
        # At the end, instead of printing, return a success message
        return "Regulatory AI Pipeline finished successfully."
    else:
        print("No articles found or an error occurred during RSS parsing.")
        return "Error: No articles found or an error occurred during RSS parsing."

if __name__ == "__main__":
    # This block is for running the app locally for testing
    # Cloud Run will use a production WSGI server instead
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port) 

# cloud test