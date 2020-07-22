#! /usr/bin/env python
"""
def ft(fruit):
    print('fruit:', fruit)
    return fruit + 'tree'
ft('apple')

tree=ft('peach')

print(tree)

def add(a,b):
    print('add',a,'and',b)
    print('%d+%d=' %(a,b), a+b)
    return a,b, a+b

A, B, result = add(3,4)
print('result A', A)
print('result B', B)
print('result result', result)

def book(name, age, book1, book2):
    print(name, age, book1, book2)
    return name

name1 = book('name1','100','C','C++')
print('name1:', name1)

#name2 =book('name1','100','C','C++','Python')
#print('name2:', name2)
#book 함수 인자는 4개여야하는데 5개를 입력해서 오류 발생
"""
"""
def book(name, age, *book):
    print(name, age, end=" ")
    for i in book:          #*로서 book이라는 변수에 매개변수 입력 가능
        print(i, end=' ')
    print()
    return name
name1 = book('name1', '100','C','C++')

"""
"""
def book(name, age, *book):
    print(name, age, end=" ")
    for abcde in book:
        print(abcde, end=' ')
    print()
    return name

name1 = book('name1', '100','C','C++')
print('name1', name1)

name2 = book('name2', '100','C','C++','Python','AAAAA')
print('name2',name2)

"""

def SUM(x,y):
    return x+y

i_lambda =(lambda x,y : x+y)(3,4)

i_func = SUM(3,4)

print(i_lambda)
print(i_func)

