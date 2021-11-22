import sys
import os
import importlib
import json
import php
from cryptography.fernet import Fernet


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


class Cryptography:

    @staticmethod
    def Encrypt(string, key):
        return Fernet(key).encrypt(string)
    
    @staticmethod
    def Decrypt(token, key):
        return Fernet(key).decrypt(token)



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


def GetPostArgs():
    f = open("php.input", "r")
    return f.read()



