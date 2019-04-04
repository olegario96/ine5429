from prime import fermat

import pytest

def test_fermat_with_prime():
    assert fermat(47)

def test_fermat_with_non_prime():
    assert fermat(25) == False
