#!/usr/bin/python

import sys
import traceback
import pexpect
import pxssh
#import paramiko as ssh_client
import telnetlib
#from  logg_wrap import *
import re


class comm(object):
      def __init__(self,device):
          self.device = device
          self.handle = None
          pass
      def connectDevice(self):
          
          if (self.device['handleType']=='SSH' or self.device['handleType']=='22'):
             self.handle = ssh.connect(self.device)
                     #self.deviceCmdStr = ssh.getCommandOutput(self.handle,'\n',self.device['prompt']).split('\n')[1]                   
          elif(self.device['handleType']=='TELNET'):
             self.handle = telnet.connect(self.device)
          else:
             print "handle type not supported"

      def disconnectDevice(self):

          if (self.device['handleType']=='SSH' or self.device['handleType']=='22'):
              self.handle = ssh.disconnect(self.handle)
                      #print self.handle            
          elif(self.device['handleType']=='TELNET'):
             self.handle = telnet.disconnect(self.handle)
          else:
             print  "handle type not supported"


      def executeCommand(self,cmd,interactive=False,expectList=[]):
          out = None
          if (self.device['handleType']=='SSH' or self.device['handleType']=='22'):
             out = ssh.getCommandOutput(self.handle,cmd,self.device['prompt'],interactive,expectList)                    
          elif(self.device['handleType']=='TELNET'):
             out = telnet.getCommandOutput(self.device,self.handle,cmd)
          else:
             print  "handle type not supported"
          return out

      def executeDebugCommand(self,cmd):
          out = None
          if (self.device['handleType']=='SSH' or self.device['handleType']=='22'):
             out = ssh.getDebugCommandOutput(self.handle,cmd,self.device['prompt'])                        
          elif(self.device['handleType']=='TELNET'):
             out = telnet.getDebugCommandOutput(self.device,self.handle,cmd)
          else:
             print  "handle type not supported"
          return out
          
      def reconnectDevice(self):

          if (self.device['handleType']=='SSH' or self.device['handleType']=='22'):
             self.handle  = ssh.reconnect(self.handle,self.device)
          elif(self.device['handleType']=='TELNET'):
             self.handle  = telnet.reconnect()
          else:
             print "handle type not supported"

class ssh(comm):
      def __init__(self,device):
          super(ssh, self).__init__(device)
      #  self.ssh_device = device
      #self.handle = None
      pass
      @staticmethod
      def connect(device):
          s = pxssh.pxssh()
          s.PROMPT= device['prompt']
          s.login(device['mgmtIp'], device['login'], device['password'],port=int(device['handlePort']),auto_prompt_reset=False,login_timeout=60)
          return s      
      @staticmethod
      def disconnect(handle):
        if(handle != None):
            handle.close()
        return None    

      @staticmethod       
      def reconnect(handle,device):
        if(handle != None):
            handle.close()    
            handle = ssh.connect(device) 
            return handle
        else:
            handle = ssh.connect(device)         
            return handle
      @staticmethod
      def getCommandOutput(handle,cmd,prompt,interactive,expectList,timeout=60):
        if(interactive):
           return ssh.handleInteractiveSession(handle,cmd,prompt,expectList,timeout) 
        else:           
           if(handle != None):
             try:
               out = ""
               out = ""+handle.read_nonblocking(size=100, timeout=1)
             except:
               pass
           handle.sendline(cmd) 
           #handle.expect('>$|#$|#\s+$')
           handle.expect("\\"+prompt+"$")
           out = ((handle.before).strip(cmd))
           outArray = out.split('\n')
           out = outArray[1:len(outArray)-1]
           out = '\n'.join(out)           
           return out.strip(cmd)

      @staticmethod 
      def handleInteractiveSession(handle,cmdList,prompt,expectList,timeout):
        print 'entering  interactive session \n'
        out = ""
        for i in range(0,len(expectList)):
            handle.sendline(cmdList[i])
            handle.expect(expectList[i])         
            out = out+handle.before+handle.after
        handle.sendline(cmdList[i+1])
        handle.expect("\\"+prompt+"$")
        out = out+handle.before+handle.after
        outArray = out.split("\n")
        outArray = outArray[1:len(outArray)-1]
        out = "\n".join(outArray)
        return out
         
      def getDebugCommandOutput(handle,cmd,prompt,timeout=60):
        t('info','cmd is '+cmd)
        if(handle != None):
            try:
               out = ""
               out = ""+handle.read_nonblocking(size=100, timeout=1)
            except:
               pass
            handle.sendline(cmd)
            handle.expect_exact('#',timeout)
            #handle.expect('^\S*#')
            print 'expext ended'
            #handle.expect_exact(prompt,timeout)
            for i in range(0,2):
                time.sleep(1)
                
                #handle.expect_exact('^\S*#',timeout)
                #handle.expect('^\S*#')
                #handle.prompt()
                print 'expext endedd'
                out = ((handle.before).strip(cmd))+out
                print out

class telnet(comm):
      def __init__(self,device):
          super(telnet, self).__init__(device)
      #self.telnet_device = device
      #self.handle = None
      pass
      @staticmethod
      def connect(device):
          tn = telnetlib.Telnet(str(device['mgmtIp']))
          tn.read_until('login: ')
          tn.write(str(device['username']) + '\n')
          tn.read_until('Password: ')
          tn.write(str(device['password']) + '\n')
          tn.read_until(str(device['prompt']))
          return tn
      @staticmethod 
      def disconnect(handle):
        if(handle != None):
            handle.write('exit\n')
        return None    

      @staticmethod
      def reconnect(handle,device):
         if(handle != None):
                 handle.write('exit\n')    
                 handle = telnet.connect(device) 
                 return handle
         else:
            handle = telnet.connect(device)         
            return handle        

      @staticmethod
      def getCommandOutput(device,handle,cmd):
          if(handle != None)    :
              handle.write(cmd+'\n')
              out = handle.read_until(device['prompt'])
              return out




if __name__ == "__main__":
    #import JsonHelper    
    config_file =   {
			"name" : "Comp1",
			"port" : "22",
			"username" : "neel",
			"password" : "cisco2010",
			"mgmtIp" : "10.0.0.100",
			"handle_type" : "SSH",
			"prompt" : "$ ",
			"Vendor"      : "Cisco",
			"Technlogy"   : "Router",
			"Model"       : "3600",
			"Device"      : "3601"
			}
    #execfile(config_file,globals())
    #devices_config = JsonHelper.jsonToDict(devices_config)
    print config_file
    pc1 = ssh(config_file)
    pc1.connectDevice()
    print "connected"
    ##Interactive session example
    #expectList = ['Destination filename \[startup-config\]\?']
    #a = pc1.executeCommand(['copy run start','startup-config'],True,expectList)

    a = pc1.executeCommand('ls')
    #a = pc1.executeCommand('ls')
    print a
    pc1.disconnectDevice()



