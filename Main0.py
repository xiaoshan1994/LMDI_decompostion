

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
# 
# =============================================================================

df = pd.read_excel('data.xlsx','Main')
name = ['China']
[name.append(df.iloc[9+i*11,2])  for i in range(30)]


from openpyxl import load_workbook
writer = pd.ExcelWriter('MainData.xlsx',engine = 'openpyxl')
book = load_workbook('MainData.xlsx')
writer.book = book


# =============================  This is China ================================================
df_China = df.iloc[0:7,2:].T
df_China.columns = ['Ec','C','Fc','P','G','Gs','Kc']

df_China['Cc'] = df_China['C']   / df_China['Fc']
df_China['p'] = df_China['P']    / df_China['Fc']
df_China['g'] = df_China['Fc']   / df_China['Gs']
df_China['s'] = df_China['G']    / df_China['P']
df_China['i'] = df_China['Gs']   / df_China['G']
df_China['e'] = df_China['Ec']   / df_China['Fc']

df_China['k'] = df_China['Kc']          # 直接让他等于 Kc
# 先在这里保存全国的结果   将sheet名设为 China
df_China.to_excel(writer,name[0])


# =============================  This is Province ================================================

for i in range(30):
    df1 = df.iloc[11+i*11:18+i*11,2:].T
    df1.columns = ['Ec','C','Fc','P','G','Gs','Kc']
    df1['Cc'] = df1['C']   / df1['Fc']
    df1['p'] = df1['P']    / df1['Fc']
    df1['g'] = df1['Fc']   / df1['Gs']
    df1['s'] = df1['G']    / df1['P']
    df1['i'] = df1['Gs']   / df1['G']
    df1['e'] = df1['Ec']   / df1['Fc']
    
    df1['k'] = df1['Kc']
    df1.to_excel(writer,name[i+1])
    writer.save()
    
        
    
    
    
    
    