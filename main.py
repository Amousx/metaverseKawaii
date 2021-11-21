import json
import pprint
import sys

import requests

import core
import net
import yaml
import schedule
import verify
import marketplace

pp = pprint.PrettyPrinter(indent=4)


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


def task_queue():
    print('task queue start')
    core.harverst()
    core.collectEgg()
    core.feed()
    core.getDye()
    core.convertDye()


def tasklist():
    # 清空任务
    schedule.clear()

    # 创建任务
    schedule.every(conf['harvestPeriod']).seconds.do(task_queue).run()

    while 1:
        schedule.run_pending()


if __name__ == "__main__":
    # marketplace.checkMarket()
    ver_ID = input("请输入验证码：")
    configure = open("conf.yaml", 'r')
    conf = yaml.safe_load(configure)
    if not verify.verity(ver_ID):
        print("联系mixiu 购买验证码")
        sys.exit()
    else:
        print("验证通过")
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
