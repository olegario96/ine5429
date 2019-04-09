from enum import Enum
from dotenv import load_dotenv

import os

load_dotenv('.env')
load_dotenv('../.env')

class CipherMode(Enum):
    M_ENCIPHER = 0
    M_DECIPHER = 1
    M_NONE = 2

FIVE_ONE_TWO = 512
randrsl = [0] * FIVE_ONE_TWO
mm = [0] * FIVE_ONE_TWO

aa = 0
bb = 0
cc = 0
randcnt = 0

MOD = 95
START = 32

v = []
c = []

def mix(a, b, c, d, e, f, g, h):
    """
        Mix the variables passed as
        argument to looks like just
        a random data. It shift
        and sum they. The shift values
        are defined by the algorithm.

        Returns: tuple containing the
        new values for a, b, c, d, e, f,
        g, h. This is necessary, because Python
        uses a copy in params for primary types.

    """
    a ^= (b << 11); d += a; b +=c
    b ^= c >> 2; e += b; c += d
    c ^= (d << 8); f += c; d += e
    d ^= e >> 16; g += d; e += f
    e ^= (f << 10); h += e; f += g
    f ^= g >> 4; a += f; g += h
    g ^= (h << 8); b += g; h += a
    h ^= a >> 9; c +=h; a += b
    return a, b, c, d, e, f, g, h

def isaac():
    """
        Implements the base algorithm for
        the ISAAC Cypher. Uses a period
        of 4 to check how the should
        be shifted. Store the result on
        the global buffer randrsl to save
        the pseudo random numbers. Finally,
        resets the counter that is used to
        check when the isaac should be
        called or not.

        Returns: None. As it stores all
        the result on global variables,
        no return is necessary.
    """
    global aa, bb, cc, randcnt

    cc = cc + 1
    bb = (bb + cc)

    for i in range(0, 256):
        x = mm[i]
        mod = i % 4
        if mod == 0:
            aa = aa ^ (aa << 13)
        elif mod == 1:
            aa = aa ^ (aa >> 6)
        elif mod == 2:
            aa = aa ^ (aa << 2)
        elif mod == 3:
            aa = aa ^ (aa >> 16)

        aa = mm[(i + 128) % 256] + aa
        mm[i] = y = mm[(x >> 2) % 256] + aa + bb
        randrsl[i] = bb = mm[(y >> 10) % 256] + x

    randcnt = 0

def rand_init(flag):
    """ Implements the randomness to generate pseudo
        random integers, based on ISAAC algorithm
        definition. Starts the pointers a ~ h,
        on the preset memory value. Calculate
        the values, call the isaac method and
        reset the counter to call again the
        isaac method.

        Args:
            flag (boolean): if True, use the global
            buffer randrsl to initialize the global
            buffer mm.

        Returns: None. As it stores all
        the result on global variables,
        no return is necessary.
    """
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
    """Generate a pseudo random integer
        based on the globals randcnt variable
        and randrsl buffer. Will save the
        the result on a variable, and increments
        the pointer. It the variable is greater
        than 256 (the default value for the message
        len), will run again the isaac algorithm
        and reset the pointer.

        Returns: returns a periodic pseudo random
        integer
    """
    global randrsl, randcnt

    r = randrsl[randcnt]
    randcnt += 1
    if (randcnt > 255):
        isaac()
        randcnt = 0

    return r

def i_rand_a():
    """ Will generate a pseudo random
        integer and applies a mod operation
        with a sum. Could use any number for
        thoose operations.

        Returns:
            int: a periodic pseudo random integer
    """
    return i_random() % 95 + 32

