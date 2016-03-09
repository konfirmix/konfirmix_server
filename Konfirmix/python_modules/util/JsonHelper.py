import json

def jsonToPythonObject(s):
    return h2o(json.loads(s))

def h2o(x):
    if isinstance(x, dict):
         return type('jo', (object,), {k: h2o(v) for k, v in x.iteritems()})
    else:      
         return x


def jsonToDict(s):
    pyObj =   jsonToPythonObject(s)
    return typeToDict(pyObj)          

def typeToDict(typeObj):
    nObj = dict()
    for key,value in  typeObj.__dict__.iteritems():
         if('__' not in key):
                if(isinstance(value,type)):
                    value = typeToDict(value)
                nObj[key] = value
    return nObj  