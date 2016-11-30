# -*- coding: utf-8 -*

import os
import pandas as pd
import math
from matplotlib import pyplot as plt
import copy

datapath = '.\data\costdata'
picsfolder = '.\pics'

def getRatio(df1, df2):
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
        filepathC = filepath.split('\\')
        seqName = filepathC[-2]
        filesize = os.path.getsize(filepath) / 1024 ** 2
        print 'Seq.Name:',seqName,'\tCU Width:',cusize,'\tFilesize:',filesize,'MB'
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
    print 'Bi rate total:',getRatio(dataBi, data)

    dataLeftBi = data[(data['leftL0Poc']!=-1) & (data['leftL1Poc']!=-1)]
    print 'Left Bi rate:', getRatio(dataLeftBi, data)
    dataAboveBi = data[(data['aboveL0Poc']!=-1) & (data['aboveL1Poc']!=-1)]
    print 'Above Bi rate:', getRatio(dataAboveBi, data)
    dataLABi = data[(data['leftL0Poc']!=-1) & (data['leftL1Poc']!=-1) & (data['aboveL0Poc']!=-1) & (data['aboveL1Poc']!=-1)]
    print 'Left Above Bi rate:',getRatio(dataLABi, data)
    print '-------------------------------'

    dataAboveBi_Bi = dataAboveBi[dataAboveBi['biType'] == 'b']
    dataAboveBi_Uni = dataAboveBi[dataAboveBi['biType'] == 'u']
    print 'AboveBi_Bi:',getRatio(dataAboveBi_Bi, dataAboveBi)
    print 'AboveBi_Uni:',getRatio(dataAboveBi_Uni, dataAboveBi)

    dataLeftBi_Bi = dataLeftBi[dataLeftBi['biType'] == 'b']
    dataLeftBi_Uni = dataLeftBi[dataLeftBi['biType'] == 'u']
    print 'LeftBi_Bi:', getRatio(dataLeftBi_Bi, dataLeftBi)
    print 'LeftBi_Uni:', getRatio(dataLeftBi_Uni, dataLeftBi)

    dataLABi_Bi = dataLABi[dataLABi['biType'] == 'b']
    dataLABi_Uni = dataLABi[dataLABi['biType'] == 'u']
    print 'LA Bi_Bi:', getRatio(dataLABi_Bi, dataLABi)
    print 'LA Bi_Uni:', getRatio(dataLABi_Uni, dataLABi)

#选出当前mv与左边mv相同的数据
    dataEqLeft = data[((data['l0_mvx'] == data['leftL0MvX']) & (data['l0_mvy'] == data['leftL0MvY']))| \
          ((data['l1_mvx'] == data['leftL1MvY']) & (data['l1_mvy'] == data['leftL1MvY']) )]
    dataEqAbove = data[((data['l0_mvx'] == data['aboveL0MvX']) & (data['l0_mvy'] == data['aboveL0MvY'])) | \
                      ((data['l1_mvx'] == data['aboveL1MvY']) & (data['l1_mvy'] == data['aboveL1MvY']))]
    print 'EqLeft:',getRatio(dataEqLeft, data)
    print 'EqAbove:', getRatio(dataEqAbove, data)



def mergeCostAnalyser(df,filepath):
    data_notmerge = df[(df['NormalMC'] == 1) & (df['merFlag'] == 0) & (df['mergeCost'] >=0)]
    data_merge = df[(df['NormalMC'] == 1) & (df['merFlag'] == 1) & (df['mergeCost'] >= 0)]


    data_nm_mCost = data_notmerge['mergeCost']
    data_m_mCost = data_merge['mergeCost']

    p1 = plt.subplot(211)
    p1.hist(data_m_mCost, bins=50,range=(0,500))
    p1.set_title(filepath + '\n'+'Merge')

    p2 = plt.subplot(212)
    p2.hist(data_nm_mCost, bins=50,range=(0,500))
    p2.set_title('Not Merge')
    p2.set_xlabel('MV Diffence')
    p2.set_ylabel('Hits')
    plt.show()

