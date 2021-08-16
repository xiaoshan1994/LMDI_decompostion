
import os
import pandas as pd
import numpy as np

def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0,Fc):
        def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
        if L(yt,y0)*np.log(xt/x0) >= 0:
             return 0
        else:
             return L(yt,y0)*np.log(xt/x0)*Fc*(-1)
        
    Delta_y = data[tt,0]-data[t0,0]
    Delta_x = []
    for i in range(2,np.shape(data)[1]):
        
        Delta_x.append(Delta_XX(data[tt,0],data[t0,0],data[tt,i],data[t0,i],data[tt,1] ) )
        
    return Delta_y,Delta_x

# =============================================================================
#  本篇代码主要用于计算LMDI 分解结果
# 依次读取31张表的数据，  再分解
# =============================================================================
# 现在为了做国家、省级的 逐年的七个分解结果，首先根据以前的方法将之前的
# =============================================================================
# =============================================================================

os.getcwd()
os.chdir("D:\\WeChat Files\\wxid_acqiywegk1ox22\\FileStorage\\File\\2021-07\\20210728_Codes")
df = pd.read_excel('Data.xlsx','Main')

name = ['China']
for i in range(30):
     name.append(df.iloc[9+i*11,2])

num1 = 0
for jj in range(1,17):
    num = 0
    for i in range(31):
        df = pd.read_excel('MainData.xlsx',name[i])
        df1 = df[['Cc','Fc','p','g','s','i','e','Kc']].values
        
        y,x = LMDI(df1,jj,jj-1)
        z = sum(x)
        re = np.append(x,z).reshape([-1,1])
        re = np.append(re,y).reshape([-1,1])
        if num == 0:
           num = 1
           res = re
        else:
            res = np.hstack([res,re])
    if num1 == 0:
        num1 = 1
        res_all = res
    else:
        res_all = np.vstack([res_all,res])
        
df = pd.DataFrame(res_all,index=(['p','i','g','s','e','Kc','Sum','Cc']*16) ,columns =name )
# df = pd.DataFrame(res,index=['p','g','s','i','e','Kc','Cc'])


df.loc[-1] = df.loc['Sum'].sum(axis=0)
df.rename(index={-1:'Total_sum'},inplace=True)

year=[]
for li in range(2001,2017):
    year.extend([li]*8)
year.append("NaN")


df.insert(1,"year",year)
    
df.to_excel('LMDI_CER_peryear.xlsx')







