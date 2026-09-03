"""
DS General Utils Exceptions
"""

# Define a custom warning class


class PriorTasksFailedError(Exception):
    """Exception raised when a prior task has failed, indicating that the process cannot proceed."""


class DeprecatedFunctionWarning(DeprecationWarning):
    """Raised when a user uses a function which is depreciated"""


class InvalidArgumentCombination(Exception):
    """Raised when invalid combinations of arguments are passed into a function"""


class InvalidArgument(Exception):
    """Raised when invalid arguments are passed into a function"""
