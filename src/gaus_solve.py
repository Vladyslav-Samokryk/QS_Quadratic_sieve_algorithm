import ctypes
import os
import pathlib
import numpy as np
from cfiles.numpyctypes import c_ndarray

# Load the shared library into ctypes
#libname = pathlib.Path().absolute() / "gaus_solve.so"
libname = str(os.path.join(pathlib.Path().absolute(), "gaus_solve.dll"))
#libname="C:\\Users\\User\\Desktop\\6sem-70efdf75d0bc48916c80737743499fa338f6ae6a\\6sem-70efdf75d0bc48916c80737743499fa338f6ae6a\\Cryptography\\1lab\\src\\gaus_solve.so"
c_lib = ctypes.CDLL(libname)

def gaus_solve(input_matrix):
    ret = np.empty(input_matrix.shape, dtype='uint8')
    par1 = c_ndarray(input_matrix, dtype = 'uint8', ndim = 2)
    par2 = c_ndarray(ret, dtype = 'uint8', ndim = 2)
    N = c_lib.test(par1, par2)
    return ret[:,:N]
