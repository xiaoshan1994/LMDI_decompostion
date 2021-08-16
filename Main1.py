import pandas as pd
import numpy as np

def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0):
        def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
        return L(yt,y0)*np.log(xt/x0)
    Delta_y = data[tt,0]-data[t0,0]
    Delta_x = []
    for i in range(1,np.shape(data)[1]):
        Delta_x.append( Delta_XX(data[tt,0],data[t0,0],data[tt,i], data[t0,i]) )
    return Delta_y,Delta_x

# =============================================================================
#  本篇代码主要用于计算LMDI 分解结果
# 依次读取31张表的数据，  再分解
# =============================================================================

df = pd.read_excel('Data.xlsx','Main')
name = ['China']
[name.append(df.iloc[9+i*11,2])  for i in range(30)]

num = 0
for i in range(31):
    df = pd.read_excel('MainData.xlsx',name[i])
    df1 = df[['Cc','p','g','s','i','e','Kc']].values
    
    y,x = LMDI(df1,16,0)
    
    x1 = x/df1[0,0]
    y1 = y/df1[0,0]
    
    
    re = np.append(x1,y1).reshape([-1,1])
    if num == 0:
        num = 1
        res = re
    else:
        res = np.hstack([res,re])

df = pd.DataFrame(res,index=['p','g','s','i','e','Kc','Cc'] ,columns =name )
# df = pd.DataFrame(res,index=['p','g','s','i','e','Kc','Cc'])
df.to_excel('LMDI_Results_1.xlsx')







