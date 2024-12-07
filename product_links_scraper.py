import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ProductLinksScraper:
    """
    Class for scraping product links from a given website.
    """

    def __init__(self, url, driver):
        """
        Initialize the scraper with the website URL and Selenium WebDriver.
        """
        self.url = url  # The website URL to visit
        self.driver = driver  # Selenium WebDriver instance
        self.wait = WebDriverWait(self.driver, 15)  # Maximum wait time for page elements
        self.raw_links = []  # List to store raw links
        self.final_links = []  # List to store cleaned links

    def extract_product_links(self):
        """
        Load the website and scrape all product links.
        """
        try:
            # Open the website
            self.driver.get(self.url)

            # Wait until the page is fully loaded
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Website loaded successfully.")

            while True:
                time.sleep(1)  # Small delay between actions to improve stability

                try:
                    # Locate the "More" button using a relative XPath
                    more_button = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='website-content']/div/div[2]/div[2]/div/div[3]/div/button")
                    ))

                    # Scroll to the button using JavaScript
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                               more_button)
                    time.sleep(1)  # Small delay before clicking

                    # Click the button
                    more_button.click()
                    time.sleep(2)  # Additional delay after clicking
                    print("🖱️ Clicked 'More' button successfully.")

                except Exception as e:
                    print("⚠️ No 'More' button found or all products loaded.")
                    break  # Exit the loop if an error occurs or the button is not found

                try:
                    # Locate all products in the grid
                    product_grid = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item-grid")))
                    self.raw_links = product_grid.find_elements(By.CSS_SELECTOR, ".image a")

                    # Get the current product count
                    product_count_text = self.driver.find_element(By.XPATH,
                                                                  "//*[@id='website-content']/div/div[2]/div[2]/div/div[3]/div/div/span").text
                    total_products = int(product_count_text.split(" ")[-1])

                    print(f"🔗 Collected {len(self.raw_links)} out of {total_products} products.")

                    # Check if all links have been collected
                    if len(self.raw_links) == total_products:
                        print("✅ All products have been successfully scraped.")
                        break

                except Exception as e:
                    print(f"⚠️ Error while retrieving product links: {e}")
                    break

        except Exception as e:
            print(f"❌ Failed to load the website: {e}")

        # Clean the links after completion
        self.clean_links()
        return self.final_links

    def clean_links(self):
        """
        Clean the raw links and prepare them for use.
        """
        print("🛠️ Starting link cleaning process...")
        for link in self.raw_links:
            clean_link = link.get_attribute("href")
            if clean_link not in self.final_links:  # Check for duplicate links
                self.final_links.append(clean_link)
        print("✅ Link cleaning completed.")
        print(self.final_links)






