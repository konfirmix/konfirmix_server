#!/usr/bin/python
class utils():
    @staticmethod
    def replaceArguments(command,globalVar):
        import re
        p = re.compile(ur'(\$[\w]+)')             
        argumentSet=re.findall(p, command)
        for argument in argumentSet:
            command=command.replace(argument,str(globalVar[argument[1:]]))
        return command
    @staticmethod
    def replaceRuleVariables(ruleList,globalVar):
        import re 
        for rule in ruleList:
            ruleObj = rule['checkObj']
            for key in ruleObj.keys(): 
                p = re.compile(ur'(\$[\w]+)')             
                argumentSet=re.findall(p, ruleObj[key])
                for argument in argumentSet:
                   ruleObj[key] = ruleObj[key].replace(argument,str(globalVar[argument[1:]]))
        return ruleList    
    
    @staticmethod
    def replaceReferenceObjForVariables(variableList,globalVar):
        import re 
        for variableObj in variableList:
            if('referenceObj' in variableObj.keys()):
                referenceObj = variableObj['referenceObj']
                for key in referenceObj.keys(): 
                    p = re.compile(ur'(\$[\w]+)')             
                    argumentSet=re.findall(p, referenceObj[key])
                    for argument in argumentSet:
                       referenceObj[key] = referenceObj[key].replace(argument,str(globalVar[argument[1:]]))
        return variableList        
    
if __name__ == "__main__":
       rules = [
                {"checkObj": {
                              "key1":" hey $var1",
                              "key2":"$var2"
                             },
                "pathArray":["rows","0"]         
                }
                
                ]
       globalVar = {
                  "var1":"sub_value1" ,
                  "var2":"sub_value2"
                
                   } 
                
                
       variables = [
                {"referenceObj": {
                              "key1":" hey $var1",
                              "key2":"$var2"
                             },
                "pathArray":["rows","0"]         
                },
                {
                "er":"r"                  
                }
                
                ]                
       #a = utils.replaceRuleVariables(rules,globalVar)        
       a = utils.replaceReferenceObjForVariables(variables,globalVar)  
    
       print a
    
    
    
    
    
