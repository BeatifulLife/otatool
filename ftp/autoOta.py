#!/usr/bin/env python
#coding=utf-8

import os
import time
from smb.SMBConnection import SMBConnection

username="xuzhaoyou"
password="mobile#3"
remote_ip="192.168.8.208"
smbconn=None
smbstatue=False
currdir='data'
curdirList=[]
strforfile="%+55s\t\t%+10s\t%+12s\t%+18s\t%+18s\t\t%+18s"
strfordir="%+55s\t\t%+10s\t%+12s\t%+18s\t%+18s\t\t%+18s"
MTK_PROJECT=["A","B","C","E","P","R"]
mtk_custom="/mnt/data/Custom_MTK/"
spr_custom="/mnt/data/Custom_SPR/"
project_map={"a708":spr_custom+"A708-L",
             "K102":mtk_custom+"K102-L",
             "K116":mtk_custom+"K116-L",
             "K707":mtk_custom+"K707-L",
             "K801":mtk_custom+"K707-L",
             "K805":mtk_custom+"K805-L",
             "K960":mtk_custom+"K960-L",
             "S960":mtk_custom+"S960-L",
             "ZH960":mtk_custom+"ZH960-K"}


def isMtkProject(projectname):
    pjhead = projectname.upper()
    for i in MTK_PROJECT:
        if pjhead.startswith(i):
            return True
    return False

def prePareDir(fullotapath):
    dirslist=fullotapath.split("/")
    if len(dirslist)!=5 or not filename[4].endswith("zip"):
        return None
    projectname=dirslist[2]
    projectinfos=projectname.split("_")
    localpath=''
    if len(projectinfos)==4:
        if isMtkProject(projectname):
            localpath=mtk_custom+projectinfos[0].upper()+"-"+projectinfos[3].upper()
        else:
            localpath=spr_custom+projectinfos[0].upper()+"-"+projectinfos[3].upper()
    else:
        for i in project_map.keys():
            if projectname.upper() == i:
                localpath=project_map[i]
                break

    if localpath!='' and  not os.exists(localpath):
        os.makedirs(localpath)
    customdirs=currdir.split("/")
    if len(customdirs)==5:
        newloacalpath=localpath+"/"+customdirs[3]+"/"+customdirs[4]
        os.makedirs(newloacalpath)
        return newloacalpath+"/"+dirslist[4]

    return None


def connectSmb():
    try:
        global smbconn
        global smbstatue
        smbconn = SMBConnection(username, password, 'xu-All-Series','WIN-FILE1',"jlinksz.com", use_ntlm_v2=True)
        smbstatue = smbconn.connect("192.168.8.206", 139)
    except Exception as e:
        print(e)
        smbconn.close()

def disconnectSmb():
    if smbstatue:
        smbconn.close()

def listShare():
    sharelist = smbconn.listShares()
    for i in sharelist:
        print i.name

def listAllFile():
    global curdirList
    global currdir
    hasota=False
    curdirList=[]
    filelist = smbconn.listPath("data",currdir)
    print(strfordir%("文件名","是否文件夹","文件大小","最后属性修改时间","创建时间","最后写入时间"))
    for i in filelist:
        if i.filename.startswith("."):
            continue
        curdirList.append(i)
        if i.file_attributes & 0x10 > 0:
            print(strfordir%(i.filename,'dir',i.file_size,TransToCurTime(i.create_time),TransToCurTime(i.last_attr_change_time),TransToCurTime(i.last_write_time)))
        else:
            print(strforfile%(i.filename,'file',i.file_size,TransToCurTime(i.create_time),TransToCurTime(i.last_attr_change_time),TransToCurTime(i.last_write_time)))

    dirs=currdir.split("/")
    if len(dirs)==5:
        if dirs[4].startswith("v"):
            listCutVersionOta()

def hasChoosefile(choosedir):
    global currdir
    for i in curdirList:
        if i.filename.upper() == choosedir.upper() and i.file_attributes & 0x10 > 0:
            currdir=currdir+"/"+i.filename
            return True
    return False

def TransToCurTime(timestr):
    timetext = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestr))
    return timetext

