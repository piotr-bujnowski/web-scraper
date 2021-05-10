import requests
import os
from bs4 import BeautifulSoup

headers = {'Accept-Language': 'en-US,en;q=0.5'}


def format_file_name(name):
    return name.replace(" ", '_').translate(str.maketrans('', '', "!\"#$%&'()*+,-./:;<=>?@[\\]^`{|}~")).strip()


def write_to_file(article_name_, article_soup_):
    article_file = open(format_file_name(f"{article_name_}.txt"), "wb")
    article_file.write(bytes(article_soup_.find('div', {"class": ["article-item__body", "article__body"]}).text.strip().encode("utf-8")))
    article_file.close()


def change_page(page_count_):
    params = {"page": str(page_count_)}
    return requests.get("https://www.nature.com/nature/articles", headers=headers, params=params)


page_num = int(input("Number of pages you want to scrape\n> "))
topic = input("What topic do you want to look for?\n> ")
req = requests.get("https://www.nature.com/nature/articles", headers=headers)
soup = BeautifulSoup(req.content, "html.parser")
print(req.url)
print()


if req.status_code == 200:
    page_count = 1
    total_num_articles_site = 0

    for p in range(1, page_num + 1):
        article_count_page = 0
        new_page_dir_name = "Page_" + str(page_count)

        if not os.path.exists(new_page_dir_name):
            os.mkdir(new_page_dir_name)
        os.chdir(new_page_dir_name)
        if not os.path.exists(topic):
            os.mkdir(topic)
        os.chdir(topic)

        articles = soup.find_all('article')

        print(f"Checking Page {page_count}")
        print(req.url)

        for i in range(0, 20):
            if articles[i].find('span', {'data-test': 'article.type'}).text.lower().strip() == topic.lower():
                print("-> Getting article: " + "https://www.nature.com" + articles[i].find('a').get('href'))

                req_article = requests.get("https://www.nature.com" + articles[i].find('a').get('href'), headers={'Accept-Language': 'en-US,en;q=0.5'})
                article_soup = BeautifulSoup(req_article.content, "html.parser")

                article_name = format_file_name(articles[i].find('a').text)
                print(f"--Writing {article_name} into file...")

                if article_soup.find('div', {"class": ["article-item__body", "article__body"]}):
                    write_to_file(article_name, article_soup)

                article_count_page += 1

        print(f"Total num of articles found on page {page_count}: {article_count_page}")
        print()

        page_count += 1
        total_num_articles_site += article_count_page

        req = change_page(page_count)
        soup = BeautifulSoup(req.content, "html.parser")

        os.chdir("../../")

    print("All articles have been saved! :)")
    print(f"Total num of articles: {total_num_articles_site}")
else:
    print("The URL returned " + str(req.status_code) + "!")
