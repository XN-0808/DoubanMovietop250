import requests
from requests import RequestException
import re
import json


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattren = re.compile('<li>.*?item">.*?src="(.*?)" class=""'
                         '.*?title">(.*?)</span>'
                         '.*?star">.*?average">(.*?)</span>'
                         '.*?quote">.*?inq">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattren, html)
    for item in items:
        yield {
            '海报': item[0],
            '电影名': item[1],
            '豆瓣评分': item[2],
            '最佳影评': item[3]
        }


def write_to_file(content):
    with open('豆瓣电影250.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(number):
    url = 'https://movie.douban.com/top250?start='+str(number)+'&filter='
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*25)
