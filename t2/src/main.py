import prime
import randomnumber
import sys

if __name__ == '__main__':
    arg = sys.argv[len(sys.argv)-1]

    n = 0
    is_prime = False

    if arg == '--fermat':
        while not is_prime:
            n = randomnumber.multiply_with_carry()
            is_prime = prime.fermat(n)
        print('Random number generated with MWC: {}'.format(n))
        print('Is prime by fermat? {}'.format(is_prime))
    elif arg == '--miller':
        while not is_prime:
            n = randomnumber.multiply_with_carry()
            is_prime = prime.miller_rabin(n)
        print('Random number generated with MWC: {}'.format(n))
        print('Is prime by miller? {}'.format(is_prime))
