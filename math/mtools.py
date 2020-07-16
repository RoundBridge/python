'''
    description:    计算x的n次方
    version:        0.0.1
    date:           2020.7.16
'''

def power(x,n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
