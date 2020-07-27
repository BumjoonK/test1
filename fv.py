#! /usr/bin/env python

l_pivo=[0,1]
pivoIn=int(input('n_th pivo:'))

for i in range(pivoIn -2): #2는 length l_pivo
    l_pivo.append(l_pivo[-1]+l_pivo[-2])
print(l_pivo[-1])

