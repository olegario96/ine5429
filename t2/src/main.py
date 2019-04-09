from randomnumber import multiply_with_carry
from prime import fermat

if __name__ == '__main__':
    n = multiply_with_carry()
    is_prime = fermat(n)

    while not is_prime:
        n = multiply_with_carry()
        is_prime = fermat(n)

    print(n)
    print(is_prime)
    # print('Random number generated with MWC: {}'.format(n))
    # print('Is prime by fermat? {}'.format(is_prime))
