from math import log
import numpy as np


# genera variable exponecial con parametro lambda
def VarExponecial(Lambda):
    U = np.random.random()
    return (-1/Lambda)*log(U)

# genera variable uniforme con parametros a,b


def VarUniform(a, b):
    U = np.random.random()
    return a + (b-a)*U

# genera el tipo de comida


def getTypefoot():
    return np.random.randint(1, 3)


def testExp(n, L):
    l = []
    for _ in range(n):
        l.append(VarExponecial(L))
    return l


def testUniform(n, a, b):
    l = []
    for _ in range(n):
        l.append(VarUniform(a, b))
    return l
