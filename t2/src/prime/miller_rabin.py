class OutOfRange(Exception):
    def __ini__(self, *args, **kwargs):
        default_message = 'a must be greater than 1 and less than n - 1'
        if not (args or kwargs): args = (default_message,)

        super().__init__(*args, **kwargs)

def calculate_k_m(n):
    k = 0
    n -= 1
    m0, m1 = 0, 0
    while (n % (2**k)) == 0:
        k += 1
        m0 = m1
        m1 = n / (2**k)

    return k - 1, m0

def miller_rabin(n, a):
    k, m = calculate_k_m(n)

    if 1 > a or a > n - 1:
        raise OutOfRange('a must be greater than 1 and less than n - 1')

    b0 = m
    i = 0
    while b0 != n -1 and b0 != 1:
        b0 = (2**b0) % n
        i += 1

    if i > 1:
        if b0 == 1:
            return False
        elif b0 == n - 1:
            return True
    else:
        return True

if __name__ == '__main__':
    print(miller_rabin(53, 2))
