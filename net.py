# 浏览器请求
import json

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://play.kawaii.global',
    'referer': 'https://play.kawaii.global/',
    'x-playfabsdk': 'UnitySDK-2.113.210830',
}


def post(url, data):
    response = requests.post(url=url, data=data, headers=headers)
    return response


def options(url):
    response = requests.options(url=url, headers=headers)
    return response

