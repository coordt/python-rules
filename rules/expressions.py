"""Main module."""
import operator
from abc import ABC, abstractmethod


class OperatorError(Exception):
    pass


class ExpressionObject(ABC):

    @abstractmethod
    def __str__(self) -> str:
        """
        A string representation of the expression

        Returns:
            str
        """
        return ""

    @abstractmethod
    def __call__(self, ctx):
        """
        Perform the operations based on the context and other arguments

        Args:
            ctx: The expression context

        Returns:
            Any
        """
        pass


class Constant(ExpressionObject):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __call__(self, ctx):
        return self.value


class ContextReference(ExpressionObject):
    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def __str__(self):
        return self.name

    def resolve_name(self, ctx):
        """
        Get a key or attr ``name`` from obj or None

        Copied and modified from Django Template variable resolutions

        Args:
            ctx:

        Returns:
            Any or None
        """
        lookups = self.name.split(".")
        current = ctx
        try:  # catch-all for unexpected failures
            for bit in lookups:
                try:  # dictionary lookup
                    current = current[bit]
                    # ValueError/IndexError are for numpy.array lookup on
                    # numpy < 1.9 and 1.9+ respectively
                except (TypeError, AttributeError, KeyError, ValueError, IndexError):
                    try:  # attribute lookup
                        current = getattr(current, bit)
                    except (TypeError, AttributeError):
                        # Reraise if the exception was raised by a @property
                        if bit in dir(current):
                            raise
                        try:  # list-index lookup
                            current = current[int(bit)]
                        except (
                            IndexError,  # list index out of range
                            ValueError,  # invalid literal for int()
                            KeyError,  # current is a dict without `int(bit)` key
                            TypeError,
                        ):  # unsubscriptable object
                            return self.default
            return current
        except Exception:  # NOQA
            return self.default

    def __call__(self, ctx):
        return self.resolve_name(ctx)


class Operator(ExpressionObject):
    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
        '^': operator.pow,
        #
        '%': operator.mod,
        #
        '&': operator.and_,
        '|': operator.or_,
        #
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        #
        'in': operator.contains,
    }

    def __init__(self, opr, left_side, right_side):
        self.left_side = left_side
        self.right_side = right_side
        self.opr = opr
        if opr not in self.operator_map.keys():
            op_list = ", ".join(self.operator_map.keys())
            raise OperatorError(f'"{opr}" is not a valid operator. Must be')

    def __str__(self):
        return f"{self.left_side} {self.opr} {self.right_side}"

    def __call__(self, ctx):
        return self.operator_map[self.opr](self.left_side(ctx), self.right_side(ctx))
