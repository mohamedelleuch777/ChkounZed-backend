from logging import error
import sys
import os
import importlib
import time
import json
import php
#from cryptography.fernet import Fernet
import base64
import random
import os
import constants


prodMode = True


if prodMode:
    REQUEST_TYPE = sys.argv[1]
    REQUEST_URL = sys.argv[2]
    REQUEST_ARGS = sys.argv[3]
    file = open("headers.input", "r")
    REQUEST_HEADERS = file.read()
else:
    REQUEST_TYPE = "GET"
    REQUEST_URL = "/Users/Login"
    REQUEST_ARGS = 'username=user1&password=hello'
    file = open("debug_header.input", "r")
    REQUEST_HEADERS = file.read()


def ThrowException(str):
    print(str)
    sys.exit() # quit  with raising an exception
    #os._exit(0) # quit immediately without raising an exception

def set_bit(val, index, x):
  # """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
  mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
  val &= ~mask          # Clear the bit indicated by the mask (if x is False)
  if x:
    val |= mask         # If x was True, set the bit indicated by the mask.
  return val            # Return the result, we're done.

def ReturnJsonError(message, error_code = None):
    err_code = "200"
    if error_code:
        core = {
                    "success": False,
                    "message": str(message),
                    "code": error_code
                }
        err_code = error_code
    else:
        core = {
                    "success": False,
                    "message": str(message)
                }
    parsedCore = json.dumps(core)
    print(str(err_code)+parsedCore)
    sys.exit() # quit  with raising an exception

def GetFlagValue(user_status, flag):
        return user_status & flag

def isFlagActive(user_status, flag):
    return user_status & flag == flag



class Controller:
    def ForceMethod(self, methodType):
        if REQUEST_TYPE != methodType:
            ReturnJsonError('This method only accept '+methodType+' requests')
    
    @staticmethod
    def BlockRequests():
        ReturnJsonError('This method is not callable',500)
    
    @staticmethod
    def InexistantRequest():
        ReturnJsonError('This method does not exist',404)

    def GetParam(self, paramName):
        params = REQUEST_ARGS.split('&')
        for item in params:
            if item.startswith(paramName):
                return item.split('=')[1]
        return None
    
    def GetBearerToken(self):
        # HTTP_AUTHORIZATION
        jsonHeaders = json.loads(REQUEST_HEADERS)
        error = {
                    "success": False,
                    "message": 'The auth token was expired!'
                }
        parsedError = json.dumps(error)
        try:
            bearerToken = jsonHeaders['HTTP_AUTHORIZATION']
            #ThrowException("401"+bearerToken)
            if self.CheckTokenValidity(bearerToken):
                return bearerToken.split(' ')[1]
            else:
                
                ReturnJsonError('401'+parsedError)
        except:
            # fix this function
            # php.run("http_response_code(401);die;")
            ReturnJsonError('401'+parsedError)

    def CheckTokenValidity(self, token):
        try:
            expiration = self.GetDataFromToken(token.split(' ')[1],'expiration')
            ts = int(time.time() * 1000)
            if( int(expiration) < int(ts) )or( expiration == None ):
                return False # not valid token or expired
            return True # valid token and not expired
        except:
            return False

    def GetDataFromToken(self, token, key):
        try:
            decodedToken = Cryptography.Decode64(token)
            json_object = json.loads(decodedToken)
            return json_object[key]
        except:
            return None

    def DecodeToken(self, token, paramName):
        data = Cryptography.Decrypt(token)
        return data[paramName]
    
    def Convert2Json(self, tuple):
        if len(tuple)==2:
            if tuple[1] == "true" or tuple[1] == "false":
                pass

    def GetPostArgs(self, argName=None):
        f = open("php.input", "r")
        obj = f.read()
        postArgs = json.loads(obj)
        if argName:
            return postArgs[argName]
        else:
            return postArgs

    def GetGetArgs(self, argName=None):
        arrArgs = REQUEST_ARGS.split('&')
        if argName:
            for i in range(0,len(arrArgs)):
                arg = arrArgs[i]
                if arg.split('=')[0] == argName:
                    return arg.split('=')[1]
            return None
        else:
            return arrArgs

    




class Cryptography:

    # @staticmethod
    # def Encrypt(string, key):
    #     return Fernet(key).encrypt(string)
    
    # @staticmethod
    # def Decrypt(token, key):
    #     return Fernet(key).decrypt(token)

    @staticmethod
    def Encode64(message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message
    
    @staticmethod
    def Decode64(base64_message):
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message



def importModule(full_path_to_module):
    # module_dir, module_file = os.path.split(full_path_to_module)
    # module_name, module_ext = os.path.splitext(module_file)
    # sys.path.insert(0, module_dir)
    # module_obj = importlib.import_module(module_name)
    # module_obj.__file__ = full_path_to_module
    # globals()[module_name] = module_obj
    # return module_obj


    #ReturnJsonError(str(module_obj)+"___"+str(module_obj.__file__ ))
    try:
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
        sys.path.insert(0, module_dir)
        module_obj = importlib.import_module(module_name)
        module_obj.__file__ = full_path_to_module
        globals()[module_name] = module_obj
    except Exception as e:
        # raise ImportError(e)
        return None
    return module_obj





