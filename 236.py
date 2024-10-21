from front import *

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

def count_sqr(a: float, b:float, c: float):
    D = float(b ** 2 - 4*a*c)
    x1 = (-b + D ** (1/2))/(2*a)
    x2 = (-b - D ** (1 / 2)) /(2 * a)
    if (x1 != x2):
        return 2
    else:
        return 1


hello()

def main():
    a = int(input())
    b = int(input())
    c = int(input())
    d = sqr_func(a,b,c)
    if (d == -1):
        error()
    else:
        if (count_sqr(a,b,c) == 2):
            two_sqrt()
        else:
            one_sqrt()
        print(d)

if __name__ == "__main__":
    main()


