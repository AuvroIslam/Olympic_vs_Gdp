from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Define the columns for the CSV
COLUMNS = ["Venue", "Country", "Gold", "Silver", "Bronze", "Total", "Image URL"]

# Hardcoded list of venues
VENUES = [
    "paris-2024",

    "tokyo-2020", 

    "rio-2016",
      
    "london-2012",
    
    "beijing-2008",
    
    "athens-2004",
   
    "sydney-2000",
]

# Function to fetch medal data for a single venue
def fetch_medal_data_for_venue(driver, venue):
    url = f"https://www.olympics.com/en/olympic-games/{venue}/medals"
    driver.get(url)
    
    # Wait for the medals table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-cy='table-content']"))
    )
    
    # Find the table content
    element = driver.find_element(By.XPATH, "//div[@data-cy='table-content']")
    
    # Extract image URLs
    image_urls = [
        image.find_element(By.CSS_SELECTOR, "source").get_attribute("srcset").split(", ")[0].split(" ")[0]
        for image in element.find_elements(By.CSS_SELECTOR, "div[data-row-id] picture")
    ]
    
    # Extract text and group the data
    grouped_data = [
        [venue] + lines + [image_urls[idx]]  # Prepend venue name to each row
        for idx, lines in enumerate(
            [line.strip() for line in element.text.splitlines() if line.strip()][i:i+5]
            for i in range(0, len(element.text.splitlines()), 5)
        )
    ]
    return grouped_data

# Main function
def main():
    driver = webdriver.Chrome()
    all_data = []  # To store data for all venues
    
    for venue in VENUES:
        try:
            print(f"Fetching data for {venue}...")
            venue_data = fetch_medal_data_for_venue(driver, venue)
            all_data.extend(venue_data)  # Add the venue's data to the global list
        except Exception as e:
            print(f"Error fetching data for {venue}: {e}")
    
    driver.quit()
    
    # Save all data to a single CSV
    df = pd.DataFrame(all_data, columns=COLUMNS)
    df.to_csv("Olympic_medals.csv", index=False)

if __name__ == "__main__":
    main()
