## Decompostion Resutls of Carbon Emission Intensity

import pandas as pd
import numpy as np
import os

os.getcwd()
os.chdir("D:\\WeChat Files\\wxid_acqiywegk1ox22\\FileStorage\\File\\2021-07\\20210728_Codes")
df = pd.read_excel('Data.xlsx','Main')

def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
            
def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0):
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
        c = df['Cc'].values
        e = df[['e']].values
        P = df[['P']].values
        
        temp_L = L(c[jj],c[jj-1])
        temp_e1 = temp_L*np.log((e[jj]/P[jj])/(e[jj-1]/P[jj-1]))
        temp_e2 = x[4] - temp_e1
    
        z = sum(x)+temp_e1+temp_e2-x[4]
        re = np.append(x, temp_e1).reshape([-1,1])
        re = np.append(re,temp_e2).reshape([-1,1])
        re = np.append(re,z).reshape([-1,1])
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
        
df = pd.DataFrame(res_all,index=(['p','i','g','s','e','Kc','e1','e2','Sum','\u0394'+'Cc']*16) ,columns =name )


kai = (-10)*(df.loc['Sum'].drop('China',axis=1).min(axis=1)) # Changing into kgC02/m2
max6cerm = kai.iloc[[0,5,7,9,11,15]]

year=[]
for li in range(2001,2017):
    year.extend([li]*10)
    
year_str= list(map(str,year))

df.insert(0,"year",year_str)    # Chang the type of 'year' into string

#%%
df.to_excel('LMDI_ceri_Kai_0804.xlsx')
#%%

## Calculating Carbon Emission Reductions

import pandas as pd
import numpy as np
import os

os.getcwd()
os.chdir("D:\\WeChat Files\\wxid_acqiywegk1ox22\\FileStorage\\File\\2021-07\\20210728_Codes")
df = pd.read_excel('Data.xlsx','Main')


def L(yt,y0):
            if yt == y0:
                return 0
            else:
                return (yt-y0)/(np.log(yt) - np.log(y0))
            
def LMDI(data,tt,t0):
    def Delta_XX(yt,y0,xt,x0,Fc):
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
        
        c = df['Cc'].values
        e = df[['e']].values
        P = df[['P']].values
        eFc = df['Fc'].values
        
        temp_L = L(c[jj],c[jj-1])
        temp_e1 = temp_L*np.log((e[jj]/P[jj])/(e[jj-1]/P[jj-1]))
        temp_e2 = x[4] - temp_e1
        
        if temp_e1 >= 0:
             temp_e1 = 0
        else:
            temp_e1 = temp_e1*eFc[jj]*(-1)
            
        if temp_e2 >= 0:
             temp_e2 = 0
        else:
            temp_e2 = temp_e2*eFc[jj]*(-1)
         
        z = sum(x)+temp_e1+temp_e2-x[4]
        
        re = np.append(x, temp_e1).reshape([-1,1])
        re = np.append(re,temp_e2).reshape([-1,1])
        re = np.append(re,z).reshape([-1,1])
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
        
df_cer = pd.DataFrame(res_all,index=(['p','i','g','s','e','Kc','e1','e2','Sum','\u0394'+'Cc']*16) ,columns =name )

year=[]
for li in range(2001,2017):
    year.extend([li]*10)
    
year_str= list(map(str,year))

df_cer.insert(1,"year",year_str)    # Chang the type of 'year' into string



max6cer = df_cer.loc['Sum'].drop('China', axis=1).iloc[[0,5,7,9,11,15]].max(axis=1)    # maximum values of co2 reductions in years 2001, 2006, 2008, 2010, 2012 and 2016.

sum_by_prov= df_cer.loc['Sum'].drop('year',axis=1).sum(axis=0)
df_cer.loc[-1] = sum_by_prov
df_cer.rename(index={-1:'sum_by_prov'},inplace=True)

cer_total_prov = sum(sum_by_prov) - sum_by_prov['China']    # sum of provincial carbon reducitons during 2001-2016, unit: MtC02

#%%
df_cer.to_excel('LMDI_cer_Kai_0804.xlsx')


