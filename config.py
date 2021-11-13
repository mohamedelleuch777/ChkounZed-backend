import sys
import os
import importlib



if __debug__:
    REQUEST_TYPE = "DEBUG"
    REQUEST_URL = "DEBUG"
    REQUEST_ARGS = "DEBUG"
    REQUEST_TYPE = "GET"
    REQUEST_URL = "/Users/run?ytd=ewgw&FAFS"
    REQUEST_ARGS = ""
else:
    REQUEST_TYPE = sys.argv[1]
    REQUEST_URL = sys.argv[2].split('?')[0]
    REQUEST_ARGS = ''
    if len(sys.argv[2].split('?')) >= 2:
        REQUEST_ARGS = sys.argv[2].split('?')[1]

print(REQUEST_ARGS)

# if len(REQUEST_URL.split('?')) >= 2:
#     REQUEST_ARGS = REQUEST_URL.split('?')[1]
# else:
#     REQUEST_ARGS = ""


def importModule1(moduleName):
    try:
        module = __import__(moduleName)
    except ImportError:
        return None
    return module


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