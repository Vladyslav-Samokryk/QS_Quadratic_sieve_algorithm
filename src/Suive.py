# -*- coding: utf-8 -*-
import pickle
from time import time

from data import Smooth_search, Smooth_file, Smooth_save
from data import n, B, step
from data import Search_smooth_par
from valcolor import valcolor
from lib import smooth_reg

from debug import suive_output

# for multiprocessing
import multiprocessing as mp
from lib import get_region
# indicate workers to stop
from ctypes import c_bool
# settings for multiprocessing
from data import maxParProc as proc_max

def worker_task(region_idx, stop_working, answer_queue, primes, q):
    while True:
        # process safe read and write operation
        with region_idx.get_lock():
            local_region_idx  = region_idx.value
            region_idx.value += 1

        # exit if we reached maximum
        if stop_working.value:
            break
        region = get_region(local_region_idx, step)
        # calculate answer
        answer = smooth_reg(*region, q, primes)
        # return it
        answer_queue.put(answer)

def suive(q, primes):
    if Search_smooth_par:
        mp.set_start_method('spawn')
        # mp.set_start_method("spawn", force=True)
        MAX_SMOOTH_QTY = len(primes)
        print("MAX_SMOOTH_QTY:", MAX_SMOOTH_QTY)
        # ініціалізуємо lock-safe чергу для відповідей
        answer_queue = mp.Queue()
        # створюємо працюючі процеси
        workers = []
        # індекс регіону
        region_idx = mp.Value('i', 0)
        # чи потрібно зупинятись воркерам
        stop_workers = mp.Value(c_bool, False)
        # ініціалізуємо процеси
        for worker_id in range(proc_max):
            workers.append(mp.Process(
                target=worker_task,
                args=(region_idx, stop_workers, answer_queue, primes, q)
            ))
        for worker in workers:
            worker.start()
        # зчитуємо з черги відповідей в нашу локальну змінну
        smooth_numbers = []
        while len(smooth_numbers) < MAX_SMOOTH_QTY:
            smooth_numbers.extend(answer_queue.get())
            suive_output(smooth_numbers, primes)
        else:
            # для того щоб наступні лінії не продовжувались разом з прогрес баром
            # Треба поставити нову лінію
            print()
        # кажемо воркерам закінчити
        stop_workers.value = True
        # Чекаємо на закінчення
        for idx, worker in enumerate(workers):
            worker.kill()
        return smooth_numbers
    elif Smooth_search:
        # Smooth_search == True so we need to find our smooth numbers
        print("step:",valcolor(step,"data"))
        k = 1
        # found_smooth = 0
        smooth_numbers = []
        while q((k-1)*step) < n:
            ans = smooth_reg((k-1)*step,k*step,q,primes)
            for i in range(len(ans)):
                smooth_numbers.append(ans[i])
            ans = smooth_reg(-k*step,-(k-1)*step,q,primes)
            for i in range(len(ans)):
                smooth_numbers.append(ans[i])
            k+=1
            print("Total number of smooth numbers:",valcolor(len(smooth_numbers),'data'))
            if len(smooth_numbers) > len(primes):
                # Вихід з функції
                if Smooth_save:
                    # we need to save our smooth numbers in file Smooth_file
                    t = time()
                    data = [B, n, smooth_numbers]
                    with open(Smooth_file, 'wb') as f:
                        pickle.dump(data, f)
                    print("\nsmooth numbers saved in time: "+valcolor(round(time() - t,4),"time"),"in file: "+str(Smooth_file))
                return smooth_numbers
    else:
        # Smooth_search == False so we need to upload factor base from Smooth_file
        t = time()
        data = []
        smooth_numbers = []
        with open(Smooth_file, 'rb') as f:
            data = pickle.load(f)
        if data[0] != B:
            print(valcolor("Suive::Error: wrong B!","strong"))
            exit()
        if data[1] != n:
            print(valcolor("Suive::Error: wrong n!","strong"))
            exit()
        smooth_numbers = data[2]
        print(valcolor("smooth upload in time:","strong")+valcolor(round(time() - t,4),"time"),"from file: "+str(Smooth_file))
        print("smooth len",valcolor(len(smooth_numbers),"data"))
        return smooth_numbers
