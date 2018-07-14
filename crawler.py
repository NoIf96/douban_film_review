# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import time

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }

proxies = {
    'http':'106.46.136.112:808',
}

def get_one_movie_comments(url):
    print("开始爬取")
    try:
        resopnse = requests.get(url, headers=header, proxies=proxies).text
        soup = BeautifulSoup(resopnse, "lxml")
        title = soup.select('#content > h1')[0].string
        print(title)
        comments = soup.select('#comments > div > div.comment')
        comments_info = []
        for comment in comments:
            name = comment.select('h3 > span.comment-info > a')[0].string
            content = comment.p.string
            comments_info.append({'name': name, 'content': content})
        movie_comments = {
            'title': title,
            'comments': comments_info
        }
        print("爬取成功")
        return movie_comments
    except:
        print("爬取失败")
        return None

def to_one_movie_comments(movie_comments):
    file_name = '剧情短评集/' + movie_comments['title'] + '.txt'
    with open(file_name, 'a', encoding='utf-8') as f:
        for comment_info in movie_comments['comments']:
            try:
                f.write(comment_info['name'])
                f.write("\n")
                f.write(comment_info['content'])
                f.write("\n")
            except:
                continue


if __name__ == '__main__':
    url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=100'
    web_data = requests.get(url, headers=header, proxies=proxies).content
    datas_json = json.loads(web_data)
    movies_url = (data_json['url'] + 'comments?&status=P' for data_json in datas_json)
    for movie_url in movies_url:
        print(movie_url)
        movie_comments = get_one_movie_comments(movie_url)
        if movie_comments is None:
            continue
        to_one_movie_comments(movie_comments)
        time.sleep(2)

