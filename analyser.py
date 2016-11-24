import os
import pandas as pd
import math

datapath = '.\data'

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


if __name__ == "__main__":
    cusize = [8,16,32,64]
    for size in cusize:
        print 'current size:',size
        for df,filepath in loadDataBySize(size):
            df = calMvDiff(df,filepath,save=1)

