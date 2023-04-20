# url = 'https://oldvaric1.pythonanywhere.com/news/10'
#
#
# article_id = url.split('/')[-1]
# print(article_id)
import json

with open('news_dict.json', encoding='utf-8') as file:
    news_dict = json.load(file)

search_id = '102'

if search_id in news_dict:
    print('все есть')
else:
    print("ого новое")