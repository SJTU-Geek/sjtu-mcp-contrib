
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
                    "page": {
                        "description": "Activitiy list page index (default is 1)",
                        "type": "integer"
                    },
                },
                "required": [
                ]
            }
	    },
        {
            "name": "sjtu_activity_signup",
            "description": "Sign up for an activity of SJTU's \"Second Classroom\".",
            "entryPoint": "tool_sjtu_activity_signup",
            "schema": {
                "title": "sjtu_activity_signup",
                "description": "Sign up for an activity of SJTU's \"Second Classroom\".",
                "type": "object",
                "properties": {
                    "id": {
                        "description": "Activity id",
                        "type": "integer"
                    },
                    "additional_info": {
                        "description": "When the initial signing-up fails, additional information may be required from the user, in JSON dictionary format. Please use property name given by previous message (Most likely a Chinese name).",
                        "type": "string"
                    }
                },
                "required": [
                    "id",
                ]
            }
	    }
    ]
}

import requests
from typing import List, Dict, Any, Optional
from urllib import parse
import base64
from scripts.base.mcp_context import get_http_session, NETWORK_DEBUG

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

def getJaccountOIDCToken(sess: requests.Session) -> str:
    req1 = sess.get('https://jaccount.sjtu.edu.cn/oauth2/authorize', params={
                            'client_id': "NMCTdJI6Tluw2SSTe6tW",
                            'redirect_uri': 'https://activity.sjtu.edu.cn/auth',
                            'response_type': 'code',
                            'scope': 'profile',
                        }, headers=HEADERS, verify=not NETWORK_DEBUG)
    code = parse.parse_qs(parse.urlparse(req1.url).query)['code'][0]
    req2 = sess.get('https://activity.sjtu.edu.cn/api/v1/login/token', params={'code':code}, headers=HEADERS, verify=not NETWORK_DEBUG)
    token = req2.json()['data']
    return token

def getActivityTypes(token: str)->Optional[Dict[str, Any]]:
    return requests.get(
        url='https://activity.sjtu.edu.cn/api/v1/system/activity_type',
        params={'isAll': 'true'}, 
        headers={'Authorization': 'Bearer ' + token},
        verify=not NETWORK_DEBUG
    ).json()["data"]
    
def getHotActivities(token: str, type_id: int = 1)->Optional[Dict[str, Any]]:
    return requests.get(
        url='https://activity.sjtu.edu.cn/api/v1/hot/list', 
        params={
            'activity_type_id': type_id,
            'fill': '1',
        }, 
        headers={'Authorization': 'Bearer ' + token}, 
        verify=not NETWORK_DEBUG
    ).json()["data"]
    
def getAllActivities(token: str, 
                     type_id: int = 1, page: int = 1, page_size: int = 9)->Optional[Dict[str, Any]]:
    resp = requests.get(
        url='https://activity.sjtu.edu.cn/api/v1/activity/list/home', 
        params={
            'page': page, ## 可翻页
            'per_page': page_size, 
            'activity_type_id': type_id,
            'time_sort': 'desc',
            # 'can_apply': 'true',
        }, 
        headers={'Authorization': 'Bearer ' + token}, 
        verify=not NETWORK_DEBUG
    )
    return sorted(resp.json()["data"], key=lambda x: x['activity_time'][0], reverse=True)

def getSingleActivity(token: str, id: int):
    resp = requests.get(
        url=f'https://activity.sjtu.edu.cn/api/v1/activity/{id}', 
        headers={'Authorization': 'Bearer ' + token}, 
        verify=not NETWORK_DEBUG
    )
    return resp.json()["data"]

def getProfile(token: str):
    resp = requests.get(
        url=f'https://activity.sjtu.edu.cn/api/v1/profile', 
        headers={'Authorization': 'Bearer ' + token}, 
        verify=not NETWORK_DEBUG
    )
    return resp.json()["data"]

