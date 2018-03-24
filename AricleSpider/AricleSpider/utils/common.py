# -*- coding:UTF-8 -*-
import hashlib


def get_md5(url):
    # 判断是否是UNcode编码，如果是python3就需要编码成utf8
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    # Python3将所有的字符编码为UNcode
    print(get_md5('http://jobbole.com/'.encode('utf-8')))



