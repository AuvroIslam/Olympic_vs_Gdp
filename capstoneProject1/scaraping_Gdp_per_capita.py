import requests
import pandas as pd
import bs4

url = "https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projected_GDP_(nominal)_per_capita"
web_page = bs4.BeautifulSoup(requests.get(url).text, "html.parser")
tables = web_page.find_all(name="table", class_="wikitable")

def inp(row, col_name):
    details = row.text.lstrip().split("\n")
    content = {}
    for i in range(len(col_name)):
        if i >= len(details):
            content[col_name[i]] = " "
        else:
            content[col_name[i]] = details[i]
    return content

# Initialize a dictionary to hold all data
data_dict = {}

# Process each table
for i in range(1, 5):
    rows = tables[i].find_all(name="tr")
    col_name = [col.text.strip() for col in rows[0].find_all(name="th")]

    for row in rows[1:]:
        row_data = inp(row, col_name)
        country = row_data['Country (or dependent territory)']
        
        # If the country is not in the dictionary, initialize it
        if country not in data_dict:
            data_dict[country] = {year: " " for year in range(1990, 2030)}
            data_dict[country]['Country (or dependent territory)'] = country
        
        # Update the dictionary with the data from the current row
        for year in col_name[1:]:
            data_dict[country][year] = row_data[year]

# Convert the dictionary to a DataFrame
cols = ['Country (or dependent territory)'] + [str(year) for year in range(1990, 2030)]
df = pd.DataFrame.from_dict(data_dict, orient='index', columns=cols)

# Save to CSV
df.to_csv("gdp_per_capita.csv", index=False)