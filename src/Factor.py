from time import time


def Factor(n, B):
    # color text!!!
    from valcolor import valcolor

    # some functions to support functionality (LOL)
    from lib import GCD,Q
    q = Q(n)

    # class generating Factor base
    from Prime import Prime
    primes = Prime(n,B,q)

    # func to suive until we have critical len of smooth numbers
    from Suive import suive

    t = time()
    smooth_numbers = suive(q,primes)
    print("time:",valcolor(round(time() - t,4),"time"))

    print("Total number of smooth numberes:",valcolor(len(smooth_numbers),'data'))
    print(valcolor("All smooth numbers found",'strong')+'\n')

    # matrix solves
    print('Start making matrix\n')
    t = time()

    from Matr_solv import Matr_solv

    matrix = Matr_solv(primes.p)

    # form matrix with given smooth
    for smooth in smooth_numbers:
        matrix.add(smooth[2])
    print("Matrix builded in:",valcolor(round(time() - t,4),"time"))

    # possibe outcome [None,None] or if we LUCKY give ans as [gcd,n//gcd]
    solve = matrix.solve(smooth_numbers)

    return solve
