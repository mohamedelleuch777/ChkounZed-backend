#!/usr/bin/env python
import config
import php


requestedClassName = config.REQUEST_URL.split('/')[1]
requestedMethodName = config.REQUEST_URL.split('/')[2]
requestedArgs = config.REQUEST_ARGS



requestedController = config.importModule("controllers/"+requestedClassName.lower()+".py")
requestedClass = getattr(requestedController, requestedClassName)
myClass = requestedClass()
methodToCall = getattr(myClass, requestedMethodName)

result = methodToCall()

print(result)
