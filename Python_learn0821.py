# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 10:09:31 2021

@author: lik6
"""
def kai(x):
    kai = x*x
    return kai
print(kai(4))

kai = lambda x:x*x
print(kai(4))

#%% filter()
#The filter() function extracts elements from an iterable (list, tuple etc.) for which a function returns True.
#iterable - an iterable like sets, lists, tuples etc.
x= [1,2,3,4,5]
y= filter(lambda x: (x%2 == 0), x)
y= filter(lambda x: x>2, x)
y= filter( lambda x: x*x, x) # doesn't work as it only returns Ture in the specified function. More suitable for loops. 
list(y)
#%%  Map takes all objects in a list and allows you to apply a function to it 
x = [1,2,3,4,5]
y = map(lambda x: x*x, x)
list(y)
# diff of map() and filter()， see https://medium.com/@ankur.ghogle100/difference-between-map-and-filter-in-python-8c5bca11afe8
#%% Numpy
import numpy as np
# create one and two dimensional arrays
np1= np.array([1,2,3])
np2= np.array([[1,2,3], [4,5,6]])
# create arrays with only 1 or 0 elements
np3 = np.ones((2,3))
np4 = np.zeros((2,3))
# index and transform
np5 = np.arange(6).reshape(3,2)
# index one or multiple columns
np5[:,1]
np5[:,[0,1]]
# index one or multiple rows
np5[1,:]
np5[[0,1],:]
# for one element
np5[1,1]
# the change of dimensions
np6 = np5.reshape(2,3)
# transpostion
np7 = np5.T

#  Return a copy of the array collapsed into one dimension.
#‘C’ means to flatten in row-major (C-style) order. 
#‘F’ means to flatten in column-major (Fortran- style) order. 
np8 = np5.flatten()
np9 = np5.flatten('F')