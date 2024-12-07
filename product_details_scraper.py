import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ProductDetailsScraper:
    """
    Class for scraping product details from given links.
    """

    def __init__(self, driver, product_links):
        """
        Initialize the scraper with a driver and a list of product links.
        """
        self.driver = driver
        self.product_links = product_links
        self.wait = WebDriverWait(self.driver, 20)
        self.product_details = []

    def scrape_product_details(self):
        """
        Scrape details for each product from the provided links.
        """

        for index, link in enumerate(self.product_links):
            self.driver.get(link)
            # Ensure the page is loaded
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            time.sleep(1)
            # Scroll down the page for loading dynamic content
            for _ in range(4):  # Scroll 5 times
                self.driver.execute_script("window.scrollBy(0, 350);")
                time.sleep(0.2)

            # Handle any popup that might appear
            try:
                close_button = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id=\"om-ot6rtcgpljz5sl6tlojl-optin\"]/div/button")))
                close_button.click()
            except Exception:
                pass

            # Initialize empty variables for product details
            image_link, title_text, brand_name, brand_url = "", "", "", ""
            quantity, price_per_quantity, price_per_kg = "", "", ""
            components, certificate, country_of_origin = "", "", ""
            abuot_product, certificate_element, information = "", "", ""
            product_code, ean_code = "", ""

            print("-------------------------------------------------------------------------------------------------\n")
            # Extract product image link
            try:
                image_element = self.driver.find_element(By.XPATH, "//*[@id=\"product-slider-main\"]/div[2]/div/img")
                image_link = image_element.get_attribute("src")
            except Exception:
                print("Image not found")

            # Extract product title
            try:

                title_element = self.driver.find_element(By.XPATH,
                                                         "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/h1")
                title_text = title_element.text
                if title_text == "":
                    self.driver.refresh()
                    title_element = self.driver.find_element(By.XPATH,
                                                             "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/h1")
                    title_text = title_element.text
            except Exception:
                print("Title not found")

            # Extract brand name and URL
            try:

                brand_element = self.driver.find_element(By.XPATH,
                                                         "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/div[2]/a")
                brand_name = brand_element.text
                brand_url = brand_element.get_attribute("href")
            except Exception:
                print("Brand name or URL not found")

            # Extract quantity
            try:

                quantity_element = self.driver.find_element(By.XPATH,
                                                            "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/div[3]")
                quantity = quantity_element.text
            except Exception:
                print("Quantity not found")

            # Extract price details
            try:

                quantity_price_element = self.driver.find_element(By.XPATH,
                                                                  "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/div[4]/div/div[1]")
                price_per_quantity = quantity_price_element.text

                price_kg_element = self.driver.find_element(By.XPATH,
                                                            "//*[@id=\"website-content\"]/div/div[2]/div[2]/div[1]/div[4]/div/div[2]")
                price_per_kg = price_kg_element.text
            except Exception:
                print("Price details not found")

            # Extract product components
            try:
                components = self.driver.find_element(By.XPATH,
                                                      ".//*[@id=\"website-content\"]/div/div[3]/div[2]/div/div/div/div[1]/div").text

            except Exception:
                print("components not found")

            try:
                certificate = self.driver.find_element(By.XPATH,
                                                       "//*[@id=\"website-content\"]/div/div[3]/div[1]/div/div[1]/div[2]").text
                certificate_element = certificate.split(":")[-1]
                abuot_product = certificate.split(":")[0]
            except Exception:
                print("certificate not found")

            try:
                # First attempt to get the first element
                information = self.driver.find_element(By.XPATH,
                                                       "//*[@id=\"website-content\"]/div/div[3]/div[1]/div/div[4]").text
            except Exception:
                try:
                    # Second attempt to get the second element
                    information = self.driver.find_element(By.XPATH,
                                                           "//*[@id=\"website-content\"]/div/div[3]/div[1]/div/div[3]").text
                except Exception:
                    # If neither element is found
                    print("Both information options not found.")

            try:
                info_list = information.split("\n")

                country_of_origin = info_list[1].strip() if len(info_list) > 1 else "N/A"
                product_code = info_list[-2].split(":")[-1].strip() if len(info_list) > 2 and ":" in info_list[
                    -2] else "N/A"
                ean_code = info_list[-1].split(":")[-1].strip() if len(info_list) > 1 and ":" in info_list[
                    -1] else "N/A"

                print(f"Country of Origin: {country_of_origin}")
                print(f"Product Code: {product_code}")
                print(f"EAN Code: {ean_code}")

            except Exception as e:
                print(f"Error extracting product details: {e}")

            # Save extracted details in a dictionary
            details_dict = {
                "Product Title": title_text,
                "Image Link": image_link,
                "Brand Name": brand_name,
                "Brand URL": brand_url,
                "Quantity": quantity,
                "Price per Quantity": price_per_quantity.split(" ")[0],
                "Price per KG": price_per_kg.split("/")[0],
                "Components": components,
                "About Product": abuot_product,
                "Certificate": certificate_element,
                "Country of Origin": country_of_origin,
                "Product Code": product_code,
                "EAN Code": ean_code
            }

            print(f"\n{index}: {details_dict}\n")

            # Append details to the list
            self.product_details.append(details_dict)
        return self.product_details

    def format_details(self, details):
        """
        Format product details into a readable format for output.
        """
        formatted_details = "\n".join([f"{key}: {value}" for key, value in details.items()])
        return formatted_details

    def display_summary(self):
        """
        Display a summary of the scraped data.
        """
        print(f"Scraping completed! Total products scraped: {len(self.product_details)}")
        for i, details in enumerate(self.product_details, 1):
            print(f"--- Product {i} ---")
            print(self.format_details(details))
            print(
                "\n-------------------------------------------------------------------------------------------------\n")





