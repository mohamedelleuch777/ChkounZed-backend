#!/usr/bin/env python
import config


if len(config.REQUEST_URL.split('/')) <= 2:
    config.Controller.BlockRequests()
if config.REQUEST_URL.split('/')[2] == '':
    config.Controller.BlockRequests()
if len(config.REQUEST_URL.split('/')) > 3:
    config.Controller.InexistantRequest()
requestedClassName = config.REQUEST_URL.split('/')[1]
requestedMethodName = config.REQUEST_URL.split('/')[2]
requestedArgs = config.REQUEST_ARGS



requestedController = config.importModule("controllers/"+requestedClassName.lower()+".py")
if requestedController == None:
    config.Controller.InexistantRequest()
requestedClass = getattr(requestedController, requestedClassName)
myClass = requestedClass()
try:
    methodToCall = getattr(myClass, requestedMethodName)
except Exception as e:
    config.Controller.InexistantRequest()

result = methodToCall()

print(result)
