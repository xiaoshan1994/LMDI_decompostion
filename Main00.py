import numpy as np
import pandas as pd 

from sklearn.preprocessing import StandardScaler


import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号



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

df = pd.read_excel('MainData.xlsx','BJ')
# df.columns = ['Ec','C','Fc','P','G','Gs','Kc']

# df['Cc'] = df['C']/df['Fc']
# df['p'] = df['P']/df['Fc']
# df['g'] = df['Fc'] / df['Gs']
# df['s'] = df['G'] / df['P']
# df['i'] = df['Gs']/df['G']
# df['e'] = df['Ec']/df['Fc']

new_df = df[['Cc','p','g','s','i','e','Kc']].values


df['Y']  = np.log(df['Cc'])
df['X1'] = np.log(df['p'])
df['X2'] = np.log(df['g'])
df['X3'] = np.log(df['s'])
df['X4'] = np.log(df['i'])
df['X5'] = np.log(df['e'])
df['X6'] = np.log(df['Kc'])

ans = df['Y']-(df['X1'] + df['X2'] + df['X3'] + df['X4'] + df['X5'] + df['X6'])



y1,x1 = LMDI(new_df,1,0)
print(x1)
y2,x2 = LMDI(new_df,2,1)
print(x2)
y3,x3 = LMDI(new_df,3,2)
print(x3)
y4,x4 = LMDI(new_df,4,3)
print(x4)
y4,x5 = LMDI(new_df,4,3)
print(x5)
y4,x6 = LMDI(new_df,4,3)
print(x6)
y4,x7 = LMDI(new_df,4,3)
print(x7)
y4,x8 = LMDI(new_df,4,3)
print(x8)


anss = np.array(x1)+np.array(x2)+np.array(x3)+np.array(x4)
ansss = anss+np.array(x5)+np.array(x6)+np.array(x7)+np.array(x8)
print(ansss)
y,x = LMDI(new_df,8,0)
print(x)







