# =============================================================================
# 
# =============================================================================
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


def L(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))

#%%  根据图7得到 原始的 Δe 
e1 = 0.3432
e2 = 0.0371


#%%  这部分用于求解 ln Et-E0    # 要注意表格中 gsi 三个概念发生了变化的。 这里不影响e
df = pd.read_excel('MainData.xlsx','China')
e_all = df['e'].values
c_all = df['Cc'].values
## 1: 延用论文中的结果
Delta_C_1 = 0.0372  # 论文中的结果


L_ctc0_1  = L(c_all[8],c_all[0])
ln_ete0_1 = e1 / L_ctc0_1


ln_EtE0_1 = np.log(e_all[8]/e_all[0])


ln_e_Adj = ln_ete0_1 - ln_EtE0_1


s1 = ln_EtE0_1 * L_ctc0_1
s2 = ln_e_Adj * L_ctc0_1

print(s1+s2)
#%%3
Delta_C_2 = 0.0031  # 论文中的结果


L_ctc0_2  = L(c_all[16],c_all[8])
ln_ete0_2 = e2 / L_ctc0_2


ln_EtE0_2 = np.log(e_all[16]/e_all[8])


ln_e_Adj2 = ln_ete0_2 - ln_EtE0_2


s3 = ln_EtE0_2 * L_ctc0_2
s4 = ln_e_Adj2 * L_ctc0_2


print(s3+s4)