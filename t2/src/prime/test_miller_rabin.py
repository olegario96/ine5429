from prime import miller_rabin

import pytest

def test_miller_rabin():
    assert miller_rabin(53, 2)
