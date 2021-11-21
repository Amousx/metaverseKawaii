#游戏相关代码
import requests
import yaml
import json
import pprint as pp
import net
import time
import util
import random

err_NotEnoughTime = "Not enough time to harvest"
err_InvalidTime = "Invalid Time"
err_NotFed = "This animal has not been fed yet"
err_InvalidFoodId = "Invalid Food Id"

configure = open("conf.yaml", 'r')
conf = yaml.safe_load(configure)


# 登录
def login(token, wallet_address, headers):
    url = 'https://playfab.imbaapi.com/LoginWithToken'
    data = {
        "host": "",
        "path": "LoginWithToken",
        "token": token,
        "address": str(wallet_address),
        "titleId": "B477A"
    }
    data = json.dumps(data)
    print('data:',data)
    response = requests.post(url, data=data, headers=headers)
    content = json.loads(response.content)
    if content.get('code') != 200:
        pp.pprint(content)
        print("【登录失败，请联系作者】")
        return False
    print(f'Authorization ：{content["data"]["SessionTicket"]}')
    # 登录成功拿到x-authorization
    headers["x-authorization"] = content["data"]["SessionTicket"]

    return True

# 游戏里的心跳包，获取服务器时间
def GetTime():
    response = net.post('https://b477a.playfabapi.com/Client/GetTime?sdk=UnitySDK-2.113.210830',
                    '{"AuthenticationContext":null}')
    content = json.loads(response.content)
    print(content)
    return content

def getTimeStamp():

    serverTime = time.strptime(GetTime()["data"]["Time"], "%Y-%m-%dT%H:%M:%S.%fZ")
    print("serverTime", serverTime)

    timeStamp = int(time.mktime(serverTime))
    timeStamp = timeStamp + 3600 * util.calculate_offset(timeStamp)  # 网页端取的是东八区时间上报
    print("interval time", timeStamp)
    return timeStamp


# 游戏的核心API
def ExecuteCloudScript(data):
    print("*********ExecuteCloudScript data:", str(data))
    net.options('https://b477a.playfabapi.com/Client/ExecuteCloudScript?sdk=UnitySDK-2.113.210830')
    response = net.post('https://b477a.playfabapi.com/Client/ExecuteCloudScript?sdk=UnitySDK-2.113.210830', data)
    content = json.loads(response.content)
    return content


