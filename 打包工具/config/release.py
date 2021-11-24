#!/usr/bin/env python  -*- coding: UTF-8 -*-
#coding=utf-8
import os,sys
import shutil
import re
import datetime
import random
import string
import zipfile 
import configparser

curPath=os.path.split(os.path.realpath(__file__))[0]
rootPath=os.path.abspath(os.path.join(curPath,".."))

tempPath = curPath + '/temp'
distPath = rootPath + '/dist'
buildPath = rootPath + '/build'
resourcePath = rootPath + '/resource'
configPath = curPath + '/config.ini'
'''
【打包脚本】
'''

def createVersionFile(new_version):
    filename = curPath + '/file_version_info.txt'
    file = open(filename,'w',encoding='utf-8')
    data = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(0, 0, 0, 0),
    prodvers=(0, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404b0',
        [StringStruct(u'CompanyName', u'请联系作者QQ641890557'),
        StringStruct(u'FileDescription', u'请联系作者QQ641890557'),
        StringStruct(u'FileVersion', u'{new_version}'),
        StringStruct(u'LegalCopyright', u'请联系作者QQ641890557'),
        StringStruct(u'ProductName', u'Kawaii Island脚本'),
        StringStruct(u'ProductVersion', u'{new_version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)'''
    file.write(data)
    file.close()


def upgradeVersion(): #自增升级版本号
    config = configparser.ConfigParser()
    config.read(configPath)
    version = config["project"]["version"]
    ver_arr = version.split('.')
    b_ver = ver_arr[0]
    m_ver = ver_arr[1]
    s_ver = int(ver_arr[2]) + 1
    new_version = f'{b_ver}.{m_ver}.{str(s_ver)}'
    print(f'版本号 {version} -> {new_version} ')
    config.set("project", "version", new_version)
    with open(configPath,"w+") as f:
        config.write(f)

    createVersionFile(new_version)


def start():
    #清空dist目录
    if os.path.isdir(distPath):
        shutil.rmtree(distPath,True)
    os.makedirs(distPath)

    #自增升级版本号
    upgradeVersion()



def createUserInfoFile():
    filename = distPath + '/userInfo.yaml'
    file = open(filename,'w') # 将要写入文件名的文件， w表示write
    data = '''---
    wallet_address: ""
    token: ""'''
    file.write(data)
    file.close()



def run_zip():
    zip = zipfile.ZipFile('KawaiiIsland脚本.zip',"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(distPath):
        fpath = path.replace(distPath,'')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))

    for path,dirnames,filenames in os.walk(resourcePath):
        fpath = path.replace(resourcePath,'')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()



def end():
    #用户信息文件，保证为空，避免上传我们测试用的token
    createUserInfoFile()

    #打包
    run_zip()

    if os.path.isdir(distPath):
        shutil.rmtree(distPath,True)
    if os.path.isdir(buildPath):
        shutil.rmtree(buildPath,True)
    if os.path.exists(curPath + '/file_version_info.txt'): 
        os.remove(curPath + '/file_version_info.txt')  


if __name__ == '__main__':
    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "end":
        end()