def neighborAnalyser(df,filepath):
    print '\n'
    print 'Assuming left CU is merge mode:'
    for partsize in range(4):
        df_leftMerge_Normal = df[(df['NormalMC'] == 1) & (df['leftMerge'] == 1) & (df['ps'] == partsize)]
        df_Normal = df[(df['NormalMC'] == 1) & (df['ps'] == partsize)]


        if df_leftMerge_Normal.shape[0] == 0:
            print 'PartSize=',partsize,' None.'
            continue
        assert df_leftMerge_Normal.shape[0]!=0
        dfMerge_leftM = df_leftMerge_Normal[df_leftMerge_Normal['merFlag']==1]
        dfMerge_Normal = df_Normal[df_Normal['merFlag']==1]
        rate_LMerge = getRatio(dfMerge_leftM, df_leftMerge_Normal)
        rate_Merge = getRatio(dfMerge_Normal, df_Normal)
        rate_filter = getRatio(df_leftMerge_Normal, df_Normal)
        print 'PartSize:', partsize
        print '\trate_LMerge:',rate_LMerge
        print '\trate_Merge:', rate_Merge
        print '\tFilter rate:',rate_filter

    print '\n'
    print 'Assuming above CU is merge mode:'
    for partsize in range(4):
        df_rightMerge_Normal = df[(df['NormalMC'] == 1) & (df['rightMerge'] == 1) & (df['ps'] == partsize)]
        df_Normal = df[(df['NormalMC'] == 1) & (df['ps'] == partsize)]

        if df_rightMerge_Normal.shape[0] == 0:
            print 'PartSize=:', partsize, ' None.'
            continue
        assert df_rightMerge_Normal.shape[0] != 0
        dfMerge_rightM = df_rightMerge_Normal[df_rightMerge_Normal['merFlag'] == 1]
        dfMerge_Normal = df_Normal[df_Normal['merFlag'] == 1]
        rate_AMerge = getRatio(dfMerge_rightM, df_rightMerge_Normal)
        rate_Merge = getRatio(dfMerge_Normal, df_Normal)
        rate_filter = getRatio(df_rightMerge_Normal, df_Normal)
        print 'PartSize:', partsize
        print '\trate_AMerge:', rate_AMerge
        print '\trate_Merge:', rate_Merge
        print '\tFilter rate:', rate_filter

    print '\n'
    print 'Assuming both above and left CU is merge mode:'
    for partsize in range(4):
        df_LAMerge_Normal = df[(df['NormalMC'] == 1) & (df['rightMerge'] == 1)&(df['leftMerge'] == 1) & (df['ps'] == partsize)]
        df_Normal = df[(df['NormalMC'] == 1) & (df['ps'] == partsize)]

        if df_LAMerge_Normal.shape[0] == 0:
            print 'PartSize=:', partsize, ' None.'
            continue

        dfMerge_LAMerge = df_LAMerge_Normal[df_LAMerge_Normal['merFlag'] == 1]
        dfMerge_Normal = df_Normal[df_Normal['merFlag'] == 1]
        rate_LAMerge = getRatio(dfMerge_LAMerge, df_LAMerge_Normal)
        rate_Merge = getRatio(dfMerge_Normal, df_Normal)
        rate_filter = getRatio(df_LAMerge_Normal, df_Normal)
        print 'PartSize:', partsize
        print '\trate_LAMerge:', rate_LAMerge
        print '\trate_Merge:', rate_Merge
        print '\tFilter rate:', rate_filter



def neighborCostAnalyser(df,filepath):
    df_LAexist = df[(df['NormalMC'] == 1) & (df['leftExist'] == 1) & (df['rightExist'] == 1) &(df['mergeCost'] != -1)]
    templist = copy.deepcopy(list(((df_LAexist['leftCost']+df_LAexist['rightCost'])/2).values))
    df_LAexist['aveLAcost'] = templist

    df_totalMerge = df_LAexist[df_LAexist['merFlag']==1]

    mergedRatioList = []
    precisionRatioList = []
    recallRatioList = []
    multiFactorList = []

    cusize = df.loc[0]['cusize']
    seqName = filepath.split('\\')[-2]
    for step in range(20):
        multiFactor = 0.5+0.1*step
        multiFactorList.append(multiFactor)
        df_costLessLA = df_LAexist[df_LAexist['mergeCost'] < multiFactor * df_LAexist['aveLAcost']]
        df_realMerge = df_costLessLA[df_costLessLA['merFlag'] == 1]

        rate = getRatio(df_LAexist, df)
        # print rate,'\tLeft and right are exist, current merge cost != -1, process normal'

        mergedRatio = getRatio(df_costLessLA, df)
        mergedRatioList.append(mergedRatio)
        precisionRatio= getRatio(df_realMerge, df_costLessLA)
        precisionRatioList.append(precisionRatio)
        recallRatio = getRatio(df_realMerge,df_totalMerge)
        recallRatioList.append(recallRatio)
    plt.figure()
    plt.plot(multiFactorList,precisionRatioList,'r-',label= 'Precision Ratio')
    plt.plot(multiFactorList,recallRatioList,'g-',label='Recall Ratio')
    plt.plot(multiFactorList,mergedRatioList,'b-',label='Merged Block')
    titleText = seqName+'   width='+str(cusize)
    savename = seqName+str(cusize)+'.png'

    plt.title(titleText)
    plt.legend()
    plt.savefig(os.path.join(picsfolder, savename))



    # print mergedRatio, '\tTotal merged block'
    # print precisionRatio,'\tPrecision ratio'
    # print recallRatio,'\tRecall ratio'


    pass

if __name__ == "__main__":
    cusize = [8,16,32,64]
    #cusize = [32]
    for size in cusize:
        print 'current size:',size
        for df,filepath in loadDataBySize(size):
            #mergeCostAnalyser(df,filepath)
            neighborCostAnalyser(df, filepath)









