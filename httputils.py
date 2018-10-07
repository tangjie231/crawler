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


def post_req(url, data=None, headers=None, cookies=None, session=None):
    if session is None:
        session = requests.session()
        rs = session.post(url, data=data, headers=headers, cookies=cookies)
    else:
        rs = session.post(url, data=data)

    rs.encoding = 'uft-8'
    return rs


def get_req(url, params=None, headers=None, cookies=None, session=None):
    if session is None:
        session = requests.session()
        rs = session.get(url, params=params, headers=headers, cookies=cookies)
    else:
        rs = session.get(url)

    rs.encoding = 'uft-8'
    return rs


def create_new_session():
    return requests.session()


def get_cookie_from_str(cookie_str):
    val_list = cookie_str.split(';')
    d = {}

    for curr in val_list:
        key_val = curr.split("=")
        d[key_val[0]] = key_val[1]

    return d


def parse_header(headers_str):
    header_list = headers_str.splitlines()

    headers = {}

    for curr in header_list:
        key_val = curr.split(':')
        if len(key_val) == 1:
            continue

        header_key = key_val[0].strip()
        header_val = key_val[1].strip()
        headers[header_key] = header_val

    return headers
