# importing the libraries
from bs4 import BeautifulSoup
import csv
import requests

f = csv.writer(open('dpr.csv', 'w'))
f.writerow(['Nama'])

url="http://www.dpr.go.id/anggota"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, 'html.parser')

for row in soup.findAll('table')[0].tbody.findAll('tr'):
    third_column = row.findAll('td')[2].contents
    #print (third_column)
    f.writerow(third_column)

