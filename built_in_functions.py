"""This Module is re-implementation of python existing built_in
functions on the basis of their execution output, It's written to
imitate those functions, not intended to be used in the programs.

"""

# List of all built_in functions written within this module
# Functions name have been capitalized to prevent conflict.
__all__ = ["Any", "All", "Chr", "Ord", "Bin",
           "Divmod", "Len", "Min", "Max", "Sum", "Sorted",
           "Map", "Zip", "Filter", "Enumerate", "Reversed"]


"""A collection of dict constants.

Public module variables:

whitespace -- a dict containing all ascii whitespace
ascii_lowercase -- a dict containing all ascii lowercase letters
ascii_uppercase -- a dict containing all ascii uppercase letters
ascii_letters -- a dict containing all ascii letters
digits -- a dict containing all ascii decimal digits
punctuation -- a dict containing all ascii punctuation characters

"""

whitespace = {32: ' ', 9: '\t', 10: '\n', 13: '\r', 11: '\x0b', 12: '\x0c'}

ascii_lowercase = {97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g',
                   104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n',
                   111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
                   118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}

ascii_uppercase = {65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G',
                   72: 'H', 73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N',
                   79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U',
                   86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z'}

punctuation = {33: '!', 34: '"', 35: '#', 36: '$', 37: '%', 38: '&', 39: "'", 40: '(', 41: ')',
               42: '*', 43: '+', 44: ',', 45: '-', 46: '.', 47: '/', 58: ':', 59: ';', 60: '<',
               61: '=', 62: '>', 63: '?', 64: '@', 91: '[', 92: '\\', 93: ']', 94: '^', 95: '_',
               96: '`', 123: '{', 124: '|', 125: '}', 126: '~'}

digits = {48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9'}

# These are some ascii characters of python representing themselves in dict{key: value} pairs.
all_ascii_characters = ascii_lowercase | ascii_uppercase | whitespace | digits | punctuation

# for checking missing arguments
MISSING = object()

def is_iter(value, /) -> bool:
    "Return True if iterable else False"

    try:
        iter(value)
        return True
    except TypeError:
        return False


def getkey(dct: dict, value: str) -> int:
    "Return key for the value."

    for key, item in dct.items():
        if value == item:
            return key
    raise KeyError(f"key not found for '{value}'")


def errorhandler(message: str, *args: list) -> None:
    "Raise Type error based on arguments passed to it."

    for value, datatype in args:
        if not isinstance(value, datatype):
            raise TypeError(f"{message}" % type(value).__name__)


def Chr(i: int, /) -> str:
    "Return a Unicode string of one character"

    errorhandler("'%s' object cannot be interpreted as an integer", [i, int])

    return all_ascii_characters[i]


def Ord(c: str, /) -> int:
    "Return the Unicode code point for a one-character string."

    errorhandler("Ord() expected string of length 1, but %s found", [c, str])
    if len(c) > 1:
        raise TypeError(
            f"Ord() expected a character, but string of length {len(c)} found")

    return getkey(all_ascii_characters, c)


def Any(iterable, /) -> bool:
    """Return True if any element of the iterable is true.
    If the iterable is empty, returns False."""

    if not is_iter(iterable):
        raise TypeError(
            f"{type(iterable).__name__!r} object is not iterable")

    for item in iterable:
        if item:
            return True
    return False


def All(iterable, /) -> bool:
    """Return True if Bool(x) is True for all values x in the iterable.

    If the iterable is empty, returns True."""

    if not is_iter(iterable):
        raise TypeError(
            f"{type(iterable).__name__!r} object is not iterable")

    for item in iterable:
        try:
            for _ in item:
                continue
        except TypeError:
            pass
        if not item:
            return False
    return True


def Bin(number: int, /) -> str:
    """Return the binary representation of an integer.

    >>> bin(2796202)
    '0b1010101010101010101010'

    """

    errorhandler("'%s' object cannot be interpreted as an integer", [number, int])

    if number == 0:
        return "0b0"
    num = abs(number)

    binary = ''
    while num != 0:
        num, remainder = divmod(num, 2)
        binary += f"{remainder}"

    if number > -1:
        return f"0b{binary[::-1]}"
    else:
        return f"-0b{binary[::-1]}"


def Divmod(x, y, /) -> tuple:
    "Return the tuple (x//y, x%y).  Invariant: div*y + mod == x."

    return (x // y, x % y)


def Len(obj, /) -> int:
    "Return the number of items in a container."

    if hasattr(obj, '__len__'):
        return obj.__len__()

    raise TypeError(
        f"object of type {type(obj).__name__!r} has no Len()")


def Min(*args, default=MISSING, key=None):
    """With a single iterable argument, return its smallest item. The
    default keyword-only argument specifies an object to return if
    the provided iterable is empty.
    With two or more arguments, return the smallest argument."""

    if not args:
        raise TypeError("Min expected at least 1 argument, got 0")

    if len(args) == 1:
        val = args[0]
        if not is_iter(val):
            raise TypeError(
                f"{type(val).__name__!r} object is not iterable")

        if not val:  # checking for empty sequence
            if default is not MISSING:
                return default
            raise ValueError("Min() arg is an empty sequence")

        it = iter(val)
    else:
        it = iter(args)

    if key is None:
        def key(x): return x

    small = next(it)
    small_key = key(small)

    for item in it:
        i = key(item)
        if i < small_key:
            small = item
            small_key = i
    return small


def Max(*args, default=MISSING, key=None):
    """With a single iterable argument, return its biggest item. The
    default keyword-only argument specifies an object to return if
    the provided iterable is empty.
    With two or more arguments, return the largest argument."""

    if not args:
        raise TypeError("Max expected at least 1 argument, got 0")

    if len(args) == 1:
        val = args[0]
        if not is_iter(val):
            raise TypeError(
                f"{type(val).__name__!r} object is not iterable")

        if not val:  # checking for empty sequence
            if default is not MISSING:
                return default
            raise ValueError("Max() arg is an empty sequence")

        it = iter(val)
    else:
        it = iter(args)

    if key is None:
        def key(x): return x

    big = next(it)
    big_key = key(big)

    for item in it:
        i = key(item)
        if i > big_key:
            big = item
            big_key = i
    return big


def Sum(iterable, /, start=0):
    """Return the sum of a 'start' value (default: 0) plus an iterable of numbers
    When the iterable is empty, return the start value.
    This function is intended specifically for use with numeric values and may
    reject non-numeric types."""

    if not is_iter(iterable):
        raise TypeError(
            f"{type(iterable).__name__!r} object is not iterable")
    if isinstance(start, str):
        raise TypeError(
            "Sum() can't sum strings [use ''.join(seq) instead]")

    output = 0
    for item in iterable:
        output += item
    return output + start


def binary_search(array, item, start, end):
    if start == end:
        if array[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start

    mid = round((start + end) / 2)

    if array[mid] < item:
        return binary_search(array, item, mid + 1, end)
    elif array[mid] > item:
        return binary_search(array, item, start, mid - 1)
    else:
        return mid

#* Insertion sort is used by timsort for small array or small runs.
def insertion_sort(array):
    for index in range(1, len(array)):
        value = array[index]
        pos = binary_search(array, value, 0, index - 1)
        array = array[:pos] + [value] + array[pos:index] + array[index+1:]
    return array

#* Returns a single sorted array from two sorted array
def merge(left, right):
    if not left:
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + merge(left[1:], right)
    return [right[0]] + merge(left, right[1:])

#* Note: This is pythonic implementation of timsort algorithm
def timsort(array):
    length = len(array)
    if length > 1000:
        from sys import setrecursionlimit
        setrecursionlimit(length)

    runs, sorted_runs = [], []
    new_run = [array[0]]
    for i in range(1, length):
        # if i is at the last index
        if i == length-1:
            new_run.append(array[i])
            runs.append(new_run)
            break
        if array[i] < array[i-1]:
            # if new_run is None (empty)
            if not new_run:
                runs.append([array[i]])
                new_run.append(array[i])
            else:
                runs.append(new_run)
                new_run = [array[i]]
        else:
            new_run.append(array[i])
    # for every item in runs, append it using insertion sort
    for item in runs:
        sorted_runs.append(insertion_sort(item))
    # for every run in sorted_runs, merge them
    sorted_array = []
    for run in sorted_runs:
        sorted_array = merge(sorted_array, run)
    return sorted_array


def Sorted(iterable, /, *, key=None, reverse=False):
    """Return a new list containing all items from the iterable in ascending order.

    A custom key function can be supplied to customize the sort order, and the
    reverse flag can be set to request the result in descending order.

    """

    array = iterable.copy() if isinstance(
        iterable, list) else list(iterable)

    if key is None:
        sorted_array = timsort(array)
    else:
        if reverse: array.reverse()
        # sorting array elements using key
        key_sorted = timsort([key(k) for k in array])
        # sorting array using sorted key elements
        sorted_array = []
        for k_item in key_sorted:
            for item in array:
                if k_item == key(item):
                    sorted_array.append(item)
                    array.remove(item)
    if reverse:
        sorted_array.reverse()
    return sorted_array


class Enumerate:
    """Return an Enumerate object.

    iterable
        an object supporting iteration

    The enumerate function yields pairs containing a count (from start, which
    defaults to zero) and a value yielded by the iterable argument.

    enumerate is useful for obtaining an indexed list:
        (0, seq[0]), (1, seq[1]), (2, seq[2]), ..."""

    def __init__(self, /, iterable, start=0):
        if not isinstance(start, int):
            raise TypeError(
                f"{type(start).__name__!r} object cannot be interpreted as an integer")

        self.__index = -1 + start
        self.__iters = iter(iterable)

    def __iter__(self, /):
        return self

    def __next__(self, /):
        self.__index += 1
        return (self.__index, next(self.__iters))

    def __repr__(self, /):
        return "<%s object at %s>" % (self.__class__.__name__,
            str(hex(id(self))).replace('x', 'x00000').upper())

    def __getstate__(self, /):
        "Return state information for pickling."

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        return self.__dict__.copy()

    def __setstate__(self, state, /):
        "Set state information for unpickling."

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)


class Reversed:
    "Return a reverse iterator over the values of the given sequence."

    def __init__(self, sequence, /):
        if hasattr(sequence, 'keys'):
            self.__data = sequence.keys()
        elif hasattr(sequence, '__getitem__'):
            self.__data = sequence
        else:
            raise TypeError(
                f"{type(sequence).__name__!r} object is not reversible")
        self.__index = len(sequence)

    def __iter__(self, /):
        return self

    def __next__(self, /):
        if self.__index == 0:
            raise StopIteration
        self.__index -= 1
        return self.__data[self.__index]

    def __repr__(self, /):
        return "<%s_reverseiterator object at %s>" % (
            type(self.__data).__name__, str(hex(id(self))).replace('x', 'x00000').upper())

    def __length_hint__(self, /):
        "Private method returning an estimate of len(list(it))."

        return len(self.__data)

    def __getstate__(self, /):
        "Return state information for pickling."

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        return self.__dict__.copy()

    def __setstate__(self, state, /):
        "Set state information for unpickling."

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)


class Map:
    """make an iterator that computes the function using arguments from

    each of the iterables. stops when the shortest iterable is exhausted."""

    def __init__(self, /, func, *args):
        if not args:
            raise TypeError(
                f"{self.__class__.__name__}() must have at least two arguments.")

        self.__func = func
        self.__iters = [iter(i) for i in args]

    def __iter__(self, /):
        return self

    def __next__(self, /):
        args = [next(i) for i in self.__iters]
        return self.__func(*args)

    def __repr__(self, /):
        return "<%s object at %s>" % (self.__class__.__name__,
            str(hex(id(self))).replace('x', 'x00000').upper())

    def __getstate__(self, /):
        "Return state information for pickling."

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        return self.__dict__.copy()

    def __setstate__(self, state, /):
        "Set state information for unpickling."

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)


class Zip:
    """Zip(*iterables, strict=False) --> Yield tuples until an input is exhausted.

      >>> list(zip('abcdefg', range(3), range(4)))
      [('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]

    The zip object yields n-length tuples, where n is the number of iterables
    passed as positional arguments to zip().  The i-th element in every tuple
    comes from the i-th iterable argument to zip().  This continues until the
    shortest argument is exhausted.

    If strict is true and one of the arguments is exhausted before the others,
    raise a ValueError."""

    def __init__(self, /, *args, strict=False):
        self.__strict = strict
        self.__pargs = args
        self.__iters = [iter(i) for i in args]

    def __iter__(self, /):
        self.__check_eq()
        return self

    def __next__(self, /):
        if not self.__iters:
            raise StopIteration

        sequence = ()
        for item in self.__iters:
            sequence += (next(item),)
        return sequence

    def __repr__(self, /):
        return "<%s object at %s>" % (self.__class__.__name__,
            str(hex(id(self))).replace('x', 'x00000').upper())

    def __getstate__(self, /):
        "Return state information for pickling."

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        return self.__dict__.copy()

    def __setstate__(self, state, /):
        "Set state information for unpickling."

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)

    def __check_eq(self, /):
        if self.__strict and self.__pargs:
            initial = len(self.__pargs[0])
            name = self.__class__.__name__
            for pos, value in enumerate(map(len, self.__pargs), start=1):
                if value > initial:
                    raise ValueError(
                        f"{name}() argument {pos} is longer than argument 1{1-pos if pos != 2 else ''}")
                if value < initial:
                    raise ValueError(
                        f"{name}() argument {pos} is shorter than arguments 1{1-pos if pos != 2 else ''}")


