import sys
import re
import string


print(sys.path[0])
with open(sys.path[0] + '\geosot_2d.h', encoding='utf-8') as f:
    with open(sys.path[0] + '\geosot_2d.py', 'w', encoding='utf-8') as f1:
        for line in f.readlines():

            if line.startswith('GEOSOT_2D_API'):
                f1.write('\n')
                words = re.split(r'\(', line)
                car = re.split(r'[ *]', words[0])
                car = list(filter(lambda x: x != '', car))
                cdr = re.split(r',', words[1])
                _no, *st, name = car
                cdr = list(map(lambda x: x.strip(');\n'), cdr))

                paramStr = ''
                for parm in cdr:
                    pa = re.split(r' *', parm)
                    paramStr += pa[-1]
                    paramStr += ', '
                paramStr = paramStr.rstrip(', ')
                if len(st) > 1:
                    reType = ' '.join(st)
                    if reType == 'unsigned long long':
                        reType = 'ctypes.c_ulonglong'
                    elif reType == 'bool':
                        reType = 'ctypes.c_bool'
                    elif reType == 'int':
                        reType = 'ctypes.c_int'
                    elif reType == 'double':
                        reType = 'ctypes.c_double'
                    elif reType == 'Direction':
                        reType = 'ctypes.c_int'
                else:
                    reType = st[0]

                argtypes = '('
                if len(cdr) > 0:
                    argtypes += cdr[0]
                    argtypes += ',)'

                # words = re.split(r'[ *();\n]', line)
                # words = list(filter(lambda x: x not in string.punctuation, words))
                # words = list(map(str.strip(string.punctuation), words))
                # param = words[3:]
                # param = param[::2]

                line1 = 'def ' + name + '(' + paramStr + '):'
                f1.write(line1)
                f1.write('\n')
                line2 = '    libc.' + name + '.argtypes = ' + argtypes
                f1.write(line2)
                f1.write('\n')
                line3 = '    libc.' + name + '.restype = ' + reType
                f1.write(line3)
                f1.write('\n')
                f1.write('# ' + line)

            else:
                f1.write(line)
