import os
import time
import logging
from dotenv import load_dotenv
import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_auth_details():
    load_dotenv()
    username = os.getenv('GITHUB_USERNAME')
    password = os.getenv('GITHUB_PASSWORD')
    if not username or not password:
        raise ValueError("Missing credentials in .env")
    return username, password

def sign_in_github(github_link, browser):
    wait = WebDriverWait(browser, 10)
    username, password = get_auth_details()
    browser.get(github_link)

    try:
        sign_in_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Sign in')))
        sign_in_button.click()

        username_field = wait.until(EC.presence_of_element_located((By.ID, 'login_field')))
        password_field = browser.find_element(By.ID, 'password')

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        logging.info("Logged in successfully.")

    except TimeoutException:
        logging.error("Login page did not load correctly.")
        raise

def search_on_github(search_query, browser, actions):
    wait = WebDriverWait(browser, 10)
    try:
        expand_search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'AppHeader-search-whenNarrow')))
        expand_search_button.click()

        search_field = wait.until(EC.presence_of_element_located((By.NAME, 'query-builder-test')))
        search_field.send_keys(search_query)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        logging.info(f"Searched for: {search_query}")
    except TimeoutException:
        logging.error("Search input did not load.")
        raise

def find_url_name_from_search_results(browser, pages, ws):
    wait = WebDriverWait(browser, 10)
    for page in range(1, pages+1):
        logging.info(f"Processing page {page}")
        try:
            repo_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "search-title")]//a'))
            )
            for repo_element in repo_elements:
                name = repo_element.text
                url = repo_element.get_attribute('href')
                ws.append([name, url])

            try:
                next_button = browser.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
                next_button.click()
                time.sleep(2)
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                logging.info("No more pages available.")
                break
        except TimeoutException:
            logging.warning("Search results not found on page.")
            break
    return ws
    
def save_workbook(path, wb):
    wb.save(path)
    logging.info(f"Results saved to {path}")

def main(github_link, search_query, path, pages):
    # Chrome options for headless mode
    options = Options()
    # options.add_argument("--headless")  # Uncomment this for headless operation
    options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=options)
    actions = ActionChains(browser)

    try:
        sign_in_github(github_link, browser)
        search_on_github(search_query, browser, actions)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "GitHub Repos"
        ws.append(['Repository Name', 'URL'])

        find_url_name_from_search_results(browser, pages, ws)
        save_workbook(path, wb)

    except Exception as e:
        logging.exception("An error occurred:")
    finally:
        browser.quit()
        logging.info("Browser closed.")


if __name__ == "__main__":
    github_link = "https://github.com/"
    search_query = "machine learning"
    path = "github_repositories.xlsx"
    pages = 2
    main(github_link, search_query, path, pages)