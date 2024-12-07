# Product Data Scraping Project from Livinn Website

## Overview
This project aims to scrape product data from the **Livinn** website (https://www.livinn.lt/maistas). The goal is to extract detailed information about products available on the website, such as product title, image link, brand details, price information, and more. After collecting the data, it is exported into an Excel file for further analysis or usage.

## Data Collected
The following data is extracted for each product:

- **Product Title:** The name of the product.
- **Image Link:** The URL link to the product's image.
- **Brand Name:** The brand of the product.
- **Brand URL:** The URL link to the brand’s page.
- **Quantity:** The amount or volume of the product.
- **Price per Quantity:** The price for the specified quantity of the product.
- **Price per KG:** The price per kilogram of the product.
- **Components:** A list of the product’s components or ingredients.
- **About Product:** A description or information about the product.
- **Certificate:** Any certification associated with the product.
- **Country of Origin:** The country where the product is made or sourced from.
- **Product Code:** The unique code identifying the product.
- **EAN Code:** The European Article Number code for the product.

## Project Objectives
- **Extract Product Details:** Automatically gather detailed information about each product from the Livinn website.
- **Organize Data:** Organize the extracted data in a structured manner, making it easy to analyze and review.
- **Export to Excel:** Save all collected product details into an Excel file for easy access and use.

## Features
- **Automated Data Extraction:** Uses **Selenium** to automatically extract product data from the Livinn website.
- **Handles Pop-up Windows:** The script manages pop-up windows and ensures smooth navigation through the website.
- **Excel Export:** The data is exported to an Excel file, which can be used for further analysis or report generation.

## Requirements
Before running the script, make sure you have the following dependencies installed:

- **Python 3.6 or higher**
- **Selenium** Python library:
  ```bash
  pip install selenium
  
- **openpyxl** Python library to export data to Excel:
  ```bash
  pip install openpyxl

- **Google Chrome and ChromeDriver** (ensure you are using the correct version of ChromeDriver compatible with your browser version): website (https://developer.chrome.com/docs/chromedriver/downloads)

## How to Run
 ### 1. Set Up the Environment
- Make sure **Python** is installed on your machine
-  Install the necessary libraries using **pip**:
  ```bash
  pip install requirements.txt
```
### 2. Run the Script
  ```bash
    python main.py
```
 




