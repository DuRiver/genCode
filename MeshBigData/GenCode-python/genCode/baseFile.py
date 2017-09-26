# coding=utf-8

import os


class fileBase(object):
    def __init__(self, csvPath=os.getcwd()):
        self.csvPath = csvPath
        self._chlids = os.walk(csvPath)
        self._dirPath = []
        self._dirNames = []
        self._fileNames = []
        for dirs, dirnames, files in self._chlids:
            self._dirPath.append(dirs)
            self._dirNames.append(dirnames)
            self._fileNames.append(files)

    def getDirPath(self):
        return self._dirPath

    def getDirNames(self):
        return self._dirNames

    def getFileNames(self):
        return self._fileNames
    