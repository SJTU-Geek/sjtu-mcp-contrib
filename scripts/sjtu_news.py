
METADATA = {
    "name": "sjtu_news",
    "version": "1.0.0",
    "author": "UNIkeEN, Teruteru",
    "description": "获取交大新闻网的新闻",
    "tools": [
        {
            "name": "sjtu_news",
            "description": "Fetch news from the SJTU's news portal.",
            "entryPoint": "tool_sjtu_news",
            "schema": {
                "title": "sjtu_news",
                "description": "Fetch news from the SJTU's news portal.",
                "type": "object",
                "properties": {
                }
            }
	    }
    ]
}

from typing import Any, Dict, List, Tuple
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def getSjtuNews() -> Tuple[bool, List[Dict[str, Any]]]:
    """交大新闻网"""
    pageUrl = 'https://news.sjtu.edu.cn/jdyw/index.html'
    req = requests.get(pageUrl)
    if req.status_code != requests.codes.ok:
        return False, "获取信息失败，请检查网络连接"
    html = req.text
    html = BeautifulSoup(html, 'lxml')
    news = html.find('div', class_='list-card-h').find_all('li', class_='item')
    result = []
    for n in news:
        card = n.find('a', class_='card')
        try:
            link =  card.get('href')
            link = urljoin(pageUrl, link)
        except:
            link = None
        try:
            imgLink = card.find('img').get('src')
            imgLink = urljoin(pageUrl, imgLink)
        except:
            imgLink = None
        try:
            title = card.find('p', class_='dot').contents[0]
        except:
            title = None
        try:
            detail = card.find('div', class_='des dot').contents[0]
        except:
            detail = None
        about = card.find('div', class_='time')
        try:
            time = about.find('span').contents[0]
        except:
            time = None
        try:
            source = about.find('div', class_='source').p.contents[0]
        except:
            source = None
        result.append({
            'title': title,
            'link': link,
            'imgLink': imgLink,
            'detail': detail,
            'time': time,
            'source': source
        })
    return True, result

def tool_sjtu_news():
    success, result = getSjtuNews()
    if (not success):
        return result
    else:
        return '\n\n'.join(
            [f"- [{item['title']}]({item['link']})\n{item['detail']}\n{item['time']} 来自于 {item['source']}" for item in result]
        )
        
if __name__ == "__main__":
    print(tool_sjtu_news())