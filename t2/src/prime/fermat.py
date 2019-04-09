import random

def fermat(n, k=10):
    """ Implements the Fermat theorem. If
    number is lesser than 2 or is divisible for
    2, for sure is not a prime number. The
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

    for i in range(k):
        a = random.randint(2, n - 2)
        result = pow(a, n-1, n)
        if result != 1:
            return False

    return True

if __name__ == '__main__':
    print(fermat(153002247429829))
