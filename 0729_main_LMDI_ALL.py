
import pandas as pd
import numpy as np

data = pd.read_excel('LMDI_Results_all_everyyear.xlsx').values

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
    for j in range(4,110,7):
        num_year += 1
        
        temp_Delta_e = data[j,i+1]
        
        temp_df = pd.read_excel('MainData.xlsx',name[i])
        c =  temp_df['Cc'].values
        e = temp_df['e'].values
        temp_L = L(c[num_year],c[num_year-1])
        temp_e1 = temp_L *  np.log(e[num_year]/e[num_year-1])
        
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
df_all.to_excel('new_e_all_everyyear.xlsx')
