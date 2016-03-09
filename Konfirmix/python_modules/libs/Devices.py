#!/usr/bin/env python
import sys
import JsonHelper
import comm
class Device():        
    def __init__(self):
        pass
        
    def connect(self):   
        pass    
        
    @staticmethod
    def createDevice(deviceConfig):
        if(deviceConfig["Vendor"]=="Cisco"):
            return CiscoDevice.createDevice(deviceConfig)
        pass    
class CiscoDevice():    
    def __init__(self,deviceConfig):
        self.handle=comm.ssh(deviceConfig)
        self.Vendor="cisco"
        self.Tech="router"
        self.Model="3600"
        self.DeviceType="3601"
        pass
    def connect(self):
        self.handle.connectDevice()
    def executeCommand(self,command,memoryRule,validationJsonRule):
        commandOutput=self.handle.executeCommand(command)        
        return commandOutput
    @staticmethod
    def createDevice(deviceConfig):
        return CiscoDevice(deviceConfig)       
        
