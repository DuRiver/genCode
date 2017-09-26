# coding=utf-8

import os
import baseFile
# import glob


class csvHelper(baseFile.fileBase):
    def __init__(self, csvPath=os.getcwd()):
        super(csvHelper, self).__init__(csvPath)
        self._dirPath = self.getDirPath()
        self._fileNames = self.getFileNames()

    def getCsvFiles(self):
        filePaths = []
        for i in range(len(self._dirPath)):
            filePaths.append([])
            for j in range(len(self._fileNames[i])):
                if(self._fileNames[i][j].endswith(('.csv', '.CSV', '.txt', '.TXT'))):
                    filePaths[i].append(os.path.join(
                        self._dirPath[i], self._fileNames[i][j]))
        return (filepath for filepath in filePaths)


"""
csv = csvHelper('/home/river/mypyProj/input/')
csvfiles = csv.getCsvFiles()    
di = csv.getDirPath()   
print(di)
na = csv.getFileNames()
print(na)
print(list(csvfiles))
"""
