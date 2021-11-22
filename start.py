import json
import pprint
import sys
from time import sleep
import requests
import core
import net
import yaml
import schedule
import verify
import marketplace
import util
from Conf import Conf

pp = pprint.PrettyPrinter(indent=4)



def showWelcome(playerStatus):
    allNFT = playerStatus["AllNFT"]
    userAccountInfo = playerStatus["UserAccountInfo"]
    util.log_info(f'''\n
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
    util.log_debug('task queue start')
    core.harverst()
    core.collectEgg()
    core.feed()
    core.getDye()
    core.convertDye()

allRunTime = 0

def runnedtime(ti):
    ti += 1
    if ti == 24:
        print("已运行24h，请重新登陆")
        sleep(10)
        sys.exit(0)

def tasklist():
    # 清空任务
    schedule.clear()

    # 创建任务
    schedule.every(Conf['harvestPeriod']).seconds.do(task_queue)
    schedule.every().hour.do(runnedtime,allRunTime)

    while 1:
        schedule.run_pending()

def checkRelease():
    if Conf["isDebug"]:
        print("注意！！isDebug忘记切换为false")
        return False
    if userInfo['token'] != '' and userInfo['wallet_address'] != '':
        print("注意！！token忘记去掉")
        return False

    return True
def run():

    if not checkRelease():
        print("\n_______________________________\n")
        print("目前为开发环境，请勿直接发布！")
        print("\n_______________________________\n")

    if not Conf["isDebug"]:
        # marketplace.checkMarket()
        ver_ID = input("请输入验证码：")
        if not verify.verity(ver_ID):
            util.log_debug("联系mixiu 购买验证码")
            sys.exit()
        else:
            util.log_debug("验证通过")
    # 先登录，需要用到用户的钱包地址和token
    # （目前不知道怎么根据钱包地址获取token，可能需要从钱包的插件。因此需要先在浏览器登录，从Network里拿到wallet_address和token，手填到代码开头，获取的方式见截图）
    loginSuccess = core.login(token=userInfo['token'],
                              wallet_address=userInfo['wallet_address'],
                              headers=net.headers)

    if loginSuccess:
        util.log_info("【登录成功！】")

    # 能够拿到用户数据
    playerData = core.GetPlayfabData()
    showWelcome(playerData)
    tasklist()
