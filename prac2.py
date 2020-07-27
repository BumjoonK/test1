#! /usr/bin/env python

d_krw={"USD":"1,203.82","EUR":"1,365.73","JPY":"11.22","CNY":"172.04"}
calc="10 USD, 5 EUR, 7 JPY, 9 CNY"

cal=calc.replace(",","")
cal=cal.split(" ")

i,s,n =0,0,""
for i in range(0,len(cal),2):
    n=d_krw[cal[i+1]].replace(",","")
    s=int(cal[i])*float(n)
    print(round(s,2),"KRW")
