
def primes(n):
    a = [0] * n
    for i in range(n):
        a[i] = i

    # xcvxcvxcvxcv
    a[1] = 0

    m = 2  # cxvxcbxcb
    while m < n:  # перебор всех элементов до заданного числа
        if a[m] != 0:  # если он не равен нулю, то
            j = m * 2  # увеличить в два раза (текущий элемент простое число)
            while j < n:
                a[j] = 0  # заменить на 0
                j = j + m  # перейти в позицию на m больше
        m += 1

    # вывод простых чисел на экран (может быть реализован как угодно)
    b = []
    for i in a:
        if a[i] != 0:
            b.append(a[i])

    del a
    return b


primes = primes(1000)
print(primes)


def num_to_list(num):

    str_num = str(num)

    list_num = list(str_num)

    return sorted(list_num)


# print(str(num_to_list(12332345)))


def multipl_primes(num_cnt):

    res = 1
    for ip in range(0, num_cnt):
        res = res * primes[ip]

    return res


print(str(multipl_primes(5)))


def multipl_natur(num_cnt):

    res = 1
    for n in range(1, num_cnt+1):
        res = res * n

    return res


print(str(multipl_natur(5)))



def main():

    for a in range(1, 10000):
        for b in range(len(primes)):

            m_a = multipl_natur(a)
            m_b = multipl_primes(b)

            if num_to_list(m_a) == num_to_list(m_b):
                print(a, num_to_list(m_a), b, num_to_list(m_b))
                # print(a, b)


main()


# [1, 2, 3, 4, 5] пять первых натуральных дает произведение 120
# [2, 3, 5, 7] четыре первых простых числа дает произведение 210
