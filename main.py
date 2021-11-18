# 导入需要的模块
import json
import requests
import pprint
import time
from datetime import datetime, timedelta
import core
import net
import yaml
import schedule

pp = pprint.PrettyPrinter(indent=4)


def getTimeStamp():
    serverTime = time.strptime(core.GetTime()["data"]["Time"], "%Y-%m-%dT%H:%M:%S.%fZ")
    print("serverTime", serverTime)
    timeStamp = int(time.mktime(serverTime)) + 32400  # 网页端取的是东八区时间上报
    print("interval time", timeStamp)
    return timeStamp


def showWelcome(playerStatus):
    allNFT = playerStatus["AllNFT"]
    userAccountInfo = playerStatus["UserAccountInfo"]
    print(f'''\n
        _____________________________________________________\n
        欢迎回来， {playerStatus["DisplayName"]} :\n
            当前体力值：{playerStatus["VirtualCurrency"]["EN"]}
            KWT:{allNFT["KWT"]}
            宝宝数量：{len(allNFT["Animals"])}
            装饰品数量：{len(allNFT["Decors"])}
            染料数量：{len(allNFT["Dyes"])}
            地块数量：{len(allNFT["Fields"])}
            材料数量：{len(allNFT["Materials"])}
            房间数量：{len(allNFT["Rooms"])}
            植物数量：{len(allNFT["Trees"])}
        ''')


def tasklist():
    # 清空任务
    schedule.clear()

    timeStamp = getTimeStamp()
    # 创建收割植物任务
    schedule.every(conf['harvestPeriod']).seconds.do(core.harverst(playerData=playerData,
                                                                       timeStamp=timeStamp,
                                                                       MaxTryTime=conf['MaxTryTime']))
    # 创建收割蛋任务

    while 1:
        schedule.run_pending()


if __name__ == "__main__":

    configure = open("conf.yaml", 'r')
    conf = yaml.safe_load(configure)

    # 先登录，需要用到用户的钱包地址和token
    # （目前不知道怎么根据钱包地址获取token，可能需要从钱包的插件。因此需要先在浏览器登录，从Network里拿到wallet_address和token，手填到代码开头，获取的方式见截图）
    loginSuccess = core.login(token=conf['token'],
                              wallet_address=conf['wallet_address'],
                              headers=net.headers)

    if loginSuccess:
        print("【登录成功！】")

    # 能够拿到用户数据
    playerData = core.GetPlayfabData()
    showWelcome(playerData)

    tasklist()
