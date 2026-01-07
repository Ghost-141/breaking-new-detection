from bs4 import BeautifulSoup
import time
from scrappers.chrome_driver import get_chrome_driver
from utils.db import save_to_db
from utils.time_parser import atn_datetime


def scrape_atn():
    driver = get_chrome_driver(headless=True)
    seen_titles = set()

    try:
        driver.get("https://www.atnnewstv.com/")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        conveyor = soup.find("div", class_=lambda x: x and "js-conveyor" in x)

        if not conveyor:
            print("js-conveyor not found")
            return

        links = [link.get("href") for link in conveyor.find_all("a", href=True)]
        print(f"Found {len(links)} potential news items")

        for url in links:
            try:
                driver.get(url)
                time.sleep(2)

                page_soup = BeautifulSoup(driver.page_source, "html.parser")

                title_elem = page_soup.find("div", class_="col-sm-12 main-title")
                title = title_elem.get_text(strip=True) if title_elem else None

                if not title or title in seen_titles:
                    continue

                seen_titles.add(title)

                time_elem = page_soup.find("div", class_="col-sm-12 col-md-12")
                publish_time = time_elem.get_text(strip=True) if time_elem else None

                formatted_time = atn_datetime(publish_time)

                print(f"\nProcessing: {title}")

                save_to_db(
                    source="ATN News",
                    title=title,
                    summary="",
                    category="",
                    link=url,
                    publish_time=formatted_time or "",
                )

                time.sleep(1)
            except Exception as e:
                print("Item Error:", e)

    finally:
        driver.quit()

    print(f"\n✅ Saved ATN News to database")


if __name__ == "__main__":
    scrape_atn()
