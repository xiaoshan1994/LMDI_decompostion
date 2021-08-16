
import pandas as pd
import numpy as np
import os

os.getcwd()
os.chdir("D:\\WeChat Files\\wxid_acqiywegk1ox22\\FileStorage\\File\\2021-07\\20210728_Codes")
df = pd.read_excel('Data.xlsx','Main')

## Decompostion Resutls of Carbon Emission Intensity

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



kai = (-10)*(df.loc['Sum'].drop('China',axis=1).min(axis=1)) # Changing into kgC02/m2
max6cerm = kai.iloc[[0,5,7,9,11,15]]

year=[]
for li in range(2001,2017):
    year.extend([li]*8)
    
year_str= list(map(str,year))

df.insert(0,"year",year_str)    # Chang the type of 'year' into string

#%%
df.to_excel('LMDI_CERI_Kai_0803.xlsx')
#%%

## Decompostion Resutls of 'e'

data = pd.read_excel('LMDI_CERI_Kai_0803.xlsx').values

df1 = pd.read_excel('Data.xlsx','Main')
name = ['China']
[name.append(df1.iloc[9+i*11,2])  for i in range(30)]


def L(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))
    

num1 = 0
for i in range(data.shape[1]-1):
    num_year = 0
    
    num = 0
    for j in range(4,125,8):
        num_year += 1
        
        temp_Delta_e = data[j,i+1]
        
        temp_df = pd.read_excel('MainData.xlsx',name[i])
        c =  temp_df['Cc'].values
        e = temp_df['e'].values
        p = temp_df['P'].values
        
        temp_L = L(c[num_year],c[num_year-1])
        
        temp_e1 = temp_L * np.log((e[num_year]/p[num_year])/(e[num_year-1]/p[num_year-1]))
        
        temp_e2 = temp_Delta_e - temp_e1
        
        if num==0:
            num = 1
            temp_ee = np.array([temp_Delta_e,temp_e1,temp_e2]).reshape([-1,1])
        else:
            temp_ee = np.vstack([temp_ee,np.array([temp_Delta_e,temp_e1,temp_e2]).reshape([-1,1])])
    
    if num1 == 0:
        temp_ee_all = temp_ee
        num1 = 1
    else:
        temp_ee_all = np.hstack([temp_ee_all,temp_ee])


df_all = pd.DataFrame(temp_ee_all,index=(['raw_e','e1','e2']*16) ,columns =name )
# df = pd.DataFrame(res,index=['p','g','s','i','e','Kc','Cc'])

year=[]
for li in range(2001,2017):
    year.extend([li]*3)
    
year_str= list(map(str,year))

df_all.insert(0,"year",year_str)    # Chang the type of 'year' into string

df.set_index('year').join(df_all.set_index('year'))


#%%
df_all.to_excel('LMDI_e_Kai_0803.xlsx')
#%%
