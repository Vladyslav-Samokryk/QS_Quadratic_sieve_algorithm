from valcolor import valcolor
from data import Verbose_level

def smooth_output(table_creation_time, s_search_time, prime_div_time,
                         ans_fill_time, ans, L1, L2, primes_skipped, primes):
    if Verbose_level >= 2:
        data = "Table: "+valcolor(round(table_creation_time,4),'time')+"\n"
        data += "S: "+valcolor(round(s_search_time,4),'time')+"\n"
        data += "Prime div: "+valcolor(round(prime_div_time,4),'time')+"\n"
        data += "Answer: "+valcolor(round(ans_fill_time,4),'time')+"\n"
        data += valcolor(len(ans),'data')+" in ["+str(L1)+"..."+str(L2)+"]"
        data += " in time "+valcolor(round(table_creation_time + s_search_time +\
                                        prime_div_time + ans_fill_time ,4),'time')
        data += " skip: "+valcolor(round(primes_skipped/(2*len(primes))*100,2),'%')+"\n"

def suive_output(smooth_numbers, primes):
    """
    output progress of searching smooth_numbers in general

    smooth_numbers: array of [x, qx, exp_vector]
    primes:         Primes instance
    """
    if Verbose_level >= 1:
        print("\rfound: {0}/{1} {2}".format(
            valcolor(len(smooth_numbers),'data'),
            valcolor(len(primes),'data'),
            valcolor(round(len(smooth_numbers)*100/len(primes),2),"%")
        ), end="")
    if Verbose_level >= 2:
        print("\nfound:",valcolor(len(smooth_numbers),'data')+"/"+valcolor(len(primes),'data'),valcolor(round(float(len(smooth_numbers))/float(len(primes))*100,2),"%")+"\n")
