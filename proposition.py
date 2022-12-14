from typing import Any, TypeVar, Generic
from collections.abc import Callable
from abc import ABCMeta, abstractmethod


class Proposition:
    pass


# ∀ S T U
S = TypeVar('S', bound=Proposition)
T = TypeVar('T', bound=Proposition)
U = TypeVar('U', bound=Proposition)


# S ∨ T
class Or(Proposition, Generic[S, T], metaclass=ABCMeta):
    @abstractmethod
    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        ...
    
    @classmethod
    def intro_left(cls, left: S):
        return Left(left)
    
    @classmethod
    def intro_right(cls, right: T):
        return Right(right)


# Construct S ∨ T from S
class Left(Or[S, T]):
    def __init__(self, left: S):
        self.left = left

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return left_case(self.left)


# Construct S ∨ T from T
class Right(Or[S, T]):
    def __init__(self, right: T):
        self.right = right

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return right_case(self.right)


# S ∧ T
class And(Proposition, Generic[S, T]):
    def __init__(self, left: S, right: T):
        self.left = left
        self.right = right


# S → T
class Implies(Proposition, Generic[S, T]):
    def __init__(self, mapping: Callable[[S], T]):
        self.apply = mapping


# S ↔︎ T
class Iff(Proposition, Generic[S, T]):
    def __init__(self, forward: Implies[S, T], backward: Implies[T, S]):
        self.forward = forward
        self.backward = backward


# ⊥
class Bottom(Proposition, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        ...

    def eliminate(self) -> Any:
        return


# ¬S
class Not(Implies[S, Bottom]):
    pass
