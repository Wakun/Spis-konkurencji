import requests
from bs4 import BeautifulSoup
import re

temp = []

url = "http://www.euro.com.pl/telewizory-led-lcd-plazmowe,strona-1.bhtml"
source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, "html.parser")

for item in soup.find_all(re.compile(r'^(h2|span)$'), {'class': re.compile(r'^(product-name|attribute-value)$')}):
    temp.extend(item.strings)

temp2 = [x.encode('utf-8') for x in temp]

with open('test params.txt', 'w') as t:
    for i in temp2:
        t.write(i)

t.close()

