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
    rs.encoding = 'uft-8'
    return rs

def get_req(url,params=None,headers=None,cookies=None):
    s=requests.session()
    rs = s.get(url, params=params, headers=headers, cookies=cookies)
    rs.encoding = 'uft-8'
    return rs

def get_cookie_from_str(cookie_str):
    val_list = cookie_str.split(';')
    d = {}

    for curr in val_list:
        key_val = curr.split("=")
        d[key_val[0]] = key_val[1]

    return d


def parse_header_and_cookie(headers_str):
    header_list = headers_str.splitlines()

    headers = {}
    cookie = {}

    for curr in header_list:
        key_val = curr.split(':')
        if len(key_val) == 1:
            continue

        if key_val[0] == 'Cookie':
            cookie = get_cookie_from_str(key_val[1])
        else:
            headers[key_val[0]] = key_val[1].strip()
    return headers,cookie

