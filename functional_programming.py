from functools import reduce
# List comprehension
def lstSquare(lst):
    res = []
    for i in lst:
        res.append(i*i)
    return res

def lstcomSquare(lst):
    return [i*i for i in lst]

def mapLstSquare(n):
    return list(map(lambda x: x * x, range(1, n + 1)))

def mapLstSquareLst(lst):
    return list(map(lambda x: x * x, lst))

def rangeComSquare(n):
    return [i*i for i in range(1, n+1)]

def flatten(lst):
    return [j for i in lst for j in i]

""" High-order function
Các hàm này nhận đầu vào là 1 hàm và trả về là 1 hàm khác.
map:

filter:

reduce:

"""
def dist(lst, n):
    return list(map(lambda x: (x, n), lst)) # Voi x bat ky thi tra ve gi

def lessThan(lst, n):
    return list(filter(lambda x: x < n, lst)) # Voi x bat ky thi dieu kien giu lai la gi?
def sumReduce(lst):
    return reduce(lambda acc, cur: cur + acc, lst, 0) # acc: phan tu phia truoc, cur: phan tu hien tai, list, tham so khoi dau?
def lessThanReduce(lst, n):
    return list(reduce(lambda acc, cur: acc + [cur] if cur < n else acc + [], lst, []))

def flattenReduce(lst):
    return list(reduce(lambda acc, cur: acc + cur, lst, []))
def main():
    lst = [12,4,5,6]
    lst2 = [1,2,3,4,5]
    flatten_lst = [[1,2,3], [4,5], [6,7]]
    print(lstcomSquare(lst))
    print(mapLstSquareLst(lst))
    print(rangeComSquare(3))
    print(mapLstSquare(3))
    
    print(dist(lst, 3))
    print(lessThan(lst, 10))
    # print(sumReduce(lst2))
    print(lessThanReduce(lst, 10))
    print(flatten(flatten_lst))
    print(flattenReduce(flatten_lst))
    
if __name__ == "__main__":
    main()