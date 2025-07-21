import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_name_link_youtube(driver, youtube_url):
    driver.get(youtube_url)
    wait = WebDriverWait(driver, 10)

    try:
        # Wait for video links to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'ytd-video-renderer')))
        time.sleep(2)  # Small buffer for JS-rendered content

        videos = driver.find_elements(By.XPATH, '//a[@id="video-title"]')

        for video in videos:
            name = video.get_attribute('title')
            link = video.get_attribute('href')
            if name and link and "/watch" in link:
                print(f"Name: {name}\nLink: {link}\n")

        logging.info(f"Found {len(videos)} videos.")
    except TimeoutException:
        logging.error("Timeout while loading YouTube results.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")

def main(youtube_url):
    # Setup Chrome with optional headless mode
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run headlessly
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        get_name_link_youtube(driver, youtube_url)
    finally:
        driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/results?search_query=top+50+song+global"
    main(youtube_url)