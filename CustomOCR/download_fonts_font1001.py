from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", '/path/to/download/directory')
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

driver = webdriver.Firefox(options=options)

for i in range(1, 3152):
    url = f"https://www.1001fonts.com/?page={i}"
    driver.get(url)
    time.sleep(10)  # wait for the page to load
    j=0
    try:
        download_buttons = driver.find_elements(By.XPATH, "//a[@class='btn btn-success'][starts-with(@href, '/download/')]")
        print(len(download_buttons))
        for button in download_buttons:
            button.click()
            j=j+1
            print(j)
            time.sleep(1)  # wait for the download to start
    except Exception as e:
        print(f"Failed to download on page {i}: {e}")

driver.quit()
