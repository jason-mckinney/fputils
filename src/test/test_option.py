from python_fp.option import Some, Empty
import pytest


def test_some():
    some_value = Some(42)
    assert some_value.is_defined(), "Expected Some to be defined."
    assert some_value.get() == 42, "Expected Some value to be 42."
    assert not some_value.is_empty(), "Expected Some to not be empty."


def test_empty():
    value = Empty()

    assert not value.is_defined(), "Expected Empty to not be defined."
    assert value.is_empty(), "Expected Empty to be empty."

    with pytest.raises(ValueError):
        value.get()

def test_contains():
    assert Some(42).contains(42), "Expected Some to contain 42."
    assert not Some(42).contains(43), "Expected Some to not contain 43."
    assert not Empty().contains(42), "Expected Empty to not contain 42."
    assert not Empty().contains(None), "Even though Empty represents None, this should be False."

def test_exists():
    assert Some(42).exists(lambda x: x > 0), "Expected Some to exist with a positive value."
    assert not Some(42).exists(lambda x: x < 0), "Expected Some to not exist with a negative value."
    assert not Empty().exists(lambda x: x > 0), "Expected Empty to not exist with any predicate."
    assert not Empty().exists(lambda x: x < 0), "Expected Empty to not exist with any predicate."

def test_filter():
    assert Some(42).filter(lambda x: x > 0).is_defined(), "Expected Some to be defined after filtering with a positive predicate."
    assert Some(42).filter(lambda x: x < 0).is_empty(), "Expected Some to be empty after filtering with a negative predicate."
    assert Empty().filter(lambda x: x > 0).is_empty(), "Expected Empty to remain empty after filtering."
    assert Empty().filter(lambda x: x < 0).is_empty(), "Expected Empty to remain empty after filtering."
    
    assert Some(42).filter_not(lambda x: x > 0).is_empty(), "Expected Some to be empty after filtering with a negative predicate."
    assert Some(42).filter_not(lambda x: x < 0).is_defined(), "Expected Some to be defined after filtering with a positive predicate."
    assert Empty().filter_not(lambda x: x > 0).is_empty(), "Expected Empty to remain empty after filtering."
    assert Empty().filter_not(lambda x: x < 0).is_empty(), "Expected Empty to remain empty after filtering."


