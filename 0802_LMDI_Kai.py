# LMDI Decompostion Method
import os
import pandas as pd
import numpy as np

#%%
os.getcwd()
os.chdir("D:\\WeChat Files\\wxid_acqiywegk1ox22\\FileStorage\\File\\2021-07\\20210728_Codes")
df = pd.read_excel('Data.xlsx','Main')

#%%
## Calculating Carbon Emission Reductions

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
    
year_str= list(map(str,year))
year_str.append("NaN")
df.insert(1,"year",year_str)    # Chang the type of 'year' into string

max6cer = df.loc['Sum'].drop('China', axis=1).iloc[[0,5,7,9,11,15]].max(axis=1)    # maximum values of co2 reductions in years 2001, 2006, 2008, 2010, 2012 and 2016.

#%%
df.to_excel('LMDI_CER_peryear.xlsx')
#%%
## Decompostion Resutls of Carbon Emission Intensity

def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0):
        def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
        if L(yt,y0)*np.log(xt/x0) >= 0:
             return 0
        else:
             return L(yt,y0)*np.log(xt/x0)
        
    Delta_y = data[tt,0]-data[t0,0]
    Delta_x = []
    for i in range(1,np.shape(data)[1]):
        
        Delta_x.append(Delta_XX(data[tt,0],data[t0,0],data[tt,i],data[t0,i] ) )
        
    return Delta_y,Delta_x

name = ['China']
for i in range(30):
     name.append(df.iloc[9+i*11,2])

num1 = 0
for jj in range(1,17):
    num = 0
    for i in range(31):
        df = pd.read_excel('MainData.xlsx',name[i])
        df1 = df[['Cc','p','g','s','i','e','Kc']].values
        
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
        
df = pd.DataFrame(res_all,index=(['p','i','g','s','e','Kc','Sum','\u0394'+'Cc']*16) ,columns =name )


df.loc[-1] = df.loc['Sum'].sum(axis=0)
df.rename(index={-1:'Total_sum'},inplace=True)

kai = (-10)*(df.loc['Sum'].drop('China',axis=1).min(axis=1)) # Changing into kgC02/m2
max6cerm = kai.iloc[[0,5,7,9,11,15]]
#%%
df.to_excel('LMDI_CERI_Kai_0803.xlsx')

#%%
## Calculating Carbon Emission Reductions Per Person

def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0,Fc,P):
        def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
        if L(yt,y0)*np.log(xt/x0) >= 0:
             return 0
        else:
             return (L(yt,y0)*np.log(xt/x0)*Fc*(-1))/P*(pow(10,3))
        
    Delta_y = data[tt,0]-data[t0,0]
    Delta_x = []
    for i in range(3,np.shape(data)[1]):
        
        Delta_x.append(Delta_XX(data[tt,0],data[t0,0],data[tt,i],data[t0,i],data[tt,1],data[tt,2]))
        
    return Delta_y,Delta_x


name = ['China']
for i in range(30):
     name.append(df.iloc[9+i*11,2])

num1 = 0
for jj in range(1,17):
    num = 0
    for i in range(31):
        df = pd.read_excel('MainData.xlsx',name[i])
        df1 = df[['Cc','Fc','P','p','g','s','i','e','Kc']].values
        
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


sum_max = df.loc['Sum'].max(axis=0)
df.loc[-1] = sum_max
df.rename(index={-1:'sum_max'},inplace=True)


max6pp = df.loc['Sum'].iloc[[0,5,7,9,11,15]].max(axis=1) # maximum values of co2 reductions per persion in years 2001, 2006, 2008, 2010, 2012 and 2016.

