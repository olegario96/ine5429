class OutOfRange(Exception):
    def __ini__(self, *args, **kwargs):
        default_message = 'a must be greater than 1 and less than n - 1'
        if not (args or kwargs): args = (default_message,)

        super().__init__(*args, **kwargs)

def calculate_k_m(n):
    """ Finds the greater 2 pow that
    divides the n number, in the field
    of the integers.

        Params:
            n (integer): the number that
            will have the primality checked

        Return tuple: the greates power of
        two that divides the number, and the
        composite part of n
    """
    k = 0
    n -= 1
    m0, m1 = 0, 0
    while (n % pow(2, k)) == 0:
        k += 1
        m0 = m1
        m1 = n // pow(2, k)

    return k - 1, int(m0)

def miller_rabin(n, a=10):
    """ Implements Miller Rabin algorithm
    to check if a n number is prime or not.
    It uses a number to check the primality
    for n. Calculates its k, m values and check
    if they have a correct range. Than, will
    loop until reach the period of the mod function
    or the mod of the division be 1 or n - 1.

        Params:
            n (int): the number that will have the
            primality checked
            a (int): number used to check if n is
            prime or not

        Returns boolean: False if n is for sure
        not a prime number. Otherwise, return True,
        indicating that is probably a prime number.
    """
    if n != 2 and n % 2 == 0:
        return False

    k, m = calculate_k_m(n)

    if 1 > a or a > n - 1:
        raise OutOfRange('a must be greater than 1 and less than n - 1')

    b0 = pow(a, m, n)
    i = 0
    while (b0 != n - 1 and b0 != 1) and (i < k - 1):
        b0 = pow(a, b0, n)
        i += 1

    if i > 1:
        if b0 == 1:
            return False
        elif b0 == n - 1:
            return True
        else:
            return False
    else:
        return True

if __name__ == '__main__':
    print(miller_rabin(37635410187193800209006478881, 5))
