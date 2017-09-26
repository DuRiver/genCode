# coding=utf-8
import os
import re


class fileHelper(object):
    def __init__(self, outputpath=None):
        # super(fileHelper, self).__init__()
        self.res = re.compile(r'    | |,')

    def reSplit(self, line):
        lineList = filter(lambda x: x != '', re.split(self.res, line))
        return lineList

    def getOutPutPath(self, pathout, filename):
        output = 'output'
        outputPath = os.path.join(pathout, output)
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        return(os.path.join(outputPath, filename))

    def readFile(self, filepath):

        with open(filepath, 'r') as fs:
            filelist = fs.readlines()
        filelist = map(lambda line: line.strip('\n'), filelist)
        return list(filelist)

    def writeToFile(self, files, filepath):
        with open(filepath, 'w') as fs:
            for line in files:
                fs.write(line)
                fs.write('\n')


"""      
fh = fileHelper()
f = fh.readFile('/home/river/mypyProj/input/locations.csv')
print(f)
"""
