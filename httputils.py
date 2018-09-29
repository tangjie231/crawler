import requests
from http.cookiejar import LWPCookieJar

def build_new_cookie():
    cookie_file = 'cookie.txt'
    cookie_obj = LWPCookieJar(filename=cookie_file)
    return cookie_obj

def save_cookie_2_file(cookie_obj):
    cookie_obj.save(ignore_expires=True, ignore_discard=True)

def load_cookie_from_file():
    cookie_file = 'cookie.txt'
    cookie_obj = LWPCookieJar()
    cookie_obj.load(cookie_file)
    return cookie_obj

def print_cookie_vals(cookie_obj):
    for cookie in cookie_obj:
        print('key:', cookie.name)
        print('value', cookie.value)

def post_req(url,data=None,headers=None,cookies=None):
    s=requests.session()
    rs = s.post(url, data=data, headers=headers, cookies=cookies)
    return rs

def get_req(url):
    s=requests.session()
    rs = s.get(url)
    return rs