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
    elif updateType == 'convertDye':
            script = '{"CustomTags":null,"FunctionName":"DyeConvertOffChain","FunctionParameter":' + param + ',"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}'
    elif updateType == 'getDye':
            script = '{"CustomTags":null,"FunctionName":"DyeObtainOffChain","FunctionParameter":' + param + ',"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}'



    result = ExecuteCloudScript(script)
    pp.pprint(result)
    # print(f'{result["data"]["FunctionResult"]}')
    # if "Statistics" in result["data"]["FunctionResult"]["Modifiers"].keys():
    #     # print(f'!!!!!!!!操作成功！EXP：{result["data"]["FunctionResult"]["Modifiers"]["Statistics"]}')
    #     return 0
    if "Error" in result["data"]["FunctionResult"]:
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

    return 0





# 收获
def harverst():
    timeStamp = getTimeStamp()
    playerData = GetPlayfabData()
    time.sleep(1)
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
    time.sleep(1)
    global foodIds
    for key, animalData in playerData["Farm"]["AllAnimals"].items():
        #修改喂食时间
        animalData["FeedTime"] =  animalData["FeedTime"] + (timeStamp-animalData["FeedTime"])//120 * 120
        animalData["UpdateTime"] =  animalData["FeedTime"]
        foodIds = conf["feed_fruit_relation"][str(animalData["Id"])]

        inventory_fruit = playerData["Inventory"]["Fruit"]
        food1Num = inventory_fruit[str(foodIds[0])] if str(foodIds[0]) in inventory_fruit else 0
        food2Num = inventory_fruit[str(foodIds[1])] if str(foodIds[1]) in inventory_fruit else 0

        print(f'{conf["item_id_animal"][str(animalData["Id"])]} 想吃的食物:{conf["item_id_fruit"][str(foodIds[0])]}[str(foodIds[0])][{foodIds[0]}]有{food1Num}个，{conf["item_id_fruit"][str(foodIds[1])]}[{foodIds[1]}]有{food2Num}个')
        animalData["LstFoodIds"] = [] #要喂的水果
        for index in range(3):#最大喂食次数是3次
            if food1Num >= 10:
                animalData["LstFoodIds"].append(foodIds[0])
                food1Num = food1Num - 10
                time.sleep(1)
            elif food2Num >= 10:
                animalData["LstFoodIds"].append(foodIds[1])
                food2Num = food2Num - 10
                time.sleep(1)

        if len(animalData["LstFoodIds"]) == 0:
            print(f"背包里都没有水果，您就别喂啦！")
            continue
        animalData["MaxCap"] = len(animalData["LstFoodIds"])

        updateRes = UpdateFarmData("feed_animal",json.dumps({key: animalData}))
        if updateRes == 0:
            # TODO 记录收菜总收成
            print(f'喂食成功！Animal Uid:{key},名称：{conf["item_id_animal"][str(animalData["Id"])]}')



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
#收蛋
def collectEgg():
    timeStamp = getTimeStamp()
    playerData = GetPlayfabData()
    time.sleep(1)
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


#合成染料 加入工作队列
def convertDye():

    playerData = GetPlayfabData()
    time.sleep(1)
    inventory_fruit = playerData["Inventory"]["Fruit"]
    for fruitData in inventory_fruit:
        if inventory_fruit.get(str(foodIds[0]), 'not exist') >= 60 :
            convertData = {
                "Id": 6006,
                "Amount": 1,
                "FunctionName": "DyeConvertOffChain",
            }
            updateRes = UpdateFarmData("convertDye",json.dumps(convertData))


#获得染料 合成完成
def getDye():
    convertData = {
        "Index": 0,
        "FunctionName": "DyeObtainOffChain",
    }
    updateRes = UpdateFarmData("getDye",json.dumps(convertData))



