import os
import pandas as pd

datapath = './data/costdata'


def loadToDf(filepath,sample=-1):
    infoSet = {}
    datacount = 0
    mergeInfoFlag = 0
    for i, line in enumerate(open(filepath, 'r')):
        line = line.strip('\n')
        lineList = line.split(',')
        flag = lineList[0]

        if flag == '$':
            if i != 0:
                datacount += 1
                if sample != -1:
                    if datacount == sample:
                        break

            if 'poc' not in infoSet.keys():
                infoSet['poc'] = []
                infoSet['poc'].append(int(lineList[1]))
            else:
                infoSet['poc'].append(int(lineList[1]))
            if 'cusize' not in infoSet.keys():
                infoSet['cusize'] = []
                infoSet['cusize'].append(int(lineList[2]))
            else:
                infoSet['cusize'].append(int(lineList[2]))

            if 'ps' not in infoSet.keys():
                infoSet['ps'] = []
                infoSet['ps'].append(int(lineList[3]))
            else:
                infoSet['ps'].append(int(lineList[3]))

            if 'puIdx' not in infoSet.keys():
                infoSet['puIdx'] = []
                infoSet['puIdx'].append(int(lineList[4]))
            else:
                infoSet['puIdx'].append(int(lineList[4]))
            mergeCost = lineList[5]
            if mergeCost ==  '4294967295':
                mergeCost = -1
            if 'mergeCost' not in infoSet.keys():
                infoSet['mergeCost'] = []
                infoSet['mergeCost'].append(int(mergeCost))
            else:
                infoSet['mergeCost'].append(int(mergeCost))

        if flag == 'C':
            if 'NormalMC' not in infoSet.keys():
                infoSet['NormalMC'] = []
                infoSet['NormalMC'].append(int(lineList[1]))
            else:
                infoSet['NormalMC'].append(int(lineList[1]))
            if 'bitype' not in infoSet.keys():
                infoSet['bitype'] = []
                infoSet['bitype'].append(int(lineList[2]))
            else:
                infoSet['bitype'].append(int(lineList[2]))

            cost0 = lineList[3]
            if cost0 == '4294967295':
                cost0 = -1
            if 'cost0' not in infoSet.keys():
                infoSet['cost0'] = []
                infoSet['cost0'].append(int(cost0))
            else:
                infoSet['cost0'].append(int(cost0))

            cost1 = lineList[4]
            if cost1 == '4294967295':
                cost1 = -1
            if 'cost1' not in infoSet.keys():
                infoSet['cost1'] = []
                infoSet['cost1'].append(int(cost1))
            else:
                infoSet['cost1'].append(int(cost1))

            costbi = lineList[5]
            if costbi == '4294967295':
                costbi = -1
            if 'costBi' not in infoSet.keys():
                infoSet['costBi'] = []
                infoSet['costBi'].append(int(costbi))
            else:
                infoSet['costBi'].append(int(costbi))

            if 'merFlag' not in infoSet.keys():
                infoSet['merFlag'] = []
            if lineList[6] == 'Merge':
                infoSet['merFlag'].append(1)
            else:
                infoSet['merFlag'].append(0)
        if flag == "N":
            if 'leftExist' not in infoSet.keys():
                infoSet['leftExist'] = []
                infoSet['leftExist'].append(int(lineList[1]))
            else:
                infoSet['leftExist'].append(int(lineList[1]))

            if 'leftCost' not in infoSet.keys():
                infoSet['leftCost'] = []
                infoSet['leftCost'].append(int(lineList[2]))
            else:
                infoSet['leftCost'].append(int(lineList[2]))

            if 'leftMerge' not in infoSet.keys():
                infoSet['leftMerge'] = []
                infoSet['leftMerge'].append(int(lineList[3]))
            else:
                infoSet['leftMerge'].append(int(lineList[3]))

            if 'aboveExist' not in infoSet.keys():
                infoSet['aboveExist'] = []
                infoSet['aboveExist'].append(int(lineList[4]))
            else:
                infoSet['aboveExist'].append(int(lineList[4]))

            if 'aboveCost' not in infoSet.keys():
                infoSet['aboveCost'] = []
                infoSet['aboveCost'].append(int(lineList[5]))
            else:
                infoSet['aboveCost'].append(int(lineList[5]))

            if 'aboveMerge' not in infoSet.keys():
                infoSet['aboveMerge'] = []
                infoSet['aboveMerge'].append(int(lineList[6]))
            else:
                infoSet['aboveMerge'].append(int(lineList[6]))

    feaLen = []
    for key in infoSet.keys():
        feaLen.append(len(infoSet[key]))
    for x in feaLen:
        if feaLen[0] != x:
            print "Feather amount error!"
            exit(1)
    datadf = pd.DataFrame.from_dict(infoSet)
    return datadf


def saveDataToFiles(filepath):
    filename = filepath.split('_')[1]
    savepath = os.path.join(datapath,filename)
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    df = loadToDf(filepath)

    paraset = [64,32,16,8]
    for item in paraset:
        df_sel = df[df['cusize'] == item]
        df_sel.index = range(df_sel.shape[0])
        w_name = 'cu'+str(item)+'.txt'
        df_sel.to_csv(os.path.join(savepath,w_name))

if __name__ == '__main__':
    files = []
    for name in os.listdir(datapath):
        ext = os.path.splitext(name)[1]
        if ext != '':
            files.append(name)

    for i,filename in enumerate(files):
        print str(i+1)+'.'+filename
        filepath = os.path.join(datapath,filename)
        saveDataToFiles(filepath)
