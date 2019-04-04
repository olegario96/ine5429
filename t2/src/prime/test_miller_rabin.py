from prime import miller_rabin
from prime import OutOfRange

import pytest

def test_miller_rabin_with_prime():
    assert miller_rabin(53, 2)

def test_miller_rabin_with_non_prime():
    assert miller_rabin(25, 3) == False

def test_exception_in_miller_rabin():
    with pytest.raises(OutOfRange):
        miller_rabin(23, 23)
