# %%
# 使用套件解
from scipy import optimize
import scipy
import numpy as np

# paper的問題:
# Max Z =60X1 + 45X2 + 45X3 + 42X4 +42X5
# s.t (1) 𝑋1 +𝑋2 +𝑋3 +𝑋4 +𝑋5 ≤61,250,000
# (2) 𝑋2 + 𝑋3 ≤ 12,250,000
# (3) 𝑋1 ≤ 18,375,000
# (4) 𝑋2 ≤ 18,375,000
# (5) 𝑋3 ≤ 18,375,000
# (6) 𝑋4 ≤ 18,375,000
# (7) 𝑋5 ≤ 18,375,000
# (8)71𝑋1 + 35𝑋2 + 41𝑋3 + 57𝑋4 + 54𝑋5 ≥ 5,500,000
# (9) 69𝑋1 + 20𝑋2 + 36𝑋3 + 42𝑋4 + 41𝑋5 ≥ 4,800,000
# (10) 56𝑋1 + 12𝑋2 + 12𝑋3 + 42𝑋4 + 39𝑋5 ≥ 4,500,000

c = np.array([-60, -45, -45, -42, -42])
A_ub = np.array([[1,1,1,1,1],
                [0,1,1,0,0],
                [-71,-35,-41,-57,-54],
                [-69,-20,-36,-42,-41],
                [-56,-12,-12,-42,-39]])

B_ub = np.array([[61250000],[12250000],[-5500000],[-4800000],[-4500000]])

res = scipy.optimize.linprog(c, A_ub, B_ub,
                             bounds = [(0,18375000),(0,18375000),(0,18375000),(0,18375000),(0,18375000)],
                             method= "revised simplex")

print(res)

# %%
# 不用套件解
# 練習手刻simplex method
import numpy as np
import pandas as pd

np.seterr(divide='ignore',invalid='ignore')

Ab = np.array([[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,61250000],
               [0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,12250000],
               [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,18375000],
               [0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,18375000],
               [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,18375000],
               [0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,18375000],
               [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,18375000],
               [71,35,41,57,54,0,0,0,0,0,0,0,-1,1,0,0,0,0,5500000],
               [69,20,36,42,41,0,0,0,0,0,0,0,0,0,-1,1,0,0,4800000],
               [56,12,12,42,39,0,0,0,0,0,0,0,0,0,0,0,-1,0,4500000],
               [-60,-45,-45,-42,-42,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype="float32")

n1,m1 = np.shape(Ab)
n = n1-1
m = m1-1

k = 0
while np.any(Ab[n,:-1]<0):
    j = np.argmin(Ab[n,:-1])
    #pivotrow
    minval = np.inf
    for i in range(n):
        val = Ab[i,m]/Ab[i,j]
        if (val>0) & (val<minval):
            minval = val
            pivotrow = i
    #print(pivotrow)

    #高斯消去法
    Ab[pivotrow,:] = Ab[pivotrow,:]/Ab[pivotrow,j]
    #print(Ab)
    for i in range(n+1):
        if (i != pivotrow) :
            multipy = Ab[i,j]/Ab[pivotrow,j]
            Ab[i,:] = Ab[i,:] - (Ab[pivotrow,:] * multipy)
    Ab = np.around(Ab,4)
    k = k+1

    #Ab = pd.DataFrame(Ab)
    #print("第" + str(k) + "次：", Ab)
    #Ab = Ab.values

Ab = pd.DataFrame(Ab)
print(Ab)