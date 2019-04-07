import random
import time

CMWC_CYCLE = 4096
CMWC_C_MAX = 809430660

def rand32():
    result = random.randint(0, 2**2048)
    return result << 16 | random.randint(0, 2**2048)

def init_cmwc(q, c, i, seed):
    global CMWC_CYCLE

    random.seed(seed)

    for i in range(CMWC_CYCLE):
        q[i] = rand32()

    while True:
        c = rand32()
        if c >= CMWC_C_MAX:
            break

    i = CMWC_CYCLE - 1
    return q, c, i

def rand_cmwc(q, c, i):
    global CMWC_CYCLE

    A = 18782
    M = 0xFFFFFFFE

    i = (i + 1) & (CMWC_CYCLE - 1)
    t = A * q[i] + c
    c = t >> 32
    x = t + c

    if (x < c):
        x += 1
        c += 1

    q[i] = x - M
    return q[i]

def mersenne_twister():
    global CMWC_CYCLE

    q = [0] * CMWC_CYCLE
    c, i = 0, 0

    seed = int(round(time.time()))
    q, c, i = init_cmwc(q, c, i, seed)
    return rand_cmwc(q, c, i)

if __name__ == '__main__':
    print(mersenne_twister())