#{"CustomTags":null,"FunctionName":"DyeConvertOffChain","FunctionParameter":{"Id":6006,"Amount":1,"FunctionName":"DyeConvertOffChain"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
#{"CustomTags":null,"FunctionName":"DyeConvertOffChain","FunctionParameter":{"Id":6006,"Amount":1,"FunctionName":"DyeConvertOffChain"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}

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
'''
{"CustomTags":null,"FunctionName":"RandomVisit","FunctionParameter":{"FunctionName":"RandomVisit"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
{
    "code": 200,
    "status": "OK",
    "data": {
        "FunctionName": "RandomVisit",
        "Revision": 107,
        "FunctionResult": {
            "PlayFabId": "2759184EEF9CDA08",
            "DisplayName": "Jaja",
            "Exp": 299308,
            "FarmModel": {
                "AllFields": {
                    "1633889872784": {
                        "Uid": "1633889872784",
                        "Id": 205001,
                        "X": 15,
                        "Y": 48
                    },
                    "1634055089562": {
                        "Uid": "1634055089562",
                        "Id": 205001,
                        "X": 8,
                        "Y": 53
                    },
                    "1634055091946": {
                        "Uid": "1634055091946",
                        "Id": 205001,
                        "X": 8,
                        "Y": 37
                    },
                    "1634055098829": {
                        "Uid": "1634055098829",
                        "Id": 205001,
                        "X": 15,
                        "Y": 54
                    },
                    "1634055101729": {
                        "Uid": "1634055101729",
                        "Id": 205001,
                        "X": 8,
                        "Y": 47
                    },
                    "1635650403777": {
                        "Uid": "1635650403777",
                        "Id": 205001,
                        "X": 21,
                        "Y": 55
                    },
                    "1636464440781": {
                        "Uid": "1636464440781",
                        "Id": 205001,
                        "X": 21,
                        "Y": 48
                    },
                    "1637204868380": {
                        "Uid": "1637204868380",
                        "Id": 205001,
                        "X": 8,
                        "Y": 42
                    }
                },
                "AllTrees": {
                    "1636365690387": {
                        "Uid": "1636365690387",
                        "Id": 201005,
                        "StartTime": 1636365690,
                        "LastHarvestTime": 1637441364,
                        "ParentUid": "1634055098829",
                        "UpdateTime": 1636365690
                    },
                    "1636985994469": {
                        "Uid": "1636985994469",
                        "Id": 201009,
                        "StartTime": 1636985994,
                        "LastHarvestTime": 1637441363,
                        "ParentUid": "1634055091946",
                        "UpdateTime": 1636985994
                    },
                    "1636986132651": {
                        "Uid": "1636986132651",
                        "Id": 201001,
                        "StartTime": 1636986132,
                        "LastHarvestTime": 1637441364,
                        "ParentUid": "1633889872784",
                        "UpdateTime": 1636986132
                    },
                    "1637345449072": {
                        "Uid": "1637345449072",
                        "Id": 201006,
                        "StartTime": 1637345449,
                        "LastHarvestTime": 1637441363,
                        "ParentUid": "1634055089562",
                        "UpdateTime": 1637345449
                    },
                    "1637345465122": {
                        "Uid": "1637345465122",
                        "Id": 201011,
                        "StartTime": 1637345465,
                        "LastHarvestTime": 1637441363,
                        "ParentUid": "1634055101729",
                        "UpdateTime": 1637345465
                    },
                    "1637345582116": {
                        "Uid": "1637345582116",
                        "Id": 201004,
                        "StartTime": 1637345582,
                        "LastHarvestTime": 1637441364,
                        "ParentUid": "1635650403777",
                        "UpdateTime": 1637345582
                    },
                    "1637385815900": {
                        "Uid": "1637385815900",
                        "Id": 201007,
                        "StartTime": 1637385815,
                        "LastHarvestTime": 1637441364,
                        "ParentUid": "1636464440781",
                        "UpdateTime": 1637385815
                    },
                    "1637408548402": {
                        "Uid": "1637408548402",
                        "Id": 201010,
                        "StartTime": 1637408548,
                        "LastHarvestTime": 1637441363,
                        "ParentUid": "1637204868380",
                        "UpdateTime": 1637408548
                    }
                },
                "AllAnimals": {
                    "1636985946353": {
                        "Uid": "1636985946353",
                        "Id": 206001,
                        "FeedTime": 1637441401,
                        "HarvestedCount": 0,
                        "UpdateTime": 1637441401,
                        "MaxCap": 3,
                        "FoodId": 0,
                        "LstFoodIds": [
                            202005,
                            202005,
                            202005
                        ]
                    },
                    "1637347246889": {
                        "Uid": "1637347246889",
                        "Id": 206010,
                        "FeedTime": 1637438943,
                        "HarvestedCount": 2,
                        "UpdateTime": 1637438943,
                        "MaxCap": 3,
                        "FoodId": 0,
                        "LstFoodIds": [
                            202006,
                            202006,
                            202006
                        ]
                    },
                    "1637347251722": {
                        "Uid": "1637347251722",
                        "Id": 206002,
                        "FeedTime": 1637439355,
                        "HarvestedCount": 1,
                        "UpdateTime": 1637439355,
                        "MaxCap": 2,
                        "FoodId": 0,
                        "LstFoodIds": [
                            202010,
                            202010
                        ]
                    },
                    "1637385820182": {
                        "Uid": "1637385820182",
                        "Id": 206004,
                        "FeedTime": 1637440976,
                        "HarvestedCount": 0,
                        "UpdateTime": 1637440976,
                        "MaxCap": 1,
                        "FoodId": 0,
                        "LstFoodIds": [
                            202007
                        ]
                    }
                }
            },
            "ProfileDescription": "I send energies everyday. Please send me too ^^",
            "Gender": "Female",
            "WearingIds": [
                "10001002",
                "10107003",
                "10207003",
                "10407005",
                "10507003",
                "10707005"
            ]
        },
        "Logs": [],
        "ExecutionTimeSeconds": 0.1072751,
        "ProcessorTimeSeconds": 0.002303,
        "MemoryConsumedBytes": 76560,
        "APIRequestsIssued": 4,
        "HttpRequestsIssued": 0
    }
}
'''

