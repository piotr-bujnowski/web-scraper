import requests
from bs4 import BeautifulSoup

print("Input the URL:")
headers = {'Accept-Language': 'en-US,en;q=0.5'}
req = requests.get(input("> "), headers=headers)
soup = BeautifulSoup(req.content, "html.parser")
print()
movies = {}

try:
    movies["title"] = soup.find("h1").text
    movies["description"] = soup.find("div", {"class": "summary_text"}).text.strip()
    print(movies)
except (ValueError, Exception):
    print("Invalid movie page!")
