from lib import eratos,Q,tonel,legendr
from time import time
import numpy as np
import pickle
from data import B_search, B_file, B_save
from valcolor import valcolor

class Prime:
    def __init__(self, n, B, q):
        if B_search:
            # B_search == True so we need to find out factor base
            prime = eratos(B)
            self.p = []
            self.r = []
            q = Q(n)
            t = time()

            if legendr(n%prime[0], prime[0]) == 1:
                tr = tonel(n,prime[0])
                r = [(tr - q.m) % prime[0]]
                self.p.append(prime[0])
                self.r.append(r)

            # Для кожного прайму проверяємо Лежандра и знаходимо корені Тонелли Шенксом
            for i in range(1,len(prime)):
                print("\r"+valcolor(round(float(i)/float(len(prime))*100,2),"%"),end="")
                if legendr(n%prime[i], prime[i]) == 1:
                    tr = tonel(n,prime[i])
                    r = [(tr - q.m) % prime[i],(prime[i] - tr - q.m) % prime[i]]
                    self.p.append(prime[i])
                    self.r.append(r)

            print("\nprime done in time: "+valcolor(round(time() - t,4),"time"))
            print("prime len",valcolor(len(self.p),"data"))

            if B_save:
                # we need to save our factor base in file B_file
                t = time()
                data = [B, n, self.p, self.r]
                with open(B_file, 'wb') as f:
                    pickle.dump(data, f)
                print("\nprime saved in time: "+valcolor(round(time() - t,4),"time"),"in file: "+str(B_file))
        else:
            # B_search == False so we need to upload factor base from B_file
            t = time()
            data = []
            with open(B_file, 'rb') as f:
                data = pickle.load(f)
            if data[0] != B:
                print(valcolor("Primes::Error: wrong B!","strong"))
                exit()
            if data[1] != n:
                print(valcolor("Primes::Error: wrong n!","strong"))
                exit()
            self.p = data[2]
            self.r = data[3]
            print(valcolor("prime upload in time:","strong")+valcolor(round(time() - t,4),"time"),"from file: "+str(B_file))
            print("prime len",valcolor(len(self.p),"data"))

    def __getitem__(self,i):
        return self.p[i]
    def __len__(self):
        return len(self.p)
