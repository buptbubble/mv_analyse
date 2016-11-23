import os
import pandas as pd

datapath = '.\data'

def loadData(cusize = 16):
    paths = []
    datafiles = os.listdir(datapath)
    for item in datafiles:
        path = os.path.join(datapath,item)
        if os.path.isdir(path):
            paths.append(path)

    filename = 'cu'+str(cusize)+'.txt'
    for path in paths:
        print path
        filepath = os.path.join(path,filename)
        df = pd.read_csv(filepath,index_col=0)
        yield df



if __name__ == "__main__":
    for df in loadData():
        print df
        break