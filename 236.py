def sqr_func(a: float, b:float, c: float):
    D = float(b ** 2 - 4*a*c)
    if D < 0:
        return -1
    x1 = (-b + D ** (1/2))/(2*a)
    x2 = (-b - D ** (1 / 2)) /(2 * a)
    if (x1 != x2):
        return x1, x2
    else:
        return x1

a = int(input())
b = int(input())
c = int(input())
d = sqr_func(a,b,c)
print(d)