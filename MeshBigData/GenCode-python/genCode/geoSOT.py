# coding=utf-8

import os
# import ctypes as ct
import ctypes as cp 


class getDll(object):
    def __init__(self):
        
        self.__cwd = os.getcwd()
        geoSotPath = os.path.join(self.__cwd, 'GeoSOT.dll')
        self.__geoDll = cp.cdll.LoadLibrary(geoSotPath)

    # def gDll(self, x, y, l):
        # return(str(x) + '.' + str(y) + ':level: ' + str(l))
    
    def gDllGetCode(self):
        rs = self.__geoDll.getGCode2DOfPoint(24.44, 55.33, 12)
        return rs

    # gDll = property(lambda gd: gd.__geoDll)

gd = getDll()
rs = gd.gDllGetCode()
print(rs)
