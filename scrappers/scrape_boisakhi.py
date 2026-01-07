from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from scrappers.chrome_driver import get_chrome_driver
from utils.db import save_to_db
from utils.time_parser import boisakhi_datetime
import time


def scrape_boisakhi():
    driver = get_chrome_driver(headless=True)
    seen_titles = set()

    try:
        driver.get("https://boishakhionline.com/")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        conveyor = soup.find("div", class_="flex-grow-1 d-flex m-auto")

        if not conveyor:
            print("Conveyor not found")
            return

        links = [link.get("href") for link in conveyor.find_all("a", href=True)]
        print(f"Found {len(links)} potential news items")

        for url in links:
            try:
                driver.get(url)
                time.sleep(2)

                page_soup = BeautifulSoup(driver.page_source, "html.parser")

                title_elem = page_soup.find("div", class_="headline_section mb-2")
                title = title_elem.get_text(strip=True) if title_elem else None

                if not title or title in seen_titles:
                    continue

                seen_titles.add(title)

                time_elem = page_soup.find(
                    "div", class_="entry_update mb-0"
                ) or page_soup.find("div", "entry_update entry_time_new mb-0")
                publish_time = time_elem.get_text(strip=True) if time_elem else None

                if publish_time:
                    formatted_time = boisakhi_datetime(publish_time)
                    publish_time = formatted_time.strftime("%Y-%m-%d %I:%M")

                print(f"\nProcessing: {title}")

                save_to_db(
                    source="Boisakhi TV",
                    title=title,
                    summary=None,
                    category=None,
                    link=url,
                    publish_time=publish_time,
                )

                time.sleep(1)
            except Exception as e:
                print("Item Error:", e)

    finally:
        driver.quit()

    print(f"\n✅ Saved Boisakhi TV news to database")


if __name__ == "__main__":
    scrape_boisakhi()
