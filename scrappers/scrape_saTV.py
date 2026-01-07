from selenium.webdriver.common.by import By
from scrappers.chrome_driver import (
    get_chrome_driver,
    wait_for_elements,
    get_element_text,
    get_element_attribute,
)
from utils.db import save_to_db
from utils.news_detector import is_breaking_news
from bs4 import BeautifulSoup
import time


def scrape_satv():
    driver = get_chrome_driver(headless=True)
    seen_titles = set()

    try:
        driver.get("https://www.satv.tv/")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        conveyor = soup.find("div", class_="footer-scrool-2")

        if not conveyor:
            print("footer-scrool-2 not found")
            return

        links = [link.get("href") for link in conveyor.find_all("a", href=True)]
        print(f"Found {len(links)} potential news items")

        for url in links:
            try:
                driver.get(url)
                time.sleep(2)

                page_soup = BeautifulSoup(driver.page_source, "html.parser")

                title_el = page_soup.select_one("h1.single-page-title")
                title = title_el.get_text(" ", strip=True) if title_el else None

                if not title or title in seen_titles:
                    continue

                seen_titles.add(title)

                time_elem = page_soup.select_one(
                    "div.viwe-count li:has(i.la-clock-o), div.viwe-count li:has(i.la.la-clock-o)"
                )
                publish_time = (
                    " ".join(time_elem.get_text(strip=True).split())
                    if time_elem
                    else None
                )

                print(f"\nProcessing: {title}")

                save_to_db(
                    source="SA TV",
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

    print(f"\n✅ Saved SA TV news to database")


if __name__ == "__main__":
    scrape_satv()
