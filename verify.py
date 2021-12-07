# 服务器验证代码
import json
import uuid
import binascii

import requests
from pyDes import des, CBC, PAD_PKCS5
from time import sleep

import util


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def des_encrypt(secret_key, s):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_decrypt(secret_key, s):
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de


def verity(ver_ID):
    imac = get_mac_address()
    imac = des_encrypt('testtest', imac)
    imac = str(imac, encoding="utf-8")
    ver_ID = des_encrypt('testtest', str(ver_ID))
    ver_ID = str(ver_ID, encoding="utf-8")
    postBody = {"param1": imac, "param2": ver_ID}
    util.log_debug("postBody : "+str(postBody))
    r = requests.post('http://118.31.34.5:5000/kawaii/', data=json.dumps(postBody))
    util.log_debug("r.text = " + r.text)
    if len(r.text) == 5:
        print("验证码使用周期超过7天")
        util.log_info("验证码使用周期超过7天")
        return False
    if len(r.text) == 1:
        print("mac地址出错")
        util.log_info("mac地址出错")
    elif len(r.text) == 2:
        print("验证码出错")
        util.log_info("验证码出错")
    elif len(r.text) == 3:
        print("数据库出错，联系管理员")
        util.log_info("数据库出错，联系管理员")

    if len(r.text) < 5:
        print("数据校验错误")
        util.log_info("数据校验错误")
        return False
    if (r.text >= str(20)):
        dif_ver = des_decrypt('testtest', str(r.text))
        dif_ver = str(dif_ver, encoding="utf-8")
        util.log_debug(dif_ver)
        util.log_debug(get_mac_address())
        if(get_mac_address() == dif_ver):
            return True
        else:
            print("该验证码已被别的机器使用，请更换验证码")
            return False

    return False
