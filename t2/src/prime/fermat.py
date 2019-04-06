def fermat(n):
    """ Implements the Fermat theorem. The
    theorem says that if a number n is prime,
    that any number between 1 and n - 1 pow
    n - 1 divided by n will remaind exactly
    one. If there is a, that do not attend
    this condition, so, for sure, n it is
    not a prime number. Otherwise, n is
    , probably with a great chance,
    prime.

        Params:
            n (int): the number that will
            be checked if is prime or not.

        Returns: boolean. If True, n is
        probably a prime number. If False,
        for certain is not a prime number.
    """
    if n != 2 and n % 2 == 0:
        return False

    for a in range(1, n - 1):
        result = (a**(n-1)) % n
        if result != 1:
            return False

    return True

if __name__ == '__main__':
    """ Uses 49 as base test.
    """
    fermat(49)
