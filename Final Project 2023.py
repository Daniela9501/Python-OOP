import requests
import csv
from pathlib import Path
from time import sleep

# Constants
API_KEY = '48EsLPXt1kynelCRYmkh206vXHvt6pd1'
URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
OUTPUT_FILE = 'nyt_annual_climate_article_counts.csv'
REQUEST_DELAY = 20  # in seconds
PAGE_SIZE = 10  # Adjust based on your requirements

def article_count(start_date, end_date):
    """

    Fetches the count of articles from the New York Times API for a giving data range

    Args:
        start_date (str): The start date in 'YYYYMMDD' format
        end_date (str): The end date in 'YYYYMMDD' format

    Raises:
        requests.exceptions.HTTPError: if the API request fails with a non-200 status code.

    Returns:
        int: The count of articles within the given date range
    """
    # Define parameters for the API request
    parameters = {
        'q': 'climate Change',
        'api-key': API_KEY,
        'begin_date': start_date,
        'end_date': end_date,
        'fl': 'headline',  # Only fetch headlines to count articles
        'sort': 'newest',  # Sort by newest articles
        'page_size': PAGE_SIZE,  # Adjust the page size
    }
    # Make an HTTP GET request to the New York Times API
    response = requests.get(URL, params=parameters)

    # Check if the API request was successful
    if response.status_code == 200:
        # Extract the total number of hits from the API response
        data = response.json()['response']
        hits = data['meta']['hits']
        return hits
    else:
        # Raise an exception for non-200 status codes
        raise requests.exceptions.HTTPError(f"API request failed with status {response.status_code}: {response.text}")

def write_article_counts_to_csv(year, count, file_name):
    """
    Writes the year and the count of articles to a CSV file.

    Args:
        year (int): The year for which the count is recorded
        count (int): The number of articles for the specified year.
        file_name (str): The name of the CSV file to write to.
    """
    # Open the CSV file for appending
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the year and count of articles to the CSV file
        writer.writerow([year, count])

def fetch_and_write_article_counts_by_year(start_year, end_year):
    """
    Fetches and writes the articles counts for each year in the specified range to a CSV file

    Args:
        start_year (int): The starting year of the range
        end_year (int): The ending year of the range
    """
    for year in range(start_year, end_year + 1):
        start_date = f"{year}0101"
        end_date = f"{year}1231"
        count = article_count(start_date, end_date)  # Get article count for the year
        write_article_counts_to_csv(year, count, OUTPUT_FILE)
        print(f"Year {year} has {count} articles.")
        sleep(REQUEST_DELAY)  # Delay to respect API rate limits

if __name__ == "__main__":
    # Create a new CSV file if it doesn't exist
    output_file_path = Path(OUTPUT_FILE)
    if not output_file_path.is_file():
        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Year', 'Article Count'])

    # Fetch and write article counts for each year
    fetch_and_write_article_counts_by_year(1980, 2020)
