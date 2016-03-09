#!/usr/bin/python
import sys
import json
import copy

from fix_path import *
import comm
from fileOperations  import *
import table

class replayTranscript():
     def __init__(self,fileName,output):
        self.filename =  fileName
        self.outputFile = output

     def prepareRun(self):
         if(isFileExists(self.filename)):
            scriptObj = json.loads(getFileContents(self.filename))
            self.transcript = scriptObj['transcriptList']
            self.outputTranscript = copy.deepcopy(self.transcript)
            if(not self.initializeDevices(scriptObj['devicelist'])):
                return False
            return True
         else:
            print 'File not valid'
            return False

     def initializeDevices(self,devices):
         print 'initializing devices'
         self.devices = dict()
         for i in range(0,len(self.transcript)):
             step = self.transcript[i]
             if(step['command']['type'] == 'cliCommand'):
                 deviceName = step['command']['arguments']['device']
                 device =table.getRowFromTable(devices,'deviceName',deviceName)
                 if(deviceName in self.devices.keys()):
                     print 'Device already connected '+deviceName
                 else:
                     try:
                         print 'Connecting device '+deviceName
                         self.devices[deviceName] = comm.ssh(device)
                         self.devices[deviceName].connectDevice()
                         if(self.devices[deviceName].handle.before == ''):
                             raise Exception
                     except:
                        #print self.devices[deviceName].handle
                        print 'could not connect device '+ deviceName
                        return False
         return True


     def closeAllConnections(self):
         for i in range(0,len(self.devices.keys())):
             key = self.devices.keys()[i]
             deviceObj = self.devices[key]
             print 'Disconnecting device'+key
             deviceObj.disconnectDevice()

     def updateOutputLog(self,content):
         content = json.dumps(content)
         writeFile(self.outputFile,content)

     def modifyResponse(self,responseStep,response):
         responseStep['response']={}
         responseStep['response']['rawOutput'] = response
         responseStep['response']['notes'] = ""

     def replaySteps(self):
         if(self.prepareRun()):
             #self.createOutputLogFile()
             print 'Replaying the commands'
             for i in range(0,len(self.transcript)):
                 step = self.transcript[i]
                 if(step['command']['type'] == 'cliCommand'):
                     deviceName = step['command']['arguments']['device']
                     cmd = step['command']['arguments']['cmd']
                     print 'executing command '+cmd+' in device '+deviceName
                     response = self.devices[deviceName].executeCommand(cmd)
                     self.modifyResponse(self.outputTranscript[i],response)
                     print response
                     self.updateOutputLog(self.outputTranscript)

             self.closeAllConnections()



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Replay the recorded steps using the konfirmix log file.')
    parser.add_argument('--inputlog', help='Konfirmix log file name to execute the recorded steps',required=True)
    parser.add_argument('--outputlog', help='Output log file file name  to save the executed response ',default="lastOutputLog.tlog")
    args = parser.parse_args()
    #print 'Input log file is '+args.inputlog
    #print 'Output log file is '+args.outputlog'''
    #obj = replayTranscript('/home/neel/Downloads/up_1.tlog','lastOutputLog.tlog')
    obj = replayTranscript(args.inputlog,args.outputlog)
    obj.replaySteps()