class Filter:
    """Filter(function or None, iterable) --> Filter object

   Return an iterator yielding those items of iterable for which function(item)
   is true. If function is None, return the items that are true."""

    def __init__(self, /, function, iterable):
        if function is None:
            def function(x): return x

        self.__iters = iter([i for i in iterable if function(i)])

    def __iter__(self, /):
        return self

    def __next__(self, /):
        return next(self.__iters)

    def __repr__(self, /):
        return "<%s object at %s>" % (self.__class__.__name__,
            str(hex(id(self))).replace('x', 'x00000').upper())

    def __getstate__(self, /):
        "Return state information for pickling."

        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        return self.__dict__.copy()

    def __setstate__(self, state, /):
        "Set state information for unpickling."

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)


__all__.extend(["Reduce"])
#* Note: `reduce` is functools library function not a python built-in function.
def Reduce(function, sequence, initial=MISSING):
    """
    Reduce(function, iterable[, initial]) -> value

    Apply a function of two arguments cumulatively to the items of a sequence
    or iterable, from left to right, so as to reduce the iterable to a single
    value.  For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
    ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
    of the iterable in the calculation, and serves as a default when the
    iterable is empty.
    """

    it = iter(sequence)
    if initial is MISSING:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError(
                "reduce() of empty iterable with no initial value") from None
    else:
        value = initial

    for element in it:
        value = function(value, element)

    return value


