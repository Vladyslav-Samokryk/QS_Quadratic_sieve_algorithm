
if __name__ == "__main__":
    from Factor import Factor
    from time import time
    import numpy as np
    from data import n, B
    from valcolor import valcolor

    print("B "+valcolor(B,"data"))
    t = time()

    res = Factor(n,B)

    print("\nans:",valcolor(int(res[0]),"strong")+" "+valcolor(int(res[1]),"strong"))
    print("time:",valcolor(round(time() - t,4),"time"))
