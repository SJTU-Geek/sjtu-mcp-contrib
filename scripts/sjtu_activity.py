
METADATA = {
    "name": "sjtu_activity",
    "version": "1.0.0",
    "author": "UNIkeEN, Teruteru",
    "description": "获取交大“第二课堂”的最新活动",
    "category": "activity",
    "require_auth": True,
    "tools": [
        {
            "name": "sjtu_activity",
            "description": "Get the latest activities of SJTU's \"Second Classroom\".",
            "entryPoint": "tool_sjtu_activity",
            "schema": {
                "title": "sjtu_activity",
                "description": "Get the latest activities of SJTU's \"Second Classroom\".",
                "type": "object",
                "properties": {
                }
            }
	    }
    ]
}

import requests
from typing import List, Dict, Any, Optional
from urllib import parse
import base64
from scripts.base.mcp_context import get_http_session

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def getJaccountOIDCToken(sess: requests.Session)->Dict[str, str]:
    req1 = sess.get('https://jaccount.sjtu.edu.cn/oauth2/authorize', params={
                            'client_id': "NMCTdJI6Tluw2SSTe6tW",
                            'redirect_uri': 'https://activity.sjtu.edu.cn/auth',
                            'response_type': 'code',
                            'scope': 'profile',
                        }, headers=HEADERS, verify=False)
    code = parse.parse_qs(parse.urlparse(req1.url).query)['code'][0]
    req2 = sess.get('https://activity.sjtu.edu.cn/api/v1/login/token', params={'code':code}, headers=HEADERS, verify=False)
    token = req2.json()['data']
    return {'Authorization': 'Bearer '+token}

def getActivityTypes(sess: requests.Session)->Optional[Dict[str, Any]]:
    headers = getJaccountOIDCToken(sess)
    return sess.get(
        url='https://activity.sjtu.edu.cn/api/v1/system/activity_type',
        params={'isAll': 'true'}, 
        headers=headers
    ).json()["data"]
    
def getHotActivities(sess: requests.Session, type_id: int = 1)->Optional[Dict[str, Any]]:
    headers = getJaccountOIDCToken(sess)
    return sess.get(
        url='https://activity.sjtu.edu.cn/api/v1/hot/list', 
        params={
            'activity_type_id': type_id,
            'fill': '1',
        }, 
        headers=headers, 
        verify=False
    ).json()["data"]
    
def getAllActivities(sess: requests.Session, 
                     type_id: int = 1, page: int = 1, page_size: int = 9)->Optional[Dict[str, Any]]:
    headers = getJaccountOIDCToken(sess)
    resp = sess.get(
        url='https://activity.sjtu.edu.cn/api/v1/activity/list/home', 
        params={
            'page': page, ## 可翻页
            'per_page': page_size, 
            'activity_type_id': type_id,
            'time_sort': 'desc',
            # 'can_apply': 'true',
        }, 
        headers=headers, 
        verify=False
    ).json()["data"]
    return sorted(resp, key=lambda x: x['activity_time'][0], reverse=True)

def actIdToUrlParam(activityId:int) -> str:
    idStr = str(activityId)
    idStr = idStr + ' ' * ((3 - len(idStr)%3) % 3)
    return base64.b64encode(idStr.encode('utf-8')).decode('utf-8')

def getSignUpMethodDesc(method: int):
    match (method):
        case 1:
            return "线上报名（审核录取）";
        case 2:
            return "线下报名";
        case 3:
            return "线上报名（先到先得）";
        case 4:
            return "无需报名";
        case 5:
            return "线上报名（随机录取）";
        case 6:
            return "跳转其他报名";
        case _:
            raise Exception("no this method");

def get_activity_info_nl(activity: dict[str, Any]):
    res = \
    f"- [{activity['name']}]({'https://activity.sjtu.edu.cn/activity/detail/' + actIdToUrlParam(activity['id'])})" + "\n" + \
    f"  ![]({'https://activity.sjtu.edu.cn' + activity['img']})" + "\n" + \
    f"  主办方：{activity['sponsor']}" + "\n" + \
    (f"  报名人数：{activity['signed_up_num']} / {activity['person_num']}\n" if activity['person_num'] else "") + \
    f"  报名方式：{getSignUpMethodDesc(activity['method'])}" + "\n" + \
    (f"  报名时间：{activity['registration_time'][0]} ~ {activity['registration_time'][1]}\n" if activity['registration_time'][0] else "") + \
    f"  活动地点：{activity['address']}" + "\n" + \
    f"  活动时间：{activity['activity_time'][0]} ~ {activity['activity_time'][1]}"
    return res

def tool_sjtu_activity():
    sess = get_http_session()
    result = getAllActivities(sess, 2, 1, 15);
    return '\n\n'.join(
        [get_activity_info_nl(item) for item in result]
    )

if __name__ == "__main__":
    print(tool_sjtu_activity())