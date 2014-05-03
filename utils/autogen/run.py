#!/usr/bin/python
import sys
import os
import CppHeaderParser

from config      import *
from genJsApi    import *
#from genJsApiMap import *
from genC        import *

def ParseHeader(name):
  try:
    printDbg("parsing " + name)
    cppHeader = CppHeaderParser.CppHeader(name)    
    return cppHeader

  except CppHeaderParser.CppParseError,  e:
    printDbg(e)
    sys.exit(1)

def HandleHeader(root, f):
  split = f.rsplit('.', 1)

  #only .h file is wanted
  if(split[1] != 'h'):
    printDbg(f + ' is not header file')
    return

  if f == "version_export.h":
    fcpp = root + "/version_export.cpp"
    os.system("cp " + fcpp + " " + OUTPUT_DEV_PATH)

  # init debug output
  SetPrintModule(f)

  cppHeader = ParseHeader(root + "/" + f);  

  #to handle the override functions
  for c in cppHeader.classes:
    FormalizeFunc(cppHeader.classes[c]["methods"]["public"])
    GroupFunc(cppHeader.classes[c]["methods"]["public"])    

  FormalizeFunc(cppHeader.functions)
  GroupFunc(cppHeader.functions)

  #GenJsApiMap(split[0], cppHeader)
  GenJsApi(split[0], cppHeader)
  GenC(split[0], cppHeader)
  
  UnsetPrintModule()

if __name__ == "__main__":

  GenPreGlobalInit()
  GenPreFuncJsApi()
  GenPreFuncJsApiMap()

  for p in INPUT_DECL_PATHS:
    printDbg("searching " + p)
    for root, dirs, files in os.walk(p):
      for f in files:
        HandleHeader(root, f)

  GenPostFuncJsApi();
  GenPostFuncJsApiMap();
  GenPostGlobalInit()
  GenGyp()
  DumpSummary()
