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
from Conf import conf
import os
import dataManager
pp = pprint.PrettyPrinter(indent=4)
configure = open(os.path.join(os.getcwd(), "userInfo.yaml"), 'r')
user_conf = yaml.safe_load(configure)

def showWelcome(playerStatus):

    allNFT = playerStatus["AllNFT"]
    userAccountInfo = playerStatus["UserAccountInfo"]
    util.log_info(f'''\n
        _____________________________________________________\n
        欢迎回来， {playerStatus["DisplayName"]} :\n
            当前体力值：{playerStatus["VirtualCurrency"]["EN"]}
            KWT:{allNFT["KWT"]}
        ''')


def task_tree():
    util.log_debug('task queue start')
    core.harverst()

def task_animalFeed():
    util.log_debug('animal feed task start')
    core.feed()

def task_eggHarvest():
    util.log_debug('animal harvest task start')
    core.collectEgg()

def task_dye():
    util.log_debug("dye task start")
    core.getDye()
    core.convertDye()

def task_metarials():
    util.log_debug("metarials task start")
    core.getMetarials()
    core.convertMetarials()

allRunTime = 0

def runnedtime():
    global allRunTime
    allRunTime += 1
    util.log_debug("已运行"+str(allRunTime)+"h")
    if allRunTime == 25:
        print("已运行24h，请重新登陆")
        sleep(10)
        sys.exit(0)

def tasklist():
    # 清空任务
    schedule.clear()
    # 创建任务
    schedule.every(conf['harvestPeriod']).seconds.do(task_tree).run()

    schedule.every(conf['eggHarvestPeriod']).minutes.do(task_eggHarvest).run()
    schedule.every(conf['animalFeedPeriod']).minutes.do(task_animalFeed).run()

    schedule.every(conf['dyePeriod']).seconds.do(task_dye).run()

    schedule.every(conf['metarialsPeriod']).seconds.do(task_metarials).run()


    schedule.every().hour.do(runnedtime).run()

    while 1:
        schedule.run_pending()

def checkRelease():
    if conf["isDebug"]:
        print("注意！！isDebug忘记切换为false")
        if user_conf['token'] != '' and user_conf['wallet_address'] != '':
            print("注意！！token忘记去掉")
        return False

    return True
def run():

    if not checkRelease():
        print("\n_______________________________\n")
        print("目前为开发环境，请勿直接发布！")
        print("\n_______________________________\n")

    if not conf["isDebug"]:
        # marketplace.checkMarket()
        print(dataManager.ver_ID)
        if dataManager.ver_ID == "":
            dataManager.ver_ID = input("请输入验证码：")
        if not verify.verity(dataManager.ver_ID):
            print("联系mixiu 购买验证码")
            util.log_info("联系mixiu 购买验证码")
            dataManager.ver_ID = ""
            sleep(5)
            sys.exit()
        else:
            util.log_debug("验证通过")

    # 先登录，需要用到用户的钱包地址和token
    # （目前不知道怎么根据钱包地址获取token，可能需要从钱包的插件。因此需要先在浏览器登录，从Network里拿到wallet_address和token，手填到代码开头，获取的方式见截图）
    loginSuccess = core.login(token=user_conf['token'],
                              wallet_address=user_conf['wallet_address'],
                              headers=net.headers)

    if loginSuccess:
        util.log_info("【登录成功！】")

    # 能够拿到用户数据
    playerData = core.GetPlayfabData()
    showWelcome(playerData)
    tasklist()
