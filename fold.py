from random import randint

printable = r"""0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable_len = len(printable)


def conversion_n(n):
    """返回n的94进制数(以printable来表示)

    :param n: 数据
    :return: 计算后的数据
    """
    x = printable_len
    res = []
    if n < x:
        res = [n]
    else:
        while n // x >= 1:
            res.append(n % x)
            n = n // x
        if n % x != 0:
            res.append(n % x)
        res = res[::-1]
    n = ''
    for i in res:
        n += printable[i]
    return n


def conversion_10(n):
    """返回n的10进制数(以printable来表示)

    :param n: 数据
    :return: 计算后的数据
    """
    n_ = 0
    n = n[::-1]
    for i in range(len(n)):
        n_ += printable.index(n[i]) * printable_len ** i
    return n_


def fold(n):
    """进行一层解密运算

    :param n: 数据
    :return: 计算后的数据
    """
    n_ = []
    for i, ii in zip(n[:len(n) // 2], n[len(n) // 2:]):
        n_.append(i ^ ii)
    return bytes(n_)


def folds(n, len_=None, num=None, callback=None, callback_args=(), callback_kwargs=None):
    """对数据进行解密(len_与num有一个即可)

    :param n: 数据
    :param len_: 数据原长度
    :param num: 数据解密运算层数
    :param callback: 回调函数，给予参数(每轮解密前的数据)，返回值将进行下一次解密
    :param callback_args: 回调函数的参数
    :param callback_kwargs: 回调函数的参数
    :return: 解密后的数据
    """
    if callback_kwargs is None:
        callback_kwargs = {}
    if len_ is num is None:
        raise TypeError('folds() missing 1 required positional argument: "len_" or "num"')
    elif len_ is not None and num is not None:
        raise TypeError('folds() takes 2 positional arguments but 3 were given')
    if callback is None:
        if len_ is not None:
            while True:
                if len(n) <= len_:
                    return n
                n = fold(n)
        else:
            for i in range(num):
                n = fold(n)
            return n
    else:
        if len_ is not None:
            while True:
                n = callback(n, *callback_args, **callback_kwargs)
                if len(n) <= len_:
                    return n
                n = fold(n)
        else:
            for i in range(num):
                n = fold(callback(n, *callback_args, **callback_kwargs))
            return n


def increase(n):
    """进行一层加密运算

    :param n: 数据
    :return: 计算后的数据
    """
    n1 = []
    n2 = []
    for i in n:
        ii = randint(0, 255)
        n1.append(i ^ ii)
        n2.append(ii)
    return bytes(n1 + n2)


def increases(n, len_=None, deviation='big', num=None,
              callback=None, callback_args=(), callback_kwargs=None):
    """对数据进行加密(len_与num有一个就可以了)

    :param n: 数据
    :param len_: 数据加密后的长度(不一定等于len_)
    :param deviation: 可以比len_长还是可以比len_短('big' or 'little')
    :param num: 加密的层数
    :param callback: 回调函数，给予参数(每轮加密前的数据)，返回值将进行下一次加密
    :param callback_args: 回调函数的参数
    :param callback_kwargs: 回调函数的参数
    :return: 加密后的数据
    """
    if callback_kwargs is None:
        callback_kwargs = {}
    if len_ is num is None:
        raise TypeError('increases() missing 1 required positional argument: "len_" or "num"')
    elif len_ is not None and num is not None:
        raise TypeError('increases() Take "len_" or "num" as one of the arguments, but give 2')
    if callback is None:
        if len_ is not None:
            if deviation == 'big':
                while True:
                    if len(n) >= len_:
                        return n
                    n = increase(n)
            elif deviation == 'little':
                while len(n) < len_:
                    n = increase(n)
                return n
            else:
                raise TypeError(f'increases() "deviation" is expected to be "big" or "little", but is"{deviation}"')
        else:
            for i in range(num):
                n = increase(n)
            return n
    else:
        if len_ is not None:
            if deviation == 'big':
                while True:
                    n = callback(n, *callback_args, **callback_kwargs)
                    if len(n) >= len_:
                        return n
                    n = increase(n)
            elif deviation == 'little':
                while len(n) < len_:
                    n = increase(callback(n, *callback_args, **callback_kwargs))
                return n
            else:
                raise TypeError(f'increases() "deviation" is expected to be "big" or "little", but is"{deviation}"')
        else:
            for i in range(num):
                n = increase(callback(n, *callback_args, **callback_kwargs))
            return n


def increases_conversion(n, len_=None, deviation='big', num=None,
                         callback=None, callback_args=(), callback_kwargs=None):
    """对数据进行加密并用94进制表示(len_与num有一个就可以了)

    :param n: 数据
    :param len_: 数据加密后的长度(不一定等于len_)
    :param deviation: 可以比len_长还是可以比len_短('big' or 'little')
    :param num: 加密的层数
    :param callback: 回调函数，给予参数(每轮加密前的数据)，返回值将进行下一次加密
    :param callback_args: 回调函数的参数
    :param callback_kwargs: 回调函数的参数
    :return: 加密后的数据
    """
    if callback_kwargs is None:
        callback_kwargs = {}
    n = increases(**locals())
    n1 = ''
    for i in n:
        i = conversion_n(i)
        if len(i) == 1:
            i = '0' + i
        n1 += i
    return n1


def folds_conversion(n, len_=None, num=None,
                     callback=None, callback_args=(), callback_kwargs=None):
    """对数据用十进制表示并进行解密(len_与num有一个即可)

    :param n: 数据
    :param len_: 数据原长度
    :param num: 数据解密运算层数
    :param callback: 回调函数，给予参数(每轮解密前的数据)，返回值将进行下一次解密
    :param callback_args: 回调函数的参数
    :param callback_kwargs: 回调函数的参数
    :return: 解密后的数据
    """
    n_ = []
    for i in range(0, len(n), 2):
        n_.append(conversion_10(n[i: i + 2]))
    n = n_
    del i, n_
    return folds(**locals())
