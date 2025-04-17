# MCP Tool 的运行环境共享变量
# 定义 CONTEXT 变量方便本地调试，在运行时会被设置为真实值

import os

JAAuthCookie = os.environ.get('JAAuthCookie', "")

class MockJaCookieProvider:
    def __init__(self):
        self.cookie = JAAuthCookie
    def SetCookie(self, c: str):
        self.cookie = c
    def GetCookie(self) -> str:
        return self.cookie
    
class MockMemoryCache:
    def __init__(self):
        self.dic = {}
    def Get(self, key: any) -> any:
        return self.dic.get(key)
    def Set(self, key: any, value: any):
        self.dic[key] = value
    def Set(self, key: any, value: any, expiration: any):
        self.dic[key] = value
    
class MockContext:
    def ResolveJaCookieProvider(self):
        return MockJaCookieProvider()
    def ResolveMemoryCache(self):
        return MockMemoryCache()

CONTEXT = MockContext()
NETWORK_DEBUG = True

def get_context():
    return CONTEXT

def get_http_session():
    cookie_value = CONTEXT.ResolveJaCookieProvider().GetCookie()
    import requests
    import http.cookies
    sess = requests.session()
    cookie = http.cookies.SimpleCookie()
    cookie['JAAuthCookie'] = cookie_value
    morsel = cookie['JAAuthCookie']
    morsel["domain"] = "jaccount.sjtu.edu.cn"
    morsel["path"] = "/"
    morsel["expires"] = None
    sess.cookies.set('JAAuthCookie', morsel)
    return sess