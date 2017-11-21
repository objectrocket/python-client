import pytest
from objectrocket import util


@pytest.mark.parametrize("values,expected",
                         [((None, 1), 1),
                          ((1, None), 1),
                          ((1, 1), 2)])
def test_sum_values_integers(values, expected):
    assert util.sum_values(*values) == expected


def test_sum_values_fails_different_types():
    with pytest.raises(TypeError) as ex:
        util.sum_values(1, 'test')
    assert 'are not of the same type' in str(ex)


def test_sum_values_succeed_different_number_types():
    assert util.sum_values(1, 2.3) == 3


def test_sum_values_succeeds_list():
    assert util.sum_values([2, 3], [1, 2]) == [1, 2, 3]


def test_sum_values_succeeds_dict():
    assert util.sum_values({"one": 1}, {"two": 2}) == {'one': 1, 'two': 2}
