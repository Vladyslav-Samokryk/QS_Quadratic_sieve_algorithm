# -*- coding: utf-8 -*-
import decimal,copy
from valcolor import valcolor
from math import log10
from time import time
import numpy as np
from debug import smooth_output

def GCD(m,n):
    mult = 1
    if m > n:
        m = m % n
    elif n > m:
        n = n % m

    while True:
        if m == 0 or n == 0 or m == n:
            return mult*max(n,m)
        if m == 1 or n == 1:
            return mult

        mm2 = m % 2
        nm2 = n % 2
        if mm2 == 0 and nm2 == 0:
            mult *= 2
            m = m//2
            n = n//2
        elif mm2 == 0 and nm2 != 0:
            m = m//2
        elif mm2 != 0 and nm2 == 0:
            n = n//2
        elif mm2 != 0 and nm2 != 0:
            if n > m:
                piv = (n-m)//2
                n = m
                m = piv
            elif n < m:
                m = (m-n)//2

def eratos(n):
    numbers = list(range(2, n + 1))
    for number in numbers:
        if number != 0:
            for candidate in range(2 * number, n+1, number):
                numbers[candidate-2] = 0
    return list(filter(lambda x: x != 0, numbers))

class Q:
    def __init__(self,n):
        self.n = n
        self.m = int(decimal.Decimal(n).sqrt() + 1)
    def __call__(self,x):
        return (x + self.m)**2 - self.n

def legendr(a, p):
    return pow(a, (p - 1) // 2, p)

def tonel(n, p):
    assert legendr(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)

    z = 2
    for z in range(2, p):
        if p - 1 == legendr(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def smooth_reg(L1, L2, q, primes):
    t = time()
    # всі значення між L1 и L2
    res0 = list(range(L1, L2))
    # одиниця означає, що число під ціи індексом гладке
    res1 = np.array([q(x) for x in range(L1, L2)])
    # масив з розкладених чисел по простим
    res2 = np.zeros((len(res0), len(primes)), dtype="int8")
    table_creation_time = time() - t

    t = time()
    # просто для статистики (скільки простих взагалі не потрапило до просіювання в
    # нашу область)
    primes_skipped = 0
    # підгоняем r до [L1, L2] => отримуємо s
    # ініціалізуємо масив сдвинутих r (робимо це для того, щоб не шукати з
    # нуля, а шукати вже в [L1, L2])
    s = [[] for _ in range(len(primes.r))]
    for smooth_idx, prime in enumerate(primes):
        # print("\rshift "+'\033[92m'+str(round(float(i)/float(len(primes))*100,2))+'\033[0m'+" %",end="")
        for r in primes.r[smooth_idx]:
            # отримуємо приблизну оцінку, скільки праймів потрібно пропустимти
            k = L1 // prime
            # уточнюємо оцінку
            while r + k*prime >= L1:
                k -= 1
            k+=1
            # якщо отримане число виходить за рамки області, то в подальшому,
            # ми его взагалі не будемо перевіряти(if просто для статистики)
            if r + k*prime >= L2:
                primes_skipped += 1
            # при просіюванні, починаємо одразу з цієї позиції
            s[smooth_idx].append(r + k*prime)

    s_search_time = time() - t

    t = time()
    for prime_idx, prime in enumerate(primes):
        # print("\rsuive "+'\033[92m'+str(round(float(p)/float(len(primes))*100,2))+'\033[0m'+" %",end="")
        for s_i in s[prime_idx]:
            if s_i < L2:
                # гарантуємо, що починаючи з s_1 - L1, кожне час prime ділиться на prime хоча б 1 раз
                res2[s_i - L1::prime, prime_idx] += 1
                res1[s_i - L1::prime] //= prime
                # ділення перевіряємо вручну
                for smooth_idx in range(s_i, L2, prime):
                    x = smooth_idx - L1
                    while res1[x] % prime == 0:
                        res1[x] //= prime
                        res2[x, prime_idx] += 1

    prime_div_time = time() - t

    t = time()
    ans = []
    for smooth_idx, qx in enumerate(res1):
        if abs(qx) == 1:
            ans.append([res0[smooth_idx],q(res0[smooth_idx]),np.copy(res2[smooth_idx])])
        # if abs(res1[smooth_idx]) == 1:

    answer_fill_time = time() - t
    smooth_output(table_creation_time, s_search_time, prime_div_time,
                         answer_fill_time, ans, L1, L2, primes_skipped, primes)

    return ans


# TODO:
#   + implement slice handling
def get_region(idx, step):
    """
    return unique region for specified index
    if index is even: return positive
                 odd: return negative
    """
    # парні: додатній знак, непарні: відємний
    sign = (idx % 2) * (-1)
    if sign == 0:
        return [idx * step, (idx + 1) * step]
    else:
        return [- (idx) * step, - (idx - 1) * step]
