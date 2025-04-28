METADATA = {
    "name": "sjtu_jwc",
    "version": "1.0.0",
    "author": "wortox1881",
    "description": "获取教务处面向学生的通知公告",
    "category": "info_portal",
    "require_auth": False,
    "tools": [
        {
            "name": "jwc_news",
            "description": "Fetch news from the jwc.sjtu.edu.cn.",
            "entrypoint": "tool_jwc_news",
            "schema": {
                "title": "jwc_news",
                "description": "Fetch news from the jwc.sjtu.edu.cn.",
                "type": "object",
                "properties": {
                }
            }
        }
    ]
}

import requests
from bs4 import BeautifulSoup
from scripts.base.mcp_context import NETWORK_DEBUG
from typing import List, Dict, Any, Tuple
import urllib3
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getJwcNews() -> Tuple[bool, List[Dict[str, str]]]:
    pageUrl = 'https://jwc.sjtu.edu.cn/xwtg/tztg.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = requests.get(pageUrl, headers=headers, verify=not NETWORK_DEBUG)
    if req.status_code != requests.codes.ok:
        return False, "获取信息失败，请检查网络连接"
    
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    news_list = soup.find_all('li', class_='clearfix')
    
    result = []
    for news in news_list:
        try:
            date_div = news.find('div', class_='sj')
            day = date_div.find('h2').text.strip()
            month_year = date_div.find('p').text.strip()
            
            year, month = month_year.split('.')
            date = f"{year}年{int(month)}月{int(day)}日"
            
            title = news.find('div', class_='wz').find('h2').text.strip()
            link = news.find('div', class_='wz').find('a').get('href')
            if link.startswith('..'):
                link = 'https://jwc.sjtu.edu.cn' + link[2:]
            
            summary = news.find('div', class_='wz').find('p').text.strip()
            
            result.append({
                'date': date,
                'title': title,
                'link': link,
                'summary': summary
            })
        except Exception as e:
            continue
    
    return True, result

def tool_jwc_news():
    success, result = getJwcNews()
    if not success:
        return result
    else:
        output = '\n\n'.join(
            [f"- [{item['title']}]({item['link']})\n{item['summary']}\n{item['date']}" for item in result]
        )
        return output

if __name__ == "__main__":
    result = tool_jwc_news()
    print(result)
