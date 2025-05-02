from __future__ import annotations

from collections.abc import Callable
from typing import Any

"""Provides the IO class for encapsulating effectful computations in a functional style.

The IO class allows deferring side effects until the computation is executed,
enabling composition using map and flatmap.
"""


class IO[T]:
    """Generic IO monad-like wrapper to represent deferred computations.

    T: The result type of the computation.
    """

    def __init__(self, effect: Callable[[], T], *args, **kwargs) -> None:
        """Constructor

        Parameters:
            effect: A callable returning the computation result, or a raw value.
            *args: Positional arguments for the effect callable.
            **kwargs: Keyword arguments for the effect callable.
        """
        self.args = args
        self.kwargs = kwargs

        if callable(effect):
            self._collect: Callable[[], T] = effect
        else:

            def collect():
                return effect

            self._collect = collect

    def __call__(self, *args, **kwargs) -> IO[T]:
        """Implementation of Callable - this is designed to allow the IO class to be used as a function decorator such that any decorated function is automatically wrapped in an IO.

        Parameters:
            *args: New positional arguments to pass to the effect.
            **kwargs: New keyword arguments to pass to the effect.

        Returns:
            An IO instance wrapping the decorated function.
        """
        self.args = args
        self.kwargs = kwargs
        return self

    def collect(self) -> T:
        """Collect and excute the chain of deferred computations and return the result of the final computation in the chain"""
        return self._collect(*self.args, **self.kwargs)

    def map(self, effect: Callable[[T], Any]) -> IO[Any]:
        """Apply a deferred function to execute after this effect in the deferred chain.

        Parameters:
            effect: A function that transforms the result T to a new value.

        Returns:
            A new IO instance wrapping the composed computations.
        """

        def collect():
            return effect(self.collect())

        return IO(collect)

    def flatmap(self, effect: Callable[[T], IO[Any]]) -> IO[Any]:
        """Bind the result of this IO to another IO-returning function, flattening the monadic structure.

        Parameters:
            effect: A function that takes the result T and returns an IO of some type.

        Returns:
            An IO instance returned by the effect.
        """
        return effect(self.collect())

    def pure(self, value: T) -> IO[T]:
        """Lift an already evaluated value into IO.
        Parameters:
            value: The value to wrap.
        Returns:
            An IO instance wrapping the value.
        """
        return IO(value)
