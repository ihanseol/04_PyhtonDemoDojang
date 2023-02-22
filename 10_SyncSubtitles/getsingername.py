import requests
from bs4 import BeautifulSoup
import json

# specify the URL of the website to scrape
url = "http://cdb.chosun.com/search/db-people/i_service/people_Dir_search_sample2.jsp"

# send a GET request to the URL and get the response
response = requests.get(url)

# parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the table element containing the singer names
table = soup.find('table', {'class': 'table4'})

# find all the rows in the table except for the header row
rows = table.find_all('tr')[1:]

# create a list to store the singer names
singer_names = []

# iterate over the rows and extract the singer name from the second column
for row in rows:
    singer_name = row.find_all('td')[1].text.strip()
    singer_names.append(singer_name)

# create a dictionary to store the list of singer names
data = {"singer_names": singer_names}

# save the data in a JSON file
with open('singer_names.json', 'w') as file:
    json.dump(data, file)
