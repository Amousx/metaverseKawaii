#游戏相关代码
import requests
import yaml
import json
import pprint as pp
import net
import copy

err_NotEnoughTime = "Not enough time to harvest"
err_InvalidTime = "Invalid Time"
err_NotFed = "This animal has not been fed yet"


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
    # pp.pprint(content)
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
    elif updateType == 'animal':
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
        if result["data"]["FunctionResult"]["Error"] == err_InvalidTime:
            print(f'无效时间！')
            return 2
        if result["data"]["FunctionResult"]["Error"] == err_NotFed:
            print(f'宝宝还没喂食！')
            return 3
            
    return -1




# 收获
def harverst(playerData, timeStamp, MaxTryTime):
    print("harverst ",playerData, timeStamp, MaxTryTime)
    # harvest Trees
    for key, plantData in playerData["Farm"]["AllTrees"].items():
        if plantData["LastHarvestTime"] == 0:
            print("请先手动收获一次")
            pass
        print("Harvesting Tree uid:", key, " id: ", str(plantData["Id"]))
        plantData["LastHarvestTime"] =  plantData["LastHarvestTime"] + (timeStamp-plantData["LastHarvestTime"])//120 * 120
        plantData["UpdateTime"] = plantData["LastHarvestTime"]
        updateRes = UpdateFarmData("tree",json.dumps({key: plantData}))
        if updateRes == 0:
            # TODO 记录收菜总收成
            print(f'收菜成功！')


    # for key, animalData in playerData["Farm"]["AllAnimals"].items():

    #     animalData["FeedTime"] =  animalData["FeedTime"] + (timeStamp-animalData["FeedTime"])//120 * 120
    #     animalData["LstFoodIds"] =  [202006]
    #     updateRes = UpdateFarmData("feed_animal",json.dumps({key: animalData}))
    #     if updateRes == 0:
    #         # TODO 记录收菜总收成
    #         print(f'喂食成功！')

    # for key, animalData in playerData["Farm"]["AllAnimals"].items():
    #     updateRes = UpdateFarmData("animal",json.dumps({key: animalData}))
    #     if updateRes == 0:
    #         # TODO 记录收菜总收成
    #         print(f'收蛋成功！')
