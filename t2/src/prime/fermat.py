def fermat(n):
    if n != 2 and n % 2 == 0:
        return False

    for a in range(1, n - 1):
        result = (a**(n-1)) % n
        if result != 1:
            return False

    return True

if __name__ == '__main__':
    fermat(49)
