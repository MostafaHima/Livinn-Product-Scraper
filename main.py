from selenium import webdriver
from website_scraper import WebsiteScraper
from product_links_scraper import ProductLinksScraper
from product_details_scraper import ProductDetailsScraper
from upload_data import ExcelExporter

# Lists to store section links
data = []

# Website URL
url = "https://www.livinn.lt/maistas"

# Setting up Chrome browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep the browser open after the script finishes
driver = webdriver.Chrome(options=chrome_options)  # Create a browser object

try:
    print("🚀 Starting website scraping process...")
    # Create an instance of the WebsiteScraper class
    scraper = WebsiteScraper(url=url, driver=driver)

    # Load the website and handle pop-up windows
    print("🌐 Loading the website...")
    scraper.section_links()

    print("\n🔗 Extracted section links:")
    links = scraper.sections_url
    print(links)

    # Print a separator line
    print("-" * 50)

    # Process each section
    for index, link in enumerate(links):
        print(f"📂 Starting scraping for section {index + 1}: {link}")

        # Extract product links in the section
        product_scraper = ProductLinksScraper(url=link, driver=driver)
        products_links = product_scraper.extract_product_links()

        print(f"🔍 Found {len(products_links)} product links in section {index + 1}.")

        # Extract product details
        scraper = ProductDetailsScraper(driver, products_links)
        scraped_data = scraper.scrape_product_details()

        print(f"✅ Finished scraping details for section {index + 1}.")
        scraper.display_summary()

        # Add the scraped data to the list
        data.append(scraped_data)

        print(f"\n🔹 Section {index + 1} data:")
        print("-" * 50)

    print("🎉 All sections scraped successfully!")
    print("\n📊 Preparing to export data to Excel...")

    print("---------------------------------------------------------------------------------------\n")
    # Export data to Excel
    file_name = "LivinnProductsData.xlsx"
    exporter = ExcelExporter(file_name, data)
    exporter.create_sheets()
    exporter.save_file()

    print("💾 Data export completed. Check the file:", file_name)
    print("-------------------------------------------------------------------------------------------\n")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    # Close the browser after the process is complete
    driver.quit()
    print("🛑 Browser closed.")
