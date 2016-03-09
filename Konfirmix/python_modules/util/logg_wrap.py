import logging
import json


def logg_init(logfile, loglevel):
    
    loglvl = "logging."+loglevel.upper()
    logging.basicConfig(filename=logfile, level=eval(loglvl), format="%(asctime)s: %(levelname)s: %(funcName)s: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')

def logg_insert(level,message):
    try:
      logg_call = "logging."+level.strip().lower()+"(message)"
      eval(logg_call)
    except:
      extype, exval = sys.exc_info()[:2]
      logging.warning("Error in logging the message at right log level: MSG:"+message + " Error: "+ str(extype) + str(exval))
def logCommand(command,device):
    node={'command':command,'device':device};
    return node        
def logCommandOutput(command,device,output):
    node={'command':command,
          'device':device,
          'output':output
          };
    return node          
def logCommandPraserOutput(device,command,output,jsonOutput):
    node={'command':command,
          'device':device,
          'output':output,
          'jsonOutput':jsonOutput
          };
    return node
def logCommandResult(device,command,output,jsonOutput,status):
    node={'command':command,
          'device':device,
          'output':output,
          'jsonOutput':jsonOutput,
          'status':status
          };
    print json.dumps(node,4); 
    pass
def logCommandFailure(stackTraceDump,node):
    node={'status': False,
          'stackTrace':stackTraceDump,
          'logs':node
          }
    print json.dumps(node,4); 
    pass