#生成订单
# {"CustomTags":null,"FunctionName":"GenerateOrder","FunctionParameter":{"FunctionName":"GenerateOrder"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
#
#
#交付订单
# {"CustomTags":null,"FunctionName":"DeliveryObtainNFT","FunctionParameter":{"IsDev":false,"Address":null,"Index":0,"FunctionName":"DeliveryObtainNFT"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
#
# 偷菜偷蛋
# {"CustomTags":null,"FunctionName":"Help","FunctionParameter":{"Data":{"DictEggs":{"207001":1}},"OtherId":"2759184EEF9CDA08","FunctionName":"Help"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
#
#
# 获取好友列表
# https://b477a.playfabapi.com/Client/GetFriendsList?sdk=UnitySDK-2.113.210830
#{"CustomTags":null,"IncludeFacebookFriends":null,"IncludeSteamFriends":null,"ProfileConstraints":{"ShowAvatarUrl":false,"ShowBannedUntil":false,"ShowCampaignAttributions":false,"ShowContactEmailAddresses":false,"ShowCreated":false,"ShowDisplayName":true,"ShowExperimentVariants":false,"ShowLastLogin":true,"ShowLinkedAccounts":false,"ShowLocations":false,"ShowMemberships":false,"ShowOrigination":false,"ShowPushNotificationRegistrations":false,"ShowStatistics":true,"ShowTags":false,"ShowTotalValueToDateInUsd":false,"ShowValuesToDate":false},"XboxToken":null,"AuthenticationContext":null}
# {"code":200,"status":"OK","data":{"Friends":[{"FriendPlayFabId":"43103EE911461424","TitleDisplayName":"mixiu","Tags":["confirmed"],"Profile":{"PublisherId":"E740DDFD3653CA4F","TitleId":"B477A","PlayerId":"43103EE911461424","LastLogin":"2021-11-21T01:30:40.57Z","DisplayName":"mixiu","Statistics":[{"Name":"Exp","Version":1,"Value":13016}]}}]}}#
#
# 通过钱包地址获取用户ID
# {"CustomTags":null,"FunctionName":"GetPlayfabIdFromMetaMask","FunctionParameter":{"MetaMaskAddress":"0x0198D860C767aF45a91CC09949c1CfB74E49c939","FunctionName":"GetPlayfabIdFromMetaMask"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
# {"code":200,"status":"OK","data":{"FunctionName":"GetPlayfabIdFromMetaMask","Revision":107,"FunctionResult":{"PlayfabId":"43103EE911461424"},"Logs":[],"ExecutionTimeSeconds":0.1211591,"ProcessorTimeSeconds":0.000533,"MemoryConsumedBytes":6064,"APIRequestsIssued":1,"HttpRequestsIssued":0}}
#
#
# 获取用户资料
# Request URL: https://b477a.playfabapi.com/Client/GetPlayerProfile?sdk=UnitySDK-2.113.210830
# {"CustomTags":null,"PlayFabId":"43103EE911461424","ProfileConstraints":{"ShowAvatarUrl":false,"ShowBannedUntil":false,"ShowCampaignAttributions":false,"ShowContactEmailAddresses":false,"ShowCreated":false,"ShowDisplayName":true,"ShowExperimentVariants":false,"ShowLastLogin":true,"ShowLinkedAccounts":false,"ShowLocations":false,"ShowMemberships":false,"ShowOrigination":false,"ShowPushNotificationRegistrations":false,"ShowStatistics":true,"ShowTags":false,"ShowTotalValueToDateInUsd":false,"ShowValuesToDate":false},"AuthenticationContext":null}
# {"code":200,"status":"OK","data":{"PlayerProfile":{"PublisherId":"E740DDFD3653CA4F","TitleId":"B477A","PlayerId":"43103EE911461424","LastLogin":"2021-11-21T01:25:20Z","DisplayName":"mixiu","Statistics":[{"Name":"Exp","Version":1,"Value":12998}]}}}
#
#
#
# 加好友
# {"CustomTags":null,"FunctionName":"SendFriendRequest","FunctionParameter":{"FriendPlayFabId":"43103EE911461424","FunctionName":"SendFriendRequest"},"GeneratePlayStreamEvent":null,"RevisionSelection":"Live","SpecificRevision":0,"AuthenticationContext":null}
