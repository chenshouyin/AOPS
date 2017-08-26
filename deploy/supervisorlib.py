#!/usr/bin/env python
#coding: utf-8

import xmlrpclib

class SuperVisor(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = "http://{}:{}/RPC2".format(self.ip, self.port)

        self.server = xmlrpclib.Server(self.url)

    def getState(self):
        '''获取supervisor状态
        '''
        return self.server.supervisor.getState()

    def getAPIVersion(self):
        '''获取RPC API版本
        '''
        return self.server.supervisor.getAPIVersion()

    def getSupervisorVersion(self):
        '''获取supervisor版本
        '''
        return self.server.supervisor.getSupervisorVersion()

    def getPID(self):
        '''获取supervisor pid
        '''
        return self.server.supervisor.getPID()

    def shutdown(self):
        '''关闭supervisor进程
        '''
        self.server.supervisor.shutdown()
        return ""

    def restart(self):
        '''重启supervisor
        self.server.supervisor.restart()'
        '''
        self.server.supervisor.restart()
        return ""

    def getProcessInfo(self, name):
        '''获取某个进程的信息.
        name: 表示 [progranme:<name>]中的<name>值
        '''
        return self.server.getProcessInfo(name)

    def getAllProcessInfo(self):
        '''获取所有进程信息
        '''
        return self.server.supervisor.getAllProcessInfo()

    def startProcess(self, name):
        '''启动命名为 name 的进程
        '''
        return self.server.supervisor.startProcess(name)

    def startProcessGroup(self):
        '''启动名为“name”的组中的所有进程
        '''
        return self.server.supervisor.startProcessGroup(name)
    
    def startAllProcesses(self):
        '''启动配置文件中列出的所有进程.
        '''
        return self.server.supervisor.startAllProcesses()

    def stopProcess(self, name):
        '''停止命名为name的进程
        '''
        return self.server.supervisor.stopProcess(name)
    
if __name__ == "__main__":
    ip = "10.135.33.236"
    port = 9001
    visor = SuperVisor(ip, port)
    print visor.getState()
    print visor.getAllProcessInfo()
