import os
import pandas as pd
import math
from matplotlib import pyplot as plt

datapath = '.\data'

def getFilterRate(df1,df2):
    rate = df1.shape[0]*1.0/df2.shape[0]
    return rate


def loadDataBySize(cusize = 8):
    paths = []
    datafiles = os.listdir(datapath)
    for item in datafiles:
        path = os.path.join(datapath,item)
        if os.path.isdir(path):
            paths.append(path)

    filename = 'cu'+str(cusize)+'.txt'
    for path in paths:

        filepath = os.path.join(path,filename)
        print filepath
        filesize = os.path.getsize(filepath)/1024 ** 2
        print 'Filesize:',filesize,'MB'
        df = pd.read_csv(filepath,index_col=0)
        yield df,filepath


def calMvDiff(df,savepath,save = 0):
    mvdiff = []
    for i, row in df.iterrows():
        l0Diff = -1
        l1Diff = -1
        if row['leftL0Poc'] != -1 and row['aboveL0Poc'] != -1:
            l0Diff = math.sqrt(
                (row['leftL0MvX'] - row['aboveL0MvX']) ** 2 + (row['leftL0MvY'] - row['aboveL0MvY']) ** 2)
        if row['leftL1Poc'] != -1 and row['aboveL1Poc'] != -1:
            l1Diff = math.sqrt(
                (row['leftL1MvX'] - row['aboveL1MvX']) ** 2 + (row['leftL1MvY'] - row['aboveL1MvY']) ** 2)

        if l0Diff == -1 and l1Diff != -1:
            l0Diff = l1Diff
        if l0Diff != -1 and l1Diff == -1:
            l1Diff = l0Diff

        mvdiff.append((l0Diff + l1Diff) * 1.0 / 2)
    df['mvdiff'] = mvdiff
    if save == 1:
        df.to_csv(savepath)
    return df

def mergeAnalyser(data,filepath):
    data_mvd_large0 = data[data['mvdiff'] >= 0]
    print 'Filter rate:', data_mvd_large0.shape[0] * 1.0 / data.shape[0]

    dataMerge = data_mvd_large0[data_mvd_large0['merFlag'] == 1]
    dataNotMerge = data_mvd_large0[data_mvd_large0['merFlag'] == 0]
    mvDiffMerge = dataMerge['mvdiff']
    mvDiffNotMerge = dataNotMerge['mvdiff']


    titleText = "path:" + filepath + " "
    p1 = plt.subplot(211)
    p1.hist(mvDiffMerge, bins=50, range=(0, 20))

    p1.set_title(titleText + 'Merge')

    p2 = plt.subplot(212)
    p2.hist(mvDiffNotMerge, bins=50, range=(0, 20))
    p2.set_title('Not Merge')
    p2.set_xlabel('MV Diffence')
    p2.set_ylabel('Hits')
    plt.show()

def biPredAnalyser(data,filepath):
    dataUni = data[data['biType'] =='u']
    dataBi = data[data['biType'] == 'b']
    print 'Bi rate total:',getFilterRate(dataBi,data)

    dataLeftBi = data[(data['leftL0Poc']!=-1) & (data['leftL1Poc']!=-1)]
    print 'Left Bi rate:', getFilterRate(dataLeftBi, data)
    dataAboveBi = data[(data['aboveL0Poc']!=-1) & (data['aboveL1Poc']!=-1)]
    print 'Above Bi rate:', getFilterRate(dataAboveBi, data)
    dataLABi = data[(data['leftL0Poc']!=-1) & (data['leftL1Poc']!=-1) & (data['aboveL0Poc']!=-1) & (data['aboveL1Poc']!=-1)]
    print 'Left Above Bi rate:',getFilterRate(dataLABi,data)
    print '-------------------------------'

    dataAboveBi_Bi = dataAboveBi[dataAboveBi['biType'] == 'b']
    dataAboveBi_Uni = dataAboveBi[dataAboveBi['biType'] == 'u']
    print 'AboveBi_Bi:',getFilterRate(dataAboveBi_Bi,dataAboveBi)
    print 'AboveBi_Uni:',getFilterRate(dataAboveBi_Uni,dataAboveBi)

    dataLeftBi_Bi = dataLeftBi[dataLeftBi['biType'] == 'b']
    dataLeftBi_Uni = dataLeftBi[dataLeftBi['biType'] == 'u']
    print 'LeftBi_Bi:', getFilterRate(dataLeftBi_Bi, dataLeftBi)
    print 'LeftBi_Uni:', getFilterRate(dataLeftBi_Uni, dataLeftBi)

    dataLABi_Bi = dataLABi[dataLABi['biType'] == 'b']
    dataLABi_Uni = dataLABi[dataLABi['biType'] == 'u']
    print 'LA Bi_Bi:', getFilterRate(dataLABi_Bi, dataLABi)
    print 'LA Bi_Uni:', getFilterRate(dataLABi_Uni, dataLABi)




if __name__ == "__main__":
    #cusize = [8,16,32,64]
    cusize = [16]
    for size in cusize:
        print 'current size:',size
        for df,filepath in loadDataBySize(size):
            #mergeAnalyser(df,filepath)
            biPredAnalyser(df,filepath)
            break

