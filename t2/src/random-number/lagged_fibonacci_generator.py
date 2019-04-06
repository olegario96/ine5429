class OutOfRange(Exception):
    def __ini__(self, *args, **kwargs):
        default_message = 'j must be greater than 0 and k must be greater than j'
        if not (args or kwargs): args = (default_message,)

def fibonacci_sequence(n):
    s0 = 0
    s1 = 1
    sequence = []

    for i in range(n):
        if i == 0:
            sequence.append(s0)
        elif i == 1:
            sequence.append(s1)
        else:
            s2 = sequence[i-1] + sequence[i-2]
            sequence.append(s2)

    return sequence

def lagged_fibonacci_generator(j, k, m=2**64):
    if 0 >= j or j >= k:
        raise OutOfRange

    n = k
    s = fibonacci_sequence(n)
    return [((s[i-j] + s[i-k]) % m) for i in range(n)]

if __name__ == '__main__':
    print(lagged_fibonacci_generator(418, 1279))