__all__.extend(["IS"])
# Note: python 'in' is an operator not a function and 'IS' isn't any python
# function rather this is 'in' implementation of python operator as function.
def IS(value, iterable, /) -> bool:
    "Perform same operation as 'in' operator"

    if isinstance(iterable, str):
        if not isinstance(value, str):
            raise TypeError(
                f"'IS <string>' requires string as left operand, not '{type(value).__name__}'")

        length = len(value)
        for i in range(len(iterable)):
            if value == iterable[i: i+length]:
                return True
        return False

    if not is_iter(iterable):
        raise TypeError(
            f"argument of type '{type(iterable).__name__}' is not iterable")

    for item in iterable:
        if value == item:
            return True
    return False


# --------------------------------------------------------------------#
#   HELPER FUNCTION DECORATOR FOR [tupleobject, listobject, etc...]   #
# --------------------------------------------------------------------#

def verifier(func, /):
    "Raise error for invalid instances."

    def wrapper(self, value, /):
        errorcode = 0
        match func.__name__:
            case '__eq__':
                symbol = '=='

            case '__ne__':
                symbol = '!='

            case '__lt__':
                symbol = '<'

            case '__le__':
                symbol = '<='

            case '__gt__':
                symbol = '>'

            case '__ge__':
                symbol = '>='

            case '__sub__':
                symbol = '-'

            case '__xor__' | '__rxor__':
                symbol = '^'

            case '__ixor__':
                symbol = '^='

            case '__and__' | '__rand__':
                symbol = '&'

            case '__iand__':
                symbol = '&='

            case '__or__' | '__ror__':
                symbol = '|'

            case '__ior__':
                symbol = '|='

            case '__add__' | '__radd__' | '__iadd__':
                errorcode = 1

            case '__mul__' | '__rmul__' | '__imul__':
                errorcode = 2

            case default:
                raise ValueError(
                    f"Invalid function: {default} for verifier")

        if errorcode == 0:
            if not isinstance(value, self.__class__):
                raise TypeError(
                    "unsupported operand type(s) for %s: '%s' and '%s'" % (
                        symbol, self.__class__.__name__, type(value).__name__))

        elif errorcode == 1:
            if not isinstance(value, self.__class__):
                name = self.__class__.__name__
                raise TypeError(
                    f'can only concatenate {name} (not "{type(value).__name__}") to {name}')
        else:
            if not isinstance(value, int):
                raise TypeError(
                    f"can't multiply sequence by non-int of type '{type(value).__name__}'")

        return func(self, value)
    return wrapper