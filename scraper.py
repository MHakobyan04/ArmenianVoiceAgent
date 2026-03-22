import os
import requests
from bs4 import BeautifulSoup
import json


def clean_text(text):
    # List of junk words to remove from the scraped content
    junk_words = [
        "Դիմել հիմա", "Ավելին", "Իմանալ ավելին",
        "Հայտ ներկայացնել", "Սեղմեք այստեղ",
        "Մանրամասն", "Պատվիրել քարտը", "Դիմել"
    ]

    cleaned = text
    for word in junk_words:
        cleaned = cleaned.replace(word, "")

    # Remove empty lines and extra whitespace for cleaner vectors
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines)


def scrape_bank_data(bank_name, urls):
    all_text = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for url in urls:
        try:
            print(f"[Info] Scraping URL: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove navigation, footer, and scripts to keep only the main content
            for element in soup(['nav', 'footer', 'header', 'script', 'style']):
                element.decompose()

            raw_text = soup.get_text(separator='\n')
            processed_text = clean_text(raw_text)

            all_text += f"\n--- Source: {url} ---\n" + processed_text + "\n"

        except Exception as e:
            print(f"[Error] Failed to scrape {url}. Reason: {e}")

    return all_text


def main():
    print("[Debug] Scraper script started successfully.")

    # Create the data directory if it doesn't exist
    if not os.path.exists("data"):
        print("[Debug] Creating 'data' directory.")
        os.makedirs("data")

    # Load and parse the configuration file
    try:
        print("[Debug] Reading banks_config.json...")
        with open("banks_config.json", "r", encoding="utf-8") as f:
            banks_data = json.load(f)

        # Handle different potential JSON structures gracefully
        if isinstance(banks_data, dict):
            banks_list = banks_data.get('banks', [banks_data])
        else:
            banks_list = banks_data

        print(f"[Debug] Found {len(banks_list)} bank(s) in configuration.")

    except FileNotFoundError:
        print("[Error] banks_config.json not found!")
        return
    except json.JSONDecodeError:
        print("[Error] banks_config.json is empty or has invalid JSON format!")
        return

    # Iterate through the configuration and start scraping
    for bank in banks_list:
        if isinstance(bank, str):
            continue

        name = bank.get('name', 'Unknown Bank')
        urls = bank.get('urls', [])

        if not urls:
            print(f"[Warning] No URLs found for {name}. Skipping.")
            continue

        print(f"\n[Info] Starting scraping process for {name}...")
        bank_info = scrape_bank_data(name, urls)

        file_path = f"data/{name.lower().replace(' ', '_')}_info.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(bank_info)

        print(f"[Success] Data for {name} saved to {file_path}")


# This is the critical entry point that actually executes the logic
if __name__ == "__main__":
    main()