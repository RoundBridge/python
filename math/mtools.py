'''
    description:    生成斐波那契序列内部函数，使用了yield，故该函数是生成器函数，
                    返回一个生成器
    version:        0.0.1
    date:           2020.7.16
'''
def _fibonacci_(n):
    a, b, counter = 0, 1, 0
    while True:
        if counter > n:
            return
        yield a
        a, b = b, a + b
        counter += 1
'''
    description:    生成斐波那契序列外部调用函数，返回一个list
    version:        0.0.1
    date:           2020.7.16
'''
def fibonacci(n):
    ret = []
    g = _fibonacci_(n)

    while True:
        try:
            ele = next(g)
            ret.append(ele)
        except StopIteration:
            return ret


'''
    description:    判断是否是闰年，返回True or False
    version:        0.0.1
    date:           2020.7.16
'''
def is_leap_year(year):
    if 0 == (year % 100):
        year = year/100
        if 0 == (year % 4):
            return True
    elif 0 == (year % 4):
        return True
    else:
        pass
    return False




if __name__ == '__main__':
    print((is_leap_year(1904)))