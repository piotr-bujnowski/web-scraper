import requests
from bs4 import BeautifulSoup


def format_file_name(name):
    return name.replace(" ", '_').translate(str.maketrans('', '', "!\"#$%&'()*+,-./:;<=>?@[\\]^`{|}~")).strip()


print("Input the URL:")
headers = {'Accept-Language': 'en-US,en;q=0.5'}
req = requests.get("https://www.nature.com/nature/articles", headers=headers, params={"type": "news"})
soup = BeautifulSoup(req.content, "html.parser")
print(req.url)
print()

if req.status_code == 200:
    articles = soup.find_all('article')

    # Iterating through articles and requesting from their href then saving body to .txt
    for article in articles:
        if article.find('a').get('data-track-action') == "view article":
            print("Getting article: " + "https://www.nature.com" + article.find('a').get('href'))
            req_article = requests.get("https://www.nature.com" + article.find('a').get('href'), headers=headers)
            article_soup = BeautifulSoup(req_article.content, "html.parser")

            print("Writing article content to txt file...")
            article_file = open(format_file_name(article.find('a').text) + ".txt", "wb")
            article_file.write(bytes(article_soup.find('div', {"class": "article__body"}).text.strip().encode("utf-8")))
            article_file.close()
            print()

    print("All articles have been saved! :)")
else:
    print("The URL returned " + str(req.status_code) + "!")
