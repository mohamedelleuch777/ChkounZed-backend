import sys
import os
import importlib


prodMode = True

if prodMode:
    REQUEST_TYPE = sys.argv[1]
    REQUEST_URL = sys.argv[2]
    REQUEST_ARGS = sys.argv[3]
else:
    REQUEST_TYPE = "GET"
    REQUEST_URL = "/Users/run"
    REQUEST_ARGS = 'ytd=ewgw&FAFS'


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