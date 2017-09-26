# codieng=utf-8

import os
import re
import geoSOT
import CSVHelper as ch
import FileHelper as fh


class genCode(object):
    def __init__(self, outputpath=None):
        self.outputpath = outputpath
        self.outpathset = True

    def __generCode(self, lon, let, level):
        gDll = geoSOT.getDll().gDll
        le = gDll(lon, let, level)
        return(le)

    def __levelToList(self, level):
        lev = re.split(r'-', level)
        if(len(lev) > 1):
            return(list(range(int(lev[0]), int(lev[1])+1)))
        elif len(lev) == 1:
            return([int(lev[0])])
        else:
            print('Wrong level input!')
            return

    def __treatCsvFile(self, filepath, lon, let, level):
        fl = fh.fileHelper()
        csvLines = fl.readFile(filepath)
        codeLines = []
        if(self.outputpath is None):
            self.outputpath = os.path.dirname(filepath)
            self.outpathset = False
        elif not self.outpathset:
            self.outputpath = os.path.dirname(filepath)
        for i in range(len(csvLines)):
            codeLines.append([])
            line = list(fl.reSplit(csvLines[i]))
            lont, letu = line[lon], line[let]
            lev = self.__levelToList(level)
            codeLines[i] = list.copy(line)
            for j in range(len(lev)):
                if(i == 0):
                    codeLines[i].append(' level:' + str(lev[j]))
                else:
                    codeLines[i].append(
                        str(self.__generCode(lont, letu, lev[j])))
        codeLines = map(lambda line: ','.join(line), codeLines)
        return list(codeLines)

    def genCodes(self, lon=0, let=1, levle='1-6'):
        csv = ch.csvHelper('/home/river/mypyProj/input')
        fl = fh.fileHelper()
        sourceFlies = csv.getCsvFiles()
        for csvf in sourceFlies:
            for k in range(len(csvf)):
                codeLines = self.__treatCsvFile(csvf[k], lon, let, levle)

                fl.writeToFile(codeLines, fl.getOutPutPath(
                    self.outputpath, 'output_' + os.path.basename(csvf[k])))

# gc = genCode('/home/river/mypyProj/out/')
# gc.genCodes()