# 请求用户数据
def GetPlayfabData():
    content = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"GetPlayfabData","FunctionParameter":{"IsDev":false,"Address":null,'
        '"FunctionName":"GetPlayfabData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live",'
        '"SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(content)
    if content["code"] != 200:
        print(f'获取用户数据失败！请联系作者')
        return None
    return content["data"]["FunctionResult"]


# 随机访问
def RandomVisit():
    result = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"RandomVisit","FunctionParameter":{"FunctionName":"RandomVisit"},'
        '"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(result)


# 要先从随机访问API拿到数据
def Help():
    result = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"Help","FunctionParameter":{"Data":{"DictFruits":{"202009":1}},'
        '"OtherId":"41A9011E57182506","FunctionName":"Help"},"GeneratePlayStreamEvent":null,'
        '"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(result)


# 获取自己的NFT背包
def GetNFTData():
    result = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"GetNFTData","FunctionParameter":{"IsDev":false,"Address":null,'
        '"LstCategories":["fields","trees","animals"],"GetKawaiiToken":false,"FunctionName":"GetNFTData"},'
        '"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(result)


# 更新体力值
def UpdateEnergy():
    result = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"UpdateEnergy","FunctionParameter":{"FunctionName":"UpdateEnergy"},'
        '"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(result)


# 定时检查农场
def IntervalCheckFarm():
    result = ExecuteCloudScript(
        '{"CustomTags":null,"FunctionName":"IntervalCheckFarm","FunctionParameter":{"IsDev":false,"Address":null,'
        '"FunctionName":"IntervalCheckFarm"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live",'
        '"SpecificRevision":0,"AuthenticationContext":null}')
    pp.pprint(result)


# 操作API
def UpdateFarmData(updateType,param):

    script = ''
    if updateType == 'tree':
        script = '{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictTrees":' + param + ',"IsHarvestTree":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live",''"SpecificRevision":0,"AuthenticationContext":null}'
    elif updateType == 'collectEgg':
        script = '{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":' + param + ',"IsHarvestAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}'
    elif updateType == 'feed_animal':
            script = '{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":' + param + ',"IsFeedAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}'


    result = ExecuteCloudScript(script)
    pp.pprint(result)
    # print(f'{result["data"]["FunctionResult"]}')
    if "Statistics" in result["data"]["FunctionResult"]["Modifiers"].keys():
        # print(f'!!!!!!!!操作成功！EXP：{result["data"]["FunctionResult"]["Modifiers"]["Statistics"]}')
        return 0
    else:
        print(f'!!!!!!!!操作失败！错误原因：{result["data"]["FunctionResult"]["Error"]}')
        if result["data"]["FunctionResult"]["Error"] == err_NotEnoughTime:
            print(f'没到时间！')
            return 1
        elif result["data"]["FunctionResult"]["Error"] == err_InvalidTime:
            print(f'无效时间！')
            return 2
        elif result["data"]["FunctionResult"]["Error"] == err_NotFed:
            print(f'宝宝还没喂食！')
            return 3
        elif result["data"]["FunctionResult"]["Error"] == err_InvalidFoodId:
            print(f'食物ID有误！')
            return 4
            
    return -1





# 收获
def harverst():
    timeStamp = getTimeStamp()
    playerData = GetPlayfabData()
    print("harverst ",playerData, timeStamp)
    # harvest Trees
    for key, plantData in playerData["Farm"]["AllTrees"].items():
        if plantData["LastHarvestTime"] == 0:
            print("请先手动收获一次")
            pass
        print("Harvesting Tree uid:", key, " id: ", str(plantData["Id"]))
        #修改收割时间
        plantData["LastHarvestTime"] =  plantData["LastHarvestTime"] + (timeStamp-plantData["LastHarvestTime"])//120 * 120
        plantData["UpdateTime"] = plantData["LastHarvestTime"]
        updateRes = UpdateFarmData("tree",json.dumps({key: plantData}))
        if updateRes == 0:
            # TODO 记录收菜总收成
            print(f'收菜成功！Tree Uid:{key},名称：{conf["item_id_species"][str(plantData["Id"])]}')

#喂食 不成功
def feed():
    timeStamp = getTimeStamp()
    playerData = GetPlayfabData()
    for key, animalData in playerData["Farm"]["AllAnimals"].items():
        #修改喂食时间
        animalData["FeedTime"] =  animalData["FeedTime"] + (timeStamp-animalData["FeedTime"])//120 * 120
        foodIds = conf["feed_fruit_relation"][str(animalData["Id"])]
        print(f'{conf["item_id_animal"][str(animalData["Id"])]} 想吃的食物是:{foodIds}')
        animalData["LstFoodIds"] = [foodIds[0]] 
        animalData["MaxCap"] = 2
        while(True):
            updateRes = UpdateFarmData("feed_animal",json.dumps({key: animalData}))
            if updateRes == 0:
                # TODO 记录收菜总收成
                print(f'喂食成功！Animal Uid:{key},名称：{conf["item_id_animal"][str(animalData["Id"])]}')
            elif updateRes == 4:
                animalData["LstFoodIds"] = [foodIds[1]] 

# {"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":{"1637045983332": {"Uid": "1637045983332", "Id": 206010, "FeedTime": 1637454840, "HarvestedCount": 0, "UpdateTime": 1637420758, "MaxCap": 2, "FoodId": 0, "LstFoodIds": [202006]}},"IsFeedAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}

#{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":{"1637045983332":{"Uid":"1637045983332","Id":206010,"FeedTime":1637454965,"HarvestedCount":0,"UpdateTime":1637454965,"MaxCap":1,"FoodId":0,"LstFoodIds":[202006]}},"IsFeedAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}

''' 网页正确请求和返回的数据
{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":{"1637045983332": {"Uid": "1637045983332", "Id": 206010, "FeedTime": 1637454480, "HarvestedCount": 0, "UpdateTime": 1637420758, "MaxCap": 2, "FoodId": 0, "LstFoodIds": [202006]}},"IsFeedAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
*
{"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":{"1637045983332":{"Uid":"1637045983332","Id":206010,"FeedTime":1637324480,"HarvestedCount":0,"UpdateTime":1637324480,"MaxCap":2,"FoodId":0,"LstFoodIds":[202006,202006]}},"IsFeedAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
{
    "code": 200,
    "status": "OK",
    "data": {
        "FunctionName": "UpdateFarmData",
        "Revision": 107,
        "FunctionResult": {
            "Modifiers": {}
        },
        "Logs": [],
        "ExecutionTimeSeconds": 0.083922,
        "ProcessorTimeSeconds": 0.00244,
        "MemoryConsumedBytes": 32536,
        "APIRequestsIssued": 5,
        "HttpRequestsIssued": 0
    }
}
'''
#收蛋 不成功
def collectEgg():
    timeStamp = getTimeStamp()
    playerData = GetPlayfabData()
    for key, animalData in playerData["Farm"]["AllAnimals"].items():
        print("collect Animal uid:", key, " id: ", str(animalData["Id"]))
        animalData["FeedTime"] =  0
        animalData["HarvestedCount"] = 0
        animalData["UpdateTime"] = timeStamp
        animalData["MaxCap"] = 0
        animalData["LstFoodIds"] = []
        updateRes = UpdateFarmData("collectEgg",json.dumps({key: animalData}))
        if updateRes == 0:
            # TODO 记录收菜总收成
            print(f'收蛋成功！')

''' 网页正确请求和返回的数据
 {"CustomTags":null,"FunctionName":"UpdateFarmData","FunctionParameter":{"Data":{"DictAnimals":{"1637045983332":{"Uid":"1637045983332","Id":206010,"FeedTime":0,"HarvestedCount":0,"UpdateTime":1637323929,"MaxCap":0,"FoodId":0,"LstFoodIds":[]}},"IsHarvestAnimal":true},"FunctionName":"UpdateFarmData"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
{
    "code": 200,
    "status": "OK",
    "data": {
        "FunctionName": "UpdateFarmData",
        "Revision": 107,
        "FunctionResult": {
            "Modifiers": {
                "Statistics": {
                    "Exp": 954
                }
            }
        },
        "Logs": [],
        "ExecutionTimeSeconds": 0.1144141,
        "ProcessorTimeSeconds": 0.003183,
        "MemoryConsumedBytes": 33984,
        "APIRequestsIssued": 7,
        "HttpRequestsIssued": 0
    }
}
'''