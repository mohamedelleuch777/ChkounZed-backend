import sys
import os
import importlib
import json
import php
from cryptography.fernet import Fernet
import base64


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
    sys.exit()


class Controller:
    def ForceMethod(self, methodType):
        if REQUEST_TYPE != methodType:
            ThrowException('This method only accept '+methodType+' requests')
    
    @staticmethod
    def BlockRequests():
        ThrowException('This method is not callable')
    
    @staticmethod
    def InexistantRequest():
        ThrowException('This method does not exist')

    def GetParam(self, paramName):
        params = REQUEST_ARGS.split('&')
        for item in params:
            if item.startswith(paramName):
                return item.split('=')[1]
        return None
    
    def GetBearerToken(self):
        # HTTP_AUTHORIZATION
        jsonHeaders = json.loads(REQUEST_HEADERS)
        try:
            return jsonHeaders['HTTP_AUTHORIZATION']
        except:
            # fix this function
            # php.run("http_response_code(401);die;")
            print("401")
            sys.exit()

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


class Cryptography:

    @staticmethod
    def Encrypt(string, key):
        return Fernet(key).encrypt(string)
    
    @staticmethod
    def Decrypt(token, key):
        return Fernet(key).decrypt(token)

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





