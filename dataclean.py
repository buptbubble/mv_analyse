import os
import pandas as pd

datapath = './data'
dataname = '32_BasketballPass_416x240_50.txt'

def loadToDf(filepath,sample=-1):

    infoSet = {}
    datacount = 0
    mergeInfoFlag = 0
    for i,line in enumerate(open(filepath,'r')):
        line = line.strip('\n')
        lineList = line.split(',')
        flag = lineList[0]

        if flag == '$':
            if i != 0:
                if 'merFlag' not in infoSet.keys():
                    infoSet['merFlag'] = []
                if mergeInfoFlag == 0:
                    infoSet['merFlag'].append(-1)
                mergeInfoFlag = 0
                datacount+=1
                if sample != -1:
                    if datacount==sample:
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


        if flag == '#':
            if 'biType' not in infoSet.keys():
                infoSet['biType'] = []
            #比较过后选择单项预测
            if lineList[1] == 'uni':
                infoSet['biType'].append('u')
            #没有进行双向预测
            elif lineList[1] == 'non-Bi':
                infoSet['biType'].append('m')
            #双向预测和单项预测比较过后，选择双向预测
            elif lineList[1] == 'Bi':
                infoSet['biType'].append('b')

        if flag == '0':
            refNum = int(lineList[1])
            if 'l0_mvx' not in infoSet.keys():
                infoSet['l0_mvx'] = []
                infoSet['l0_mvx'].append(int(lineList[2+refNum]))
            else:
                infoSet['l0_mvx'].append(int(lineList[2+refNum]))

            if 'l0_mvy' not in infoSet.keys():
                infoSet['l0_mvy'] = []
                infoSet['l0_mvy'].append(int(lineList[3+refNum]))
            else:
                infoSet['l0_mvy'].append(int(lineList[3+refNum]))

            if 'l0_refBestPoc' not in infoSet.keys():
                infoSet['l0_refBestPoc'] = []
                infoSet['l0_refBestPoc'].append(int(lineList[4+refNum]))
            else:
                infoSet['l0_refBestPoc'].append(int(lineList[4+refNum]))

            if 'l0_cost' not in infoSet.keys():
                infoSet['l0_cost'] = []
                infoSet['l0_cost'].append(int(lineList[5+refNum]))
            else:
                infoSet['l0_cost'].append(int(lineList[5+refNum]))


        if flag == '1':
            refNum = int(lineList[1])

            if 'l1_mvx' not in infoSet.keys():
                infoSet['l1_mvx'] = []
                infoSet['l1_mvx'].append(int(lineList[2 + refNum]))
            else:
                infoSet['l1_mvx'].append(int(lineList[2 + refNum]))

            if 'l1_mvy' not in infoSet.keys():
                infoSet['l1_mvy'] = []
                infoSet['l1_mvy'].append(int(lineList[3 + refNum]))
            else:
                infoSet['l1_mvy'].append(int(lineList[3 + refNum]))

            if 'l1_refBestPoc' not in infoSet.keys():
                infoSet['l1_refBestPoc'] = []
                infoSet['l1_refBestPoc'].append(int(lineList[4 + refNum]))
            else:
                infoSet['l1_refBestPoc'].append(int(lineList[4 + refNum]))

            if 'l1_cost' not in infoSet.keys():
                infoSet['l1_cost'] = []
                infoSet['l1_cost'].append(int(lineList[5 + refNum]))
            else:
                infoSet['l1_cost'].append(int(lineList[5 + refNum]))

        if flag == 'L0':
            if 'leftL0Poc' not in infoSet.keys():
                infoSet['leftL0Poc'] = []
            if 'leftL0MvX' not in infoSet.keys():
                infoSet['leftL0MvX'] = []
            if 'leftL0MvY' not in infoSet.keys():
                infoSet['leftL0MvY'] = []
            content = lineList[1]
            content = content.replace(" ", "")
            if content != 'none':
               # print flag,lineList[1]
                #print 'Line:',i
                infoSet['leftL0Poc'].append(int(lineList[1]))
                infoSet['leftL0MvX'].append(int(lineList[2]))
                infoSet['leftL0MvY'].append(int(lineList[3]))
            else:
                infoSet['leftL0Poc'].append(-1)
                infoSet['leftL0MvX'].append(-1)
                infoSet['leftL0MvY'].append(-1)
                
        if flag == 'L1':
            if 'leftL1Poc' not in infoSet.keys():
                infoSet['leftL1Poc'] = []
            if 'leftL1MvX' not in infoSet.keys():
                infoSet['leftL1MvX'] = []
            if 'leftL1MvY' not in infoSet.keys():
                infoSet['leftL1MvY'] = []
            content = lineList[1]
            content = content.replace(" ", "")
            if content != 'none':
                infoSet['leftL1Poc'].append(int(lineList[1]))
                infoSet['leftL1MvX'].append(int(lineList[2]))
                infoSet['leftL1MvY'].append(int(lineList[3]))
            else:
                infoSet['leftL1Poc'].append(-1)
                infoSet['leftL1MvX'].append(-1)
                infoSet['leftL1MvY'].append(-1)
                
        if flag == 'A0':
            if 'aboveL0Poc' not in infoSet.keys():
                infoSet['aboveL0Poc'] = []
            if 'aboveL0MvX' not in infoSet.keys():
                infoSet['aboveL0MvX'] = []
            if 'aboveL0MvY' not in infoSet.keys():
                infoSet['aboveL0MvY'] = []
            content = lineList[1]
            content = content.replace(" ", "")
            if content != 'none':
                infoSet['aboveL0Poc'].append(int(lineList[1]))
                infoSet['aboveL0MvX'].append(int(lineList[2]))
                infoSet['aboveL0MvY'].append(int(lineList[3]))
            else:
                infoSet['aboveL0Poc'].append(-1)
                infoSet['aboveL0MvX'].append(-1)
                infoSet['aboveL0MvY'].append(-1)
                
        if flag == 'A1':
            if 'aboveL1Poc' not in infoSet.keys():
                infoSet['aboveL1Poc'] = []
            if 'aboveL1MvX' not in infoSet.keys():
                infoSet['aboveL1MvX'] = []
            if 'aboveL1MvY' not in infoSet.keys():
                infoSet['aboveL1MvY'] = []
            content = lineList[1]
            content = content.replace(" ", "")
            if content != 'none':
                infoSet['aboveL1Poc'].append(int(lineList[1]))
                infoSet['aboveL1MvX'].append(int(lineList[2]))
                infoSet['aboveL1MvY'].append(int(lineList[3]))
            else:
                infoSet['aboveL1Poc'].append(-1)
                infoSet['aboveL1MvX'].append(-1)
                infoSet['aboveL1MvY'].append(-1)


        if flag == '&':
            mergeInfoFlag = 1
            if 'merFlag' not in infoSet.keys():
                infoSet['merFlag']=[]
            if lineList[1] == 'Merge':
                infoSet['merFlag'].append(1)
            else:
                infoSet['merFlag'].append(0)
    #print infoSet['merFlag']
    #print infoSet['biType']
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
        df_sel = df[df.cusize == item]
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

    exit(0)

