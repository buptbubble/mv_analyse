import os
import pandas as pd

datapath = './data'
dataname = '32_BasketballPass_416x240_50.txt'

def file_analyser(filepath):
    datadf = pd.DataFrame
    infoSet = {}
    datacount = 0
    for i,line in enumerate(open(filepath,'r')):
        line = line.strip('\n')
        lineList = line.split(',')
        flag = lineList[0]
        if flag == '$':
            if i != 0:
                if 'merFlag' not in infoSet.keys():
                    infoSet['merFlag'] = -1

                pdrecord = pd.DataFrame(infoSet,index=[0])
                if datadf.empty:
                    datadf = pdrecord.copy()
                else:
                    pd.concat(datadf,pdrecord)

                print datadf
                datacount+=1
                if datacount==5:

                    break
                infoSet.clear()
            infoSet['poc'] =lineList[1]
            infoSet['cusize'] = lineList[2]
            infoSet['ps'] = lineList[3]
            infoSet['puIdx'] = lineList[4]
        if flag == '#':
            if lineList[1] == 'uni':
                infoSet['biType'] = 'u'

            elif lineList[1] == 'non-Bi':
                infoSet['biType'] = 'm'

            elif lineList[1] == 'Bi':
                infoSet['biType'] = 'b'
        if flag == '0':
            refNum = int(lineList[1])
            infoSet['l0_mvx'] = int(lineList[2+refNum])
            infoSet['l0_mvy'] = int(lineList[3+refNum])
            infoSet['l0_refBestPoc'] = int(lineList[4+refNum])
            infoSet['l0_cost'] = int(lineList[5+refNum])
        if flag == '1':
            refNum = int(lineList[1])
            infoSet['l1_mvx'] = int(lineList[2 + refNum])
            infoSet['l1_mvy'] = int(lineList[3 + refNum])
            infoSet['l1_refBestPoc'] = int(lineList[4 + refNum])
            infoSet['l1_cost'] = int(lineList[5 + refNum])
        if flag == '&':
            if lineList[1] == 'Merge':
                infoSet['merFlag'] = 1
            if lineList[1] == 'NotMerge':
                infoSet['merFlag'] = 0










if __name__ == '__main__':
    filepath = os.path.join(datapath,dataname)
    file_analyser(filepath)