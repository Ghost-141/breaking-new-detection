from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from scrappers.chrome_driver import get_chrome_driver
from utils.db import save_to_db
import datetime as dt
import time


def scrape_ekattor():
    driver = get_chrome_driver(headless=True)
    seen_titles = set()

    try:
        driver.get("https://ekattor.tv/")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        conveyor = soup.find("div", class_="ticker_slider widget_marquee")

        if not conveyor:
            print("Ticker slider not found")
            return

        links = [link.get("href") for link in conveyor.find_all("a", href=True)]
        print(f"Found {len(links)} news items")

        for url in links:
            try:
                if not url.startswith("http"):
                    url = "https://ekattor.tv" + url

                driver.get(url)
                time.sleep(2)

                page_soup = BeautifulSoup(driver.page_source, "html.parser")

                title_el = page_soup.select_one("h1[itemprop='headline']")
                title = title_el.get_text(" ", strip=True) if title_el else None

                if not title or title in seen_titles:
                    continue

                seen_titles.add(title)

                time_elem = page_soup.select_one("span[itemprop='datePublished']")
                publish_time = None
                if time_elem and time_elem.get("content"):
                    try:
                        dt_obj = dt.datetime.fromisoformat(time_elem.get("content"))
                        publish_time = dt_obj.strftime("%d-%m-%Y %I:%M:%S")
                    except:
                        pass

                print(f"\nProcessing: {title}")

                save_to_db(
                    source="Ekattor TV",
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

    print(f"\n✅ Saved Ekattor TV news to database")


if __name__ == "__main__":
    scrape_ekattor()
