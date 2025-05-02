from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, Iterator
from Either import Either, Left, Right


class Option[A](metaclass=ABCMeta):
    def _get_value(self) -> A:
        return self.__value

    def _set_value(self, value: A):
        self.__value = value

    def _del_value(self) -> None:
        del self.__value

    _value = property(_get_value, _set_value, _del_value)

    @abstractmethod
    def get(self) -> A:
        """
        Returns:
            The option's value.

        raises:
            ValueError: If the option is Empty.
        """
        return NotImplemented

    @abstractmethod
    def is_defined(self) -> bool:
        """
        Returns:
            True if this is Some, False otherwise.
        """
        return NotImplemented

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Returns:
            True if this is Empty, False otherwise.
        """
        return NotImplemented

    def contains(self, value: A) -> bool:
        """
        Returns:
            True if this is Some and its value is equal to the given value, False otherwise.
        """
        return self._value == value if self.is_defined() else False

    def exists(self, predicate: Callable[[A], bool]) -> bool:
        """
        Returns:
            False if this is Empty or returns the result of the given predicate against the Some value.
        """
        return False if self.is_empty() else predicate(self._value)

    def filter(self, predicate: Callable[[A], bool]) -> Option[A]:
        """
        Returns:
            this Option if this is Some and the given predicate does hold for the Some value,
            otherwise Empty
        """
        return self if self.is_defined() and predicate(self._value) else Empty()

    def filter_not(self, predicate: Callable[[A], bool]) -> Option[A]:
        """
        Returns:
            this Option if this is Some and the given predicate does not hold for the Some value,
            otherwise Empty
        """
        return self if self.is_defined() and not predicate(self._value) else Empty()

    def flatmap[B](self, f: Callable[[A], Option[B]]) -> Option[B]:
        """
        Returns:
            the result of applying f to this Option's value if this Option is non-empty,
            otherwise Empty.
        """
        return Empty() if self.is_empty() else f(self._value)

    def map[B](self, f: Callable[[A], B]) -> Option[B]:
        """
        Returns:
            the result of applying f to this Option's value if this Option is non-empty,
            otherwise Empty.
        """
        return Empty() if self.is_empty() else Some(f(self._value))

    def flatten[B](self) -> Option[B]:
        """
        Returns:
            the nested Option's value if this is a Some,
            otherwise Empty.

        raises: AssertionError: If this is a Some and the nested value is not an Option.
        """
        assert isinstance(self._value, Option)
        return Empty() if self.is_empty() else self._value

    def fold[B](self, f: Callable[[A], B], if_empty: B) -> B:
        """
        Returns:
            if_empty if this is Empty,
            f(self._value) if this is Some.
        """
        return if_empty if self.is_empty() else f(self._value)

    def forall(self, predicate: Callable[[A], bool]) -> bool:
        """
        Returns:
            True if this is Empty,
            True if this is Some and the given predicate holds for the Some value,
            False otherwise.
        """
        return True if self.is_empty() else predicate(self._value)

    def foreach(self, f: Callable[[A], None]) -> None:
        """
        Applies the given function to this Option's value if this Option is non-empty.
        """
        if self.is_defined():
            f(self._value)

    def get_or_else(self, other: A) -> A:
        """
        Returns:
            this Option's value if this is Some,
            other otherwise.
        """
        return self._value if self.is_defined() else other

    def iterator(self) -> Iterator[A]:
        """
        Returns:
            An iterator over this Option's value if this is Some,
            otherwise an empty iterator.
        """
        return iter([self._value]) if self.is_defined() else iter([])

    def or_else(self, other: Option[A]) -> Option[A]:
        """
        Returns:
            this Option if this is Some,
            other otherwise.
        """
        return self if self.is_defined() else other

    def or_none(self) -> A | None:
        """
        Returns:
            this Option's value if this is Some,
            None otherwise.
        """
        return self._value if self.is_defined() else None

    def to_left[B](self, right: B) -> Either[A, B]:
        """
        Returns:
            this Option's value as a Left if this is Some,
            otherwise a Right with the given value.
        """
        return Left(self._value) if self.is_defined() else Right(right)

    def to_right[B](self, left: A) -> Either[A, B]:
        """
        Returns:
            this Option's value as a Right if this is Some,
            otherwise a Left with the given value.
        """
        return Right(self._value) if self.is_defined() else Left(left)

    def unzip[B](self) -> tuple[Option[A], Option[B]]:
        """
        Returns:
            A pair of Options, containing non-empty values if this option is a pair and empty Options otherwise
        """
        return (
            (Some(self._value[0]), Some(self._value[1]))
            if self.is_defined() and isinstance(self._value, tuple)
            else (Empty(), Empty())
        )

    def zip[B](self, other: Option[B]) -> Option[tuple[A, B]]:
        """
        Returns:
            A new option containing a tuple of the values of this option and the given option if both are non-empty,
            otherwise Empty.
        """
        return (
            Some((self._value, other.value))
            if self.is_defined() and other.is_defined()
            else Empty()
        )


class Some[A](Option[A]):
    def __init__(self, value: A):
        self._value = value

    def get(self) -> A:
        return self._value

    def is_defined(self) -> bool:
        return True

    def is_empty(self) -> bool:
        return False


class Empty(Option):
    def get(self) -> None:
        raise ValueError("Empty Option")

    def is_defined(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return True