def doSignUp(token, form_submit):
    resp = requests.post(
        url=f'https://activity.sjtu.edu.cn/api/v1/signUp',
        json=form_submit,
        headers={'Authorization': 'Bearer ' + token}, 
        verify=not NETWORK_DEBUG
    )
    resp.raise_for_status()
    return resp.json()

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
    f"  id:{activity['id']}" + "\n" + \
    f"  主办方：{activity['sponsor']}" + "\n" + \
    (f"  报名人数：{activity['signed_up_num']} / {activity['person_num']}\n" if activity['person_num'] else "") + \
    f"  报名方式：{getSignUpMethodDesc(activity['method'])}" + "\n" + \
    (f"  报名时间：{activity['registration_time'][0]} ~ {activity['registration_time'][1]}\n" if activity['registration_time'][0] else "") + \
    f"  活动地点：{activity['address']}" + "\n" + \
    f"  活动时间：{activity['activity_time'][0]} ~ {activity['activity_time'][1]}"
    return res

def render_undetermined_form(form: dict[str, any]):
    if (form['tag'] == 'ElInput'):
        return f"- {form['label']}（类型：短文本）"
    elif (form['tag'] == 'textarea'):
        return f"- {form['label']}（类型：长文本）"
    elif (form['tag'] == 'Selector'):
        options = ','.join([("\"" + item['name'] + "\"") for item in form['dict']])
        return f"- {form['label']}（类型：单选；可选项：{options}）"
    elif (form['tag'] == 'RadioGroup'):
        options = ','.join([("\"" + item['name'] + "\"") for item in form['dict']])
        return f"- {form['label']}（类型：单选；可选项：{options}）"
    elif (form['tag'] == 'CheckboxGroup'):
        options = ','.join([("\"" + item['name'] + "\"") for item in form['dict']])
        return f"- {form['label']}（类型：多选；可选项：{options}）"
    elif (form['tag'] == 'file'):
        return f"- {form['label']}（类型：附件；助手无法处理，请用户手动报名）"
    elif (form['tag'] == 'img'):
        return f"- {form['label']}（类型：图片；助手无法处理，请用户手动报名）"
    
def tool_sjtu_activity(page: int = 1):
    sess = get_http_session()
    token = getJaccountOIDCToken(sess)
    result = getAllActivities(token, 2, page, 10)
    return '\n\n'.join(
        [get_activity_info_nl(item) for item in result]
    )

def tool_sjtu_activity_signup(id: int, additional_info: str = "{}"):
    sess = get_http_session()
    token = getJaccountOIDCToken(sess)
    profile = getProfile(token)
    if (not profile):
        return False, "授权失败"
    activity = getSingleActivity(token, id)
    if (activity == False):
        return False, "找不到活动"
    if (activity['in_signed_up'] == True):
        return True, "已经报名，无需重复报名"
    form_infos = activity['sign_up_info']['form_design']
    form_submit = {"id":id,"college":profile['topOrganizeId'],"form_value":{}}
    if (form_infos):
        from scripts.account_info import get_account_info
        from types_linq import Enumerable
        import json
        account_info = get_account_info()
        identity = Enumerable(account_info.entities[0].identities) \
            .first(lambda x: x.is_default)
        additional_forminfos = json.loads(additional_info)
        undetermined_forms = []
        for form_info in form_infos:
            if ("手机" in str(form_info['label'])):
                form_submit['form_value'][form_info['id']] = account_info.entities[0].mobile
            elif ("邮箱" in str(form_info['label'])):
                form_submit['form_value'][form_info['id']] = account_info.entities[0].email
            elif ("身份证" in str(form_info['label'])):
                form_submit['form_value'][form_info['id']] = account_info.entities[0].card_no
            elif ("学院" in str(form_info['label'])):
                form_submit['form_value'][form_info['id']] = identity.organize.name
            elif ("专业" in str(form_info['label'])):
                form_submit['form_value'][form_info['id']] = identity.major.name
            elif (str(form_info['label']) in additional_forminfos):
                form_submit['form_value'][form_info['id']] = additional_forminfos[str(form_info['label'])]
            else:
                undetermined_forms.append(form_info)
        if (len(undetermined_forms) > 0):
            forms_rendered = '\n'.join(
                [render_undetermined_form(form) for form in undetermined_forms]
            )
            return False, f"报名未完成，还需要补充以下信息：\n{forms_rendered}"
    submit_res = doSignUp(token, form_submit)
    if (submit_res['code'] == 200):
        return True, (submit_res['message'] if submit_res['message'] else "报名成功")
    else:
        return False, (submit_res['message'] if submit_res['message'] else "报名失败")