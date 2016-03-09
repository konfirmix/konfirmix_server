import subprocess
import os
import signal
class ProcessUtil():

       @staticmethod
       def getShellOutput(cmdArray):
         p = subprocess.Popen(cmdArray, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         output, err = p.communicate()            
         return output,err  

       @staticmethod
       def killProcess(processName):
         cmdArray = "ps -ef |grep "+"""'"""+processName+"""'"""
         output = ProcessUtil.getShellOutput(cmdArray)
         processList =  output[0].split('\n')
         for process  in processList:
            if('grep' not in process and process != ''):	
               processId = process.split()[1]
               os.kill(int(processId),signal.SIGKILL)

if __name__ == "__main__":
      a = ProcessUtil.killProcess("nohup python /home/neel/workspace/networkautomation/konfirmixV2    estB")
      