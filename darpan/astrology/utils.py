from random import randint


l = [randint(30,150) for i in range(1000)] + [25, 25, 180]
l= sorted(l)


def percentile(numbers):
    numbers = sorted(numbers)
    l = len(numbers)
    d = {}
    for i, n in enumerate(numbers):
        if n not in d:
            d[n] = (i+1)/float(l)
    
    p = []
    min_ = min(d.keys())
    max_ = max(d.keys())
    last = 0
    for i in range(200):
        if i< min_:
            last = 0
            p.append(last)
        elif i in d:
            last = d[i]
            p.append(last)
        else:
            p.append(last)
            
    
    return p

p = percentile(l)
for i,n in enumerate(p):
    print(i,n)
