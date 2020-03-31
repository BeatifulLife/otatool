# coding=utf-8
import os
import time
import subprocess
import zipfile

from autoOtainfo import *


class otautil:

    # 时间戳转问本地时间
    @staticmethod
    def TransToCurTime(timestr):
        timetext = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestr))
        return timetext

    # 根据smb服务器相对路劲获取dir
    @staticmethod
    def getRelativePath(currdir, relpath):
        temcurrdir = currdir
        reldirs = relpath.split("/")
        for i in reldirs:
            if i == ".":
                continue
            elif i == "..":
                temcurdirs = temcurrdir.split("/")
                length = len(temcurdirs)
                if length >= 2:
                    temcurrdir = ''
                    for j in range(length - 1):
                        if j == 0:
                            temcurrdir = j
                        else:
                            temcurrdir += "/" + j
                else:
                    return None
            else:
                temcurrdir += "/" + i

        return temcurrdir

    # 运行命令行
    @staticmethod
    def runCommand(cmd, isshell=True, isprintout=True, isprintcmd=True, isroot=False):
        if isprintcmd:
            print("Running: " + cmd)

        if not isroot:
            p = subprocess.Popen(cmd, shell=isshell)
        else:
            cmd = "echo " + autoOtainfo.RootPass + " | sudo -S " + cmd
            p = subprocess.Popen(cmd, shell=isshell)

        output, errput = p.communicate()
        if isprintout:
            print(output)
        return output, p.returncode

    # 获取一个不存在的文件夹用于创建和存放文件
    @staticmethod
    def getNonexistDir(dirpath):
        oripath = os.path.abspath(dirpath)
        tempath = oripath
        numindex = 1
        while True:
            if os.path.exists(tempath):
                tempath = oripath + "_" + str(numindex)
                numindex += 1
            else:
                return tempath

    @staticmethod
    def compare(x, y):
        if x > y:
            return 1
        elif x == y:
            return 0
        else:
            return -1

    @staticmethod
    def getZipfileStamp(zipfilepath: str, name: str):
        if os.path.exists(zipfilepath) and zipfilepath.endswith(".zip") and zipfile.is_zipfile(zipfilepath):
            otazipfile = zipfile.ZipFile(zipfilepath)
            try:
                otazipinfo = otazipfile.getinfo(name)
                #print("%d-%d-%d %d:%d:%d" % (otazipinfo.date_time[0], otazipinfo.date_time[1], otazipinfo.date_time[2], otazipinfo.date_time[3], otazipinfo.date_time[4], otazipinfo.date_time[5]))
                otatimestamp = time.mktime(time.strptime("%d-%d-%d %d:%d:%d" % (otazipinfo.date_time[0], otazipinfo.date_time[1], otazipinfo.date_time[2], otazipinfo.date_time[3],
                                             otazipinfo.date_time[4], otazipinfo.date_time[5]), '%Y-%m-%d %H:%M:%S'))
                otazipfile.close()
                return otatimestamp
            except KeyError:
                print(zipfilepath + " has no " + name)
                otazipfile.close()
                return 0.0
        else:
            #print(zipfilepath + "is not a zipfile")
            return 0.0