def i_seed(seed, flag):
    """ Clears the global buffer mm and initialize the
        randrsl global buffer with the seed, and fills it
        with zeroes in case of the seed be smaller than
        ranrsl. Calls the rand_init method using the flag
        passed as argument.

        Args:
            seed (list): list of integers to garantee
            the minimal randomness for the algorithm.
            flag (boolean): if True, use the global
            buffer randrsl to initialize the global
            buffer mm.

        Returns: None. As it stores all
        the result on global variables,
        no return is necessary.
    """
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
    """ Vernam encryption algorithm. It clears
    the global buffer v, and for each caharacter
    in the message will generate a number and
    will apply a XOR operation with the character
    (using the byte value in ASCII coding system).

    Args:
        msg (str): the message that will be encrypted

    Returns:
        bytes: the global v buffer with the encrypted
        (or decrypted) message in bytes format. The
        method returns in byte format, as it works
        only with numbers and not with strings
    """
    global v

    l = len(msg)

    for i in range(0, len(v)):
        v[i] = 0

    for i in range(0, l):
        v[i] = (i_rand_a()) ^ msg[i]

    return bytes(v)

def caesar(m, ch, shift, modulo, start):
    """ Implements the caesar cyper, using any
    number for the modulo operation, instead of 5.
    If the M_DECIPHER flag is enabled, it reverses
    the shift the message to decrypt the message.

    Args:
        m (int): Is the cipher mode flag. Indicates with
        the method should encrypt or decrypt the message.
        ch (str): The character that will be encrypted
        shift (number): indcate how many bits should be
        shifted
        modulo (str): Number that will be the diviser in
        the modulo operation
        start (str): starting position for start encryption
    """
    if (m == CipherMode.M_DECIPHER):
        shift = -shift

    n = (ch-start) + shift
    n = n % modulo
    if n < 0:
        n += modulo
    return start + n

def caesar_str(m, msg, modulo, start):
    """ Clears the c buffer to garantee that previous
    encryption operation will mess with the encryption
    process. Will apply the cypher to each char in the
    string using the caesar algorithm.

    Args:
        m (int): Is the cipher mode flag. Indicates with
        the method should encrypt or decrypt the message.
        msg (str): The message that will be encrypted
        modulo (str): Number that will be the diviser in
        the modulo operation
        start (str): starting position for start encryption

    Returns:
        bytes: The return value is the global c
        buffer in bytes format, as we are working
        only with numbers.
    """
    global c

    l = len(msg)

    for i in range(0, len(c)):
        c[i] = 0

    for i in range(0, l):
        c[i] = caesar(m, msg[i], i_rand_a(), modulo, start)

    return bytes(c)

def main(msg, key):
    """ Method that runs the ISAAC Cipher algorithm
    Encode the message and the key as bytes to work only
    with numbers, and not strings. Encrypts the messgage using
    the Vernam algorithm and also encrypt the original message
    with caesar algoritm. Finally, decrypt the messages using
    the same algorithms to prove that the method does it works.
    The encrypted message, is printed during the process, to prove
    that method is encrypted. It will show just a real big number,
    even with you try to decode with ASCII encoding system.

    Args:
        msg (str): The message that will be encrypted
        key (str): A key to encrypt the message

    Returns:
        None: all the process is printed to the user
    """
    global v, c, MOD, START

    print('Message: {}'.format(msg))
    print('Key: {}'.format(key))

    print('--------------')

    LEN_MSG = len(msg)

    v = [0] * LEN_MSG
    c = [0] * LEN_MSG

    msg = msg.encode('ascii')
    key = key.encode('ascii')

    l = len(msg)

    i_seed(key, True)
    vctx = vernam(msg)
    cctx = caesar_str(CipherMode.M_ENCIPHER, msg, MOD, START)

    i_seed(key, True)
    vptx = vernam(vctx)
    cptx = caesar_str(CipherMode.M_DECIPHER, cctx, MOD, START)

    print('XOR: {}'.format(int.from_bytes(vctx, byteorder='big')))
    print('XOR dcr: {}'.format(vptx.decode('ascii')))

    print('--------------')

    print('MOD: {}'.format(int.from_bytes(cctx, byteorder='big')))
    print('MOD dcr: {}'.format(cptx.decode('ascii')))

if __name__ == '__main__':
    """
        Just for didatic reasons, the lorem package is used to generate
        big strings to mock up a real message and a real a key that would
        be used in a real case.
    """
    msg = os.environ.get('MSG')
    key = os.environ.get('KEY')
    # msg = 'La'
    # key = 'Sa'
    main(msg, key)
