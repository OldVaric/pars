import json

import requests
from bs4 import BeautifulSoup

def get_first_news():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 111.0.0.0Safari / 537.36OPR / 97.0.0.0(EditionYxGX)'
    }

    url = 'https://oldvaric1.pythonanywhere.com/news/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='alert alert-warning')

    news_dict = {}
    for article in articles_cards:
        article_title = article.find('h3').text.strip()
        article_desc = article.find('p').text.strip()
        article_u = article.find('a')['href']
        article_url = f'https://oldvaric1.pythonanywhere.com{article_u}'

        article_id = article_url.split('/')[-1]

        # print(f"{article_title} | {article_url}")

        news_dict[article_id] = {
            'article_title': article_title,
            'article_url': article_url,
            'article_desc': article_desc
        }

    with open('news_dict.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_up():
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 111.0.0.0Safari / 537.36OPR / 97.0.0.0(EditionYxGX)'
    }

    url = 'https://oldvaric1.pythonanywhere.com/news/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='alert alert-warning')

    fresh_news = {}
    for article in articles_cards:
        article_u = article.find('a')['href']
        article_url = f'https://oldvaric1.pythonanywhere.com{article_u}'
        article_id = article_url.split('/')[-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('h3').text.strip()
            article_desc = article.find('p').text.strip()

            news_dict[article_id] = {
                'article_title': article_title,
                'article_url': article_url,
                'article_desc': article_desc
            }

            fresh_news[article_id] = {
                'article_title': article_title,
                'article_url': article_url,
                'article_desc': article_desc
            }

    with open('news_dict.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    print(check_news_up())


if __name__ == '__main__':
    main()