## Decomposition Resutls of Carbon Emission Intensity 

import pandas as pd
import numpy as np

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
        
        for i in range(6):
           if x[i] >= 0:
                x[i] = 0
           else:
                x[i] = (-10)*x[i]   # replace negative values in x(list)
                
        temp_e1[temp_e1>0] = 0
        temp_e1[temp_e1<0] = (-10)*temp_e1   
        
        temp_e2[temp_e2>0] = 0
        temp_e2[temp_e2<0] = (-10)*temp_e2  # replace negative values in temp_e1/2(both arrays)
        
        z = sum(x[:4]+x[5:])+temp_e1+temp_e2    # sum specific values in a list by constructing a new one
        
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

year=[]
for li in range(2001,2017):
    year.extend([li]*10)
    
year_str= list(map(str,year))

df.insert(0,"year",year_str)    # Chang the type of 'year' into string

max6cerm = df.loc['Sum'].drop('China',axis=1).max(axis=1).iloc[[0,5,7,9,11,15]] #  maximum values of decomposition results in years 2001, 2006, 2008, 2010, 2012 and 2016.

prov_av = (df.loc['Sum'].drop('year',axis=1).sum(axis=0))/16

df.loc[-1] = prov_av
df.rename(index={-1:'prov_av'},inplace=True)    # average values of provincial CERI in 16 years




### Average CERI for 7 regions

ceri_7r =[]

ceri_7r.append(df.loc['prov_av'][2:7].sum()/5)
ceri_7r.append(df.loc['prov_av'][7:10].sum()/3)
ceri_7r.append(df.loc['prov_av'][10:17].sum()/7)
ceri_7r.append(df.loc['prov_av'][17:20].sum()/3)
ceri_7r.append(df.loc['prov_av'][20:23].sum()/3)
ceri_7r.append(df.loc['prov_av'][23:27].sum()/4)
ceri_7r.append(df.loc['prov_av'][27:32].sum()/5)

ceri_7r= pd.DataFrame(ceri_7r,index=['NC', 'NER', 'EC','CC','SC','SWC','NWC'])

#%%

df.to_excel('LMDI_ceri_Kai_0804.xlsx')
#%%
## Calculating Carbon Emission Reductions

import pandas as pd
import numpy as np

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


### Calculating the difference of provincial and national resutls by year

sumcol = df_cer.loc['Sum'].drop('China', axis=1).sum(axis=1) 
sumchina = df_cer['China']['Sum']

sumcc=pd.concat([sumcol, sumchina],axis=1,keys=['province','China'])

year=[]
for li in range(2001,2017):
    year.append(li)
    year_str= list(map(str,year))

sumcc.insert(0,"year",year_str)    # Chang the type of 'year' into string

sumcc['diff'] = sumcc.iloc[:,1]-sumcc.iloc[:,2] # Difference of CER from the year 2001 t0 2016 between province and nation

### Calculating CER/CE

df = pd.read_excel('Data.xlsx','Main')

name = []
for i in range(30):
     name.append(df.iloc[9+i*11,2])
     
cer_ce = []  
csum = [] 
cer = [] 
for i in range(30):
    df = pd.read_excel('MainData.xlsx',name[i])
    cer_ce.append( df_cer.loc['sum_by_prov'][i+2]/(df['C'].values.sum()) )
    cer.append(df_cer.loc['sum_by_prov'][i+2])
    csum.append((df['C'].values.sum()) ) # a list of CE

cer_ce1 = pd.DataFrame({'province': name, 'CER': cer, 'CE': csum,'CER/CE': cer_ce})     # CER, CE and CER/CE for 30 provinces 

#### Calculating average values of CER, CE and CER/CE

num = 0
for i in range(1,4):
    av1_nc = cer_ce1.iloc[0:5,i].sum()/5
    av1_nec = cer_ce1.iloc[5:8,i].sum()/3
    av1_ec = cer_ce1.iloc[8:15,i].sum()/7
    av1_cc = cer_ce1.iloc[15:18,i].sum()/3
    av1_sc = cer_ce1.iloc[18:21,i].sum()/3
    av1_swc = cer_ce1.iloc[21:25,i].sum()/4
    av1_nwc = cer_ce1.iloc[25:30,i].sum()/5

    cer_av=np.array([av1_nc,av1_nec,av1_ec,av1_cc,av1_sc,av1_swc,av1_nwc]).reshape([-1,1])
    if num == 0:
           num = 1
           cer_aver= cer_av
    else:
            cer_aver = np.hstack([cer_aver,cer_av])
cer_aver = pd.DataFrame(cer_aver, index = ['NC','NEC','EC','CC','SC','SWC','NWC'], columns = ['CER_av','CE_av','CER/CE_av']) # CER, CE and CER/CE for 7 regions


### Calculating CER of 7 regions

sum_nc = []
sum_nec = []
sum_ec = []
sum_cc = []
sum_sc = []
sum_swc = []
sum_nwc = []
for jj in range(0,16):
    sum_nc.append(df_cer.loc['Sum'].iloc[jj,2:7].sum())
    sum_nec.append(df_cer.loc['Sum'].iloc[jj,7:10].sum())
    sum_ec.append(df_cer.loc['Sum'].iloc[jj,10:17].sum())
    sum_cc.append(df_cer.loc['Sum'].iloc[jj,17:20].sum())
    sum_sc.append(df_cer.loc['Sum'].iloc[jj,20:23].sum())
    sum_swc.append(df_cer.loc['Sum'].iloc[jj,23:27].sum())
    sum_nwc.append(df_cer.loc['Sum'].iloc[jj,27:32].sum())
    
cer_7r= pd.DataFrame({'NC': sum_nc, 'NER': sum_nec, 'EC': sum_ec,'CC': sum_cc,'SC': sum_sc,'SWC': sum_swc,'NWC': sum_nwc})


#%%'
sumcc.to_excel('LMDI_cer_diff_Kai_0804.xlsx')

#%%
df_cer.to_excel('LMDI_cer_Kai_0804.xlsx')   

#%%
## Calculating Carbon Emission Reductions Per Person

import pandas as pd
import numpy as np

df = pd.read_excel('Data.xlsx','Main')

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
