from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open LinkedIn
driver.get("https://www.linkedin.com/login")

# Log in
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("your-email@example.com")
password.send_keys("yourpassword")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

# Wait for the page to load
time.sleep(5)

# Go to UCR alumni page
driver.get("https://www.linkedin.com/school/university-of-california-riverside/people/")
time.sleep(5)

# Find the search bar or filter for data science
search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Search by title, keyword, or company']")
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)

# Function to scrape a single page
def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    alumni_profiles = soup.find_all("div", class_="entity-result__item")

    alumni_list = []
    for profile in alumni_profiles:
        name = profile.find("span", class_="entity-result__title-text").get_text(strip=True)
        headline = profile.find("div", class_="entity-result__primary-subtitle").get_text(strip=True)
        location = profile.find("div", class_="entity-result__secondary-subtitle").get_text(strip=True)

        alumni_list.append({
            "Name": name,
            "Headline": headline,
            "Location": location
        })
    return alumni_list

# Main scraping loop with pagination handling
alumni_data = []
while True:
    alumni_data.extend(scrape_page(driver))

    # Check if there's a next page button
    try:
        next_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next')]")
        next_button.click()
        time.sleep(5)  # Adjust the sleep time as needed
    except:
        break  # Exit loop if no more pages

# Save data to a CSV file
df = pd.DataFrame(alumni_data)
df.to_csv("ucr_data_science_alumni.csv", index=False)

# Close the driver
driver.quit()
