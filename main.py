
from generation_var import *
from sys import maxsize as MAX
from collections import deque


def simulate(thre=False):
    t = Na = 0
    T = 660
    # tiempos de salida del servidor i
    tD1 = MAX
    tD2 = MAX
    tD3 = MAX

    # cantidad de partidas desde el servidor i
    nD1 = 0
    nD2 = 0
    nD3 = 0

    # Diccionario para los tiempos de salida del servidor i
    D1 = {}
    D2 = {}
    D3 = {}
    #Diccionario para los tiempos de atendidos por el servidor i
    T1 = {}
    T2 = {}
    T3 = {}


    A = {}  # diccionario de tiempo de llegadas

    tA = VarExponecial(1/10)
    cookers = [0]*3
    q = deque()
    while t <= T:
        times = [tA, tD1, tD2, tD3]
        if min(times) == tA:
            if tA > T:
                tA = MAX
                break
            t = tA
            Na += 1
            if (t > 90 and t < 210) or (t > 420 and t < 540):
                tAt = VarExponecial(2/5)
            else:
                tAt = VarExponecial(1/10)

            tA = t + tAt
            A[Na] = t
            f = getTypefoot()
            if f == 1:
                te = VarUniform(3, 5)
            else:
                te = VarUniform(5, 8)

            if cookers[0] == 0:
                cookers[0] = Na
                T1[Na] = t
                tD1 = t+te
            elif cookers[1] == 0:
                cookers[1] = Na
                T2[Na] = t
                tD2 = t + te
            # orario pico
            elif thre and ((t > 90 and t < 210) or (t > 420 and t < 540)):
                q.append(Na)

                if cookers[2] == 0:
                    c = q.pop()
                    cookers[2] = c
                    T3[c] = t
                    tD3 = t + te

            else:
                q.append(Na)

        elif min(times) == tD1:
            t = tD1
            if thre and ((t > 90 and t < 210) or (t > 420 and t < 540)) and cookers[2] == 0 and len(q) > 0:

                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                c = q.pop()
                cookers[2] = c
                T3[c] = t
                tD3 = t+te

            nD1 += 1
            D1[cookers[0]] = t
            if len(q) == 0:
                cookers[0] = 0
                tD1 = MAX
            else:

                c = q.pop()
                cookers[0] = c
                T1[c] = t
                f = getTypefoot()
                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                tD1 = t+te

        elif min(times) == tD2:
            t = tD2
            if thre and ((t > 90 and t < 210) or (t > 420 and t < 540)) and cookers[2] == 0 and len(q) > 0:

                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                c = q.pop()
                cookers[2] = c
                T3[c] = t
                tD3 = t+te
            nD2 += 1
            D2[cookers[1]] = t
            if len(q) == 0:
                cookers[1] = 0
                tD2 = MAX
            else:

                c = q.pop()
                cookers[1] = c
                T2[c] = t
                f = getTypefoot()
                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                tD2 = t+te
        elif min(times) == tD3:
            t = tD3
            nD3 += 1
            D3[cookers[2]] = t
            if (t > 90 and t < 210) or (t > 420 and t < 540):
                if len(q) == 0:
                    cookers[2] = 0
                    tD3 = MAX
                else:

                    c = q.pop()
                    cookers[2] = c
                    T3[c] = t
                    f = getTypefoot()
                    if f == 1:
                        te = VarUniform(3, 5)
                    else:
                        te = VarUniform(5, 8)
                    tD3 = t+te
            else:
                cookers[2] = 0
                tD3 = MAX

    while tA != MAX or tD1 != MAX or tD3 != MAX:

        times = [tA, tD1, tD2]
        if min(times) == tA:
            tA = MAX
        elif min(times) == tD1:
            t = tD1
            nD1 += 1
            D1[cookers[0]] = t
            if len(q) == 0:
                cookers[0] = 0
                tD1 = MAX
            else:

                c = q.pop()
                cookers[0] = c
                T1[c] = t
                f = getTypefoot()
                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                tD1 = t+te
        elif min(times) == tD2:
            t = tD2
            nD2 += 1
            D2[cookers[1]] = t
            if len(q) == 0:
                cookers[1] = 0
                tD2 = MAX
            else:

                c = q.pop()
                cookers[1] = c
                T2[c] = t
                f = getTypefoot()
                if f == 1:
                    te = VarUniform(3, 5)
                else:
                    te = VarUniform(5, 8)
                tD2 = t+te

    return nD1, nD2, nD3, D1, D2, D3, A, T1, T2, T3, Na


def porcent(A, T1, T2, T3):

    TimeE = {}
    for t in T1:
        TimeE[t] = T1[t]-A[t]

    for t in T2:
        TimeE[t] = T2[t]-A[t]

    for t in T3:
        TimeE[t] = T3[t]-A[t]

    c = 0
    for t in TimeE:
        if TimeE[t] > 5:
            c += 1

    return c*100/len(A)


def main():
    mp = 0
    _mp = 0
    n = 50
    n1 = 0
    n2 = 0
    n3 = 0
    _n1 = 0
    _n2 = 0
    _n3 = 0
    na = 0
    _na = 0
    for _ in range(n):
        nD1, nD2, nD3, D1, D2, D3, A, T1, T2, T3, Na = simulate(True)
        p = porcent(A, T1, T2, T3)
        mp += p
        n1 += nD1
        n2 += nD2
        n3 += nD3
        na += Na

        _nD1, _nD2, _nD3, _D1, _D2, _D3, _A, _T1, _T2, _T3, _Na = simulate()
        _p = porcent(_A, _T1, _T2, _T3)
        _mp += _p
        _n1 += _nD1
        _n2 += _nD2
        _na += _Na

    print('resultados finales')

    print(
        f'la media de el pociento de tiempo de espera mayor que 5 minutos para 2 trabajadores y un tercero en los horarios picos es {mp/n}')

    print(
        f'la media de el pociento de tiempo de espera mayor que 5 minutos para 2 trabajadores es {_mp/n}')

    print(
        f'la media de clientes atendidos por el trabajador uno ,con dos trabajadores es de {_n1/n}')

    print(
        f'la media de clientes atendidos por el trabajador dos ,con dos trabajadores es de {_n2/n}')

    print(
        f'la media de clientes atendidos por el trabajador uno ,con dos trabajadores y un tercero en los horarios picos es de {n1/n}')

    print(
        f'la media de clientes atendidos por el trabajador dos ,con dos trabajadores y un tercero en los horarios picos es de {n2/n}')

    print(
        f'la media de clientes atendidos por el trabajador tres ,con dos trabajadores y un tercero en los horarios picos es de {n3/n}')

    print(
        f'la media de clientes atendidos por dias con dos trabajadores es  {_na/n}')

    print(
        f'la media de clientes atendidos por dias con dos trabajadores y un tercero en los horarios picos es  {na/n}')


main()
