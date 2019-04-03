
from enum import Enum

HEX_MASK = 0xFFFFFFFF

class CipherMode(Enum):
    M_ENCIPHER = 0
    M_DECIPHER = 1
    M_NONE = 2

randrsl = [0] * 256
mm = [0] * 256

aa = 0
bb = 0
cc = 0
randcnt = 0

MOD = 95
START = 32

v = [0] * 4096
c = [0] * 4096

def mix(a, b, c, d, e, f, g, h):
    a ^= b << 11&HEX_MASK; d += a; d &= HEX_MASK; b +=c; b &= HEX_MASK
    b ^= c >> 2; e += b; e &= HEX_MASK; c += d; c &= HEX_MASK
    c ^= d << 8&HEX_MASK; f += c; f &= HEX_MASK; d += e; d &= HEX_MASK
    d ^= e >> 16; g += d; g &= HEX_MASK; e += f; e &= HEX_MASK
    e ^= f << 10&HEX_MASK; h += e; h &= HEX_MASK; f += g; f &= HEX_MASK
    f ^= g >> 4; a += f; a &= HEX_MASK; g += h; g &= HEX_MASK
    g ^= h << 8&HEX_MASK; b += g; b &= HEX_MASK; h += a; h &= HEX_MASK
    h ^= a>> 9; c +=h; c &= HEX_MASK; a += b; a &= HEX_MASK
    return a, b, c, d, e, f, g, h


def isaac():
    global aa, bb, cc, randcnt

    cc += 1
    bb += cc

    for i in range(0, 256):
        x = mm[i]
        mod = i % 4
        if mod == 0:
            aa = aa^(aa << 13)&HEX_MASK
        elif mod == 1:
            aa = aa^(aa >> 6)
        elif mod == 2:
            aa = aa^(aa << 2)&HEX_MASK
        elif mod == 3:
            aa = aa^(aa >> 16)

        aa = mm[(i + 128) % 256] + aa
        mm[i] = y = mm[(x >> 2) % 256] + aa + bb
        randrsl[i] = bb = mm[(y >> 10) % 256] + x

    randcnt = 0

def rand_init(flag):
    global aa, bb, cc, randrsl, randcnt
    aa = bb = cc = 0
    a = b = c = d = e = f = g = h = 0x9e3779b9

    for i in range(0, 4):
        a, b, c, d, e, f, g, h = mix(a, b, c, d, e, f, g, h)

    for i in range(0, 256, 8):
        if flag:
            a += randrsl[i]
            b += randrsl[i + 1]
            c += randrsl[i + 2]
            d += randrsl[i + 3]
            e += randrsl[i + 4]
            f += randrsl[i + 5]
            g += randrsl[i + 6]
            h += randrsl[i + 7]

        a, b, c, d, e, f, g, h = mix(a, b, c, d, e, f, g, h)
        mm[i] = a
        mm[i + 1] = b
        mm[i + 2] = c
        mm[i + 3] = d
        mm[i + 4] = e
        mm[i + 5] = f
        mm[i + 6] = g
        mm[i + 7] = h

    if flag:
        for i in range(0, 256, 8):
            a += mm[i]
            b += mm[i + 1]
            c += mm[i + 2]
            d += mm[i + 3]
            e += mm[i + 4]
            f += mm[i + 5]
            g += mm[i + 6]
            h += mm[i + 7]

            a, b, c, d, e, f, g, h = mix(a, b, c, d, e, f, g, h)

            mm[i] = a
            mm[i + 1] = b
            mm[i + 2] = c
            mm[i + 3] = d
            mm[i + 4] = e
            mm[i + 5] = f
            mm[i + 6] = g
            mm[i + 7] = h

    isaac()
    randcnt = 0

def i_random():
    global randrsl, randcnt

    r = randrsl[randcnt]
    randcnt += 1
    if (randcnt > 255):
        isaac()
        randcnt = 0

    return r

def i_rand_a():
    return i_random() % 95 + 32

def i_seed(seed, flag):
    global randrsl, mm

    for i in range(0 , 256):
        mm[i] = 0

    m = len(seed)

    for i in range(0, 256):
        if i >= m:
            randrsl[i] = 0
        else:
            randrsl[i] = seed[i]

    rand_init(flag)

def vernam(msg):
    global v

    l = len(msg)
    for i in range(0, l):
        v[i] = 0

    for i in range(0, l):
        if type(msg[i]) == str:
            v[i] = i_rand_a() ^ ord(msg[i])
        elif type(msg[i]) == int:
            v[i] = (i_rand_a() & 0xFF) ^ msg[i]

    return bytes(v)

def caesar(m, ch, shift, modulo, start):
    if (m == CipherMode.M_DECIPHER):
        shift = -shift

    if type(ch) == str:
        ch_ = ord(ch)
    elif type(ch) == int:
        ch_ = ch

    n = (ch_-start) + shift
    n = n % modulo
    if n < 0:
        n += modulo
    return start + n

def caesar_str(m, msg, modulo, start):
    global c

    l = len(msg)

    for i in range(0, l):
        c[i] = 0

    for i in range(0, l):
        c[i] = caesar(m, msg[i], i_rand_a(), modulo, start)

    return bytes(c)

def main_inversive():
    global MOD, START

    msg = 'a Top Secret secret'.encode('ascii')
    key = 'this is my secret key'.encode('ascii')

    l = len(msg)

    i_seed(key, True)
    vctx = vernam(msg)
    cctx = caesar_str(CipherMode.M_ENCIPHER, msg, MOD, START)

    i_seed(key, True)
    vptx = vernam(vctx)
    cptx = caesar_str(CipherMode.M_DECIPHER, cctx, MOD, START)

    print('Message {}'.format(msg))
    print('Key {}'.format(key))
    print('XOR')

    for i in range(0, l):
        print(vctx[i])

    print('XOR dcr: {}'.format(vptx))
    print('MOD: ')
    for i in range(0, l):
        print(cptx[i])

    print('MOD dcr: {}'.format(cptx))
