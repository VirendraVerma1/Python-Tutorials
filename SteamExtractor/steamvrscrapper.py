from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# cd C:\Users\HP\AppData\Local\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"

# Read the Excel file to get the URLs
df = pd.read_excel('vginsights3.xlsx')
urls = df['App detail'].tolist()

# Specify Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Path to the ChromeDriver
chrome_driver_path = "D:\\Programs\\Python_private\\SeleniumBots\\chromedriver.exe"

# Initialize the Chrome WebDriver with the specified options
driver=webdriver.Chrome()


# DataFrame to hold the extracted information
extracted_data = {
    "Active Players": [],
    "24h Peak": [],
    "Positive Reviews": [],
    "Gross Revenue": [],
    "Units Sold": [],
    "Average Play Time": [],
    "Median Play Time": []
}

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    quick_stats = soup.find_all('div', class_='flex items-center gap-1')

    
        # Initialize default values for each field
    data = {
            "Active Players": '0',
            "24h Peak": '0',
            "Positive Reviews": '0',
            "Gross Revenue": '0',
            "Units Sold": '0',
            "Average Play Time": '0',
            "Median Play Time": '0'
        }
    try:
        for stat in quick_stats:
            h2 = stat.find('h2')
            div = stat.find('div')
            if h2 and div:
                h2_text = h2.get_text(strip=True)
                div_text = div.get_text(strip=True).lower()

                if 'active players' in div_text and ('ago' in div_text or 'peak' in div_text):
                    key = "24h Peak" if 'peak' in div_text else "Active Players"
                    data[key] = h2_text
                elif 'positive reviews' in div_text:
                    data["Positive Reviews"] = h2_text
                elif 'gross revenue' in div_text:
                    data["Gross Revenue"] = h2_text
                elif 'units sold' in div_text:
                    data["Units Sold"] = h2_text
                elif 'avg play time' in div_text:
                    data["Average Play Time"] = h2_text
                elif 'median play time' in div_text:
                    data["Median Play Time"] = h2_text
                data["Average Play Time"]=soup.find_all("div",{"class":"flex items-center gap-1 ng-star-inserted"})[0].find('h2').text
                data["Median Play Time"]=soup.find_all("div",{"class":"flex items-center gap-1 ng-star-inserted"})[1].find('h2').text

        # Append the extracted data to the lists in the extracted_data dict
        
    except:
        pass
    for key in data:
        extracted_data[key].append(data[key])
    print(extracted_data)

    


# Navigate to each URL and extract the information
for url in urls:
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    html = driver.page_source
    time.sleep(2)
    extract_info(html)

# Close the Selenium WebDriver
driver.quit()

# Update the DataFrame with the extracted information
for key, values in extracted_data.items():
    df[key] = pd.Series(values)

# Save the updated DataFrame to an Excel file
df.to_excel('vginsights_updated.xlsx', index=False)
