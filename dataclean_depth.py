import os
import pandas as pd
import math


datapath = './data/depthdata'

def getRatio(df1, df2):
    rate = df1.shape[0]*1.0/df2.shape[0]
    return rate

def data_analyser(path):
    df = pd.read_csv(filepath,names=['tag','leftExist','leftDepth'\
        ,'aboveExist','aboveDepth','0','1','2','3'])
    df_LA = df[(df['leftExist']==1)& (df['aboveExist']==1)&(df['aboveExist']==1)]
    df_LA['aveDepth'] = (df_LA['leftDepth']+df_LA['aboveDepth'])/2
    resultRatio = []
    for i in range(4):
        resultRatio.append(list())
    for i,item in df_LA.iterrows():
        #print 'Row:',i
        depthlist = [0,1,2,3]
        depthDiff = [abs(x-item["aveDepth"]) for x in depthlist]
        diffDict = {}

        for i,key in enumerate(depthlist):
            diffDict[key] = depthDiff[i]
        dict = sorted(diffDict.iteritems(),key=lambda d:d[1])
        depthSort = [x[0] for x in dict]

        totalPart = item['0']+item['1']+item['2']+item['3']
        for i,depth in enumerate(depthSort):
            rate = item[str(depth)]*1.0/totalPart

            resultRatio[i].append(rate)
        #print resultRatio
    print path
    sumRatio = 0
    for i,item in enumerate(resultRatio):
        aveRatio = sum(item)/len(item)
        sumRatio +=aveRatio
        print i,'.',sumRatio







if __name__ == '__main__':
    files = []
    for name in os.listdir(datapath):
        ext = os.path.splitext(name)[1]
        if ext != '':
            files.append(name)

    for i,filename in enumerate(files):
        print str(i+1)+'.'+filename
        filepath = os.path.join(datapath,filename)
        data_analyser(filepath)

