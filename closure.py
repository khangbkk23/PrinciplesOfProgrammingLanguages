def make_multi(n):
    def multi(x):
        return x * n
    return multi

def enter_number():
    num = []
    def inner(x):
        num.append(x)
        print(num)
    return inner


temp = make_multi(5)
print(temp(5))


temp = enter_number()
temp(12)
temp(13)
temp(14)