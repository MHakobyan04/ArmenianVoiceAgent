import requests
import json
import os
from bs4 import BeautifulSoup
import time


def scrape_page(url):
    # Disguise as a standard Mac browser to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'  # Ensure correct encoding for Armenian characters
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            # Remove unnecessary parts of the page
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator='\n')
            lines = (line.strip() for line in text.splitlines())
            return '\n'.join(chunk for chunk in lines if chunk)
    except Exception as e:
        print(f"Error reading {url}: {e}")
    return None


def main():
    # Create the data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Read the verified URLs from the JSON file
    with open('banks_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    for bank in config['banks']:
        print(f"Scraping data for {bank['name']}...")
        bank_content = ""

        for url in bank['urls']:
            print(f"Reading: {url}")
            content = scrape_page(url)
            if content:
                bank_content += f"\n--- Source: {url} ---\n" + content
            time.sleep(1)  # Add a small delay to avoid overloading the servers

        # Save the cleaned text in the data directory
        file_path = f"data/{bank['name'].lower()}_info.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(bank_content)
        print(f"Finished {bank['name']}. Saved to {file_path}\n")


if __name__ == "__main__":
    main()