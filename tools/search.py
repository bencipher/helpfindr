import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_SEARCH_KEY = os.environ.get('GOOGLE_SEARCH_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')


def get_research_urls(query):
    search_url = build_googlesearch_url(query, GOOGLE_CSE_ID, 10, GOOGLE_SEARCH_KEY)
    search_response = google_search_response(search_url)
    research_urls = []
    for item in search_response['items']:
        research_urls.append(item['link'])
    return research_urls


def build_googlesearch_url(q, cx, num, key):
    q = q.replace(" ", "+")
    base_url = "https://customsearch.googleapis.com/customsearch/v1"
    url_params = f"?q={q}&cx={cx}&num={num}&key={key}&alt=json"
    full_url = base_url + url_params
    return full_url


def google_search_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except ValueError as ve:
        print(f"Error parsing JSON data: {ve}")
        return None