def listChooseDir(choosedir):
    global currdir
    if hasChoosefile(choosedir):
        listAllFile()
    else:
        num=0
        fileobject=None
        upchoose=choosedir.upper()
        print("\n\n")
        for i in curdirList:
            if i.filename.encode("utf-8").upper().find(upchoose)!=-1:
                num+=1
                fileobject=i
                print("\t"*10+i.filename)
        if num==0:
            listAllFile()
        elif num==1:
            print("\n\n")
            if fileobject.file_attributes & 0x10 > 0:
                currdir+="/"+fileobject.filename
                listAllFile()
            else:
                print(strfordir%("文件名","是否文件夹","  文件大小","最后属性修改时间","创建时间","  最后写入时间"))
                print(strfordir%(fileobject.filename,'file',fileobject.file_size,TransToCurTime(fileobject.create_time),TransToCurTime(fileobject.last_attr_change_time),TransToCurTime(fileobject.last_write_time)))
                chooice=raw_input("是否拉取到本地,Y/N):\n")
                if chooice=='Y':
                    pullFile("./",fileobject.filename)


def listCurDir(choosedir):
    global currdir
    isneedList=True
    if choosedir is not None:
        if choosedir == 'A' or choosedir=="..":
            if "/" in currdir:
                ind=currdir.rindex("/")
                if ind > 0:
                    currdir=currdir[0:ind]
            else:
                currdir='data'
        elif choosedir == 'B':
            currdir='data/JLink_OTA'
        elif choosedir == 'C':
            currdir='data'
        else:
            isneedList=False
            listChooseDir(choosedir)

    if isneedList:
        listAllFile()

def listCutVersionOta():
    temdirpath=currdir
    if currdir.endswith("/"):
        temdirpath=temdirpath[0:len(temdirpath)-1]
    dirs=currdir.split("/")
    otadir="data/Jlink_OTA/"
    if len(dirs)==5:
        otadir+=dirs[1]+"/"+dirs[4].split("_")[0]
        try:
            filelist = smbconn.listPath("data",otadir)
            for i in filelist:
                if i.filename.startswith("."):
                    continue
                if i.file_attributes & 0x10 > 0:
                    print(strfordir%(otadir+"/"+i.filename,'dir',i.file_size,TransToCurTime(i.create_time),TransToCurTime(i.last_attr_change_time),TransToCurTime(i.last_write_time)))
                else:
                    print(strforfile%(otadir+"/"+i.filename,'file',i.file_size,TransToCurTime(i.create_time),TransToCurTime(i.last_attr_change_time),TransToCurTime(i.last_write_time)))
        except:
            print("\n\t当前版本未发现ota包\n")
    


def pullFile(localdir,filename):
    if filename.startswith("data/Jlink_OTA") and filename.endswith("zip") and len(filename.split("/"))==5:
        if localdir.endswith("/"):
            lf = open(localdir.encode("utf-8")+filename.encode("utf-8").split("/")[4],'w')
        else:
            lf = open(localdir.encode("utf-8")+"/"+filename.encode("utf-8").split("/")[4],'w')
        smbconn.retrieveFile("data",filename,lf)
        lf.close()
    else:
        for i in curdirList:
            if i.filename.encode("utf-8").upper() == filename.upper().encode("utf-8"):
                if i.file_attributes & 0x10 ==0:
                    if localdir.endswith("/"):
                        lf = open(localdir.encode("utf-8")+filename.encode("utf-8"),'w')
                    else:
                        lf = open(localdir.encode("utf-8")+"/"+filename.encode("utf-8"),'w')
                    smbconn.retrieveFile("data",currdir+"/"+filename,lf)
                    lf.close()
                else:
                    print("仅支持文件的拉取，你选择的是"+filename+"文件夹")
            
 
def init():
    connectSmb()
    listAllFile()
    chooice=raw_input("请选择目录:\n\tA)上一层目录\n\tB)OTA目录\n\tC)根目录\n\t*)或直接输入当前目录\n\tQ)退出\n") 

if __name__ == '__main__':
    connectSmb()
    listAllFile()
    while(1):
        chooice=raw_input("请选择目录:\n\tA)上一层目录\n\tB)OTA目录\n\tC)根目录\n\t*)或直接输入当前目录\n\tQ)退出\n")
        if chooice == 'Q':
            disconnectSmb()
            break;
        elif chooice.find("/")!=-1:
            pullchooice=raw_input("是否拉取到本地,Y/N):\n")
            if pullchooice=='Y':
                pullFile("./",chooice)
        else:
            listCurDir(chooice)
        
    
