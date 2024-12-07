import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class WebsiteScraper:
    def __init__(self, url, driver):
        self.url = url  # Website URL to be opened
        self.driver = driver  # Selenium WebDriver instance
        self.wait = WebDriverWait(self.driver, 15)  # Maximum wait time is set to 15 seconds
        self.sections_url = []  # To store links of sections found on the website

    def section_links(self):
        """
        Open the website and handle popups or cookies.
        """
        print("🚀 Opening the website...")
        self.driver.get(self.url)

        # Wait for the page body to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Page loaded successfully.")

        # Handle cookies acceptance button
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
            cookies_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookies_button.click()
            print("🍪 Cookies accepted.")
        except Exception as e:
            print(f"⚠️ Cookies button not found. Skipping... Error: {e}")

        # Handle the first popup close button
        try:
            print("⏳ Waiting for the first popup...")
            time.sleep(10)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"om-ot6rtcgpljz5sl6tlojl-optin\"]/div/button")))
            close_button = self.driver.find_element(By.XPATH, "//*[@id=\"om-ot6rtcgpljz5sl6tlojl-optin\"]/div/button")
            close_button.click()
            print("✅ First popup closed successfully.")
        except Exception as e:
            print(f"⚠️ First popup close button not found. Skipping... Error: {e}")

        # Handle the second popup close button
        try:
            print("⏳ Waiting for the second popup...")
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"om-vfqqhhm117waztbzxtba-optin\"]/div/button")))
            close2_button = self.driver.find_element(By.XPATH, "//*[@id=\"om-vfqqhhm117waztbzxtba-optin\"]/div/button")
            close2_button.click()
            print("✅ Second popup closed successfully.")
        except Exception as e:
            print(f"⚠️ Second popup close button not found. Skipping... Error: {e}")

        print("🎉 The website is ready for scraping!")
        print("-" * 100)
        self.extract_section_links()

    def extract_section_links(self):
        """
        Locate and extract links to all sections of the website.
        """
        print("🔍 Locating section links...")
        sections_container = self.driver.find_element(By.CSS_SELECTOR, ".header-bottom-menu-container")
        section_elements = sections_container.find_elements(By.CSS_SELECTOR, ".btn.btn-green.btn-round-5.btn-small a")

        print(f"📂 Number of sections found: {len(section_elements)}")
        for section in section_elements:
            section_link = section.get_attribute("href")
            self.sections_url.append(section_link)  # Add each section link to the list
            print(f"🔗 Section link added: {section_link}")

        print("✅ All section links extracted successfully!")
        return self.sections_url  # Return the list of links
