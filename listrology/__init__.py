from collections.abc import Sequence
from functools import reduce
import random

def _is_sequence(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))

_sentinel = object()

class List(list):
    def __class_getitem__(cls, args):
        """Alternative constructor
        List[1,2,3] == [1,2,3]
        L[4,5,6] == List[4,5,6] == List([4,5,6]) == [4,5,6]
        """
        if not isinstance(args, tuple):
            args = (args,)
        return cls(args)
    
    def __getitem__(self, arg):
        """Ensure List[2:4] also returns List
        """
        if isinstance(arg, slice):
            return type(self)(super().__getitem__(arg))
        return super().__getitem__(arg)
    
    def copy(self):
        """Copy and preserve type"""
        return type(self)(super().copy())
    
    def sort(self, key=None, reverse=False):
        """no in-place sorting, create copy for chaining"""
        new = self.copy()
        list.sort(new, key=key, reverse=reverse)
        return new
    
    def includes(self, index):
        return index < len(self)
    
    def length(self):
        # as a method
        return len(self)
    size = length
    
    def map(self, func):
        return type(self)(map(func, self))
    
    def map_until_error(self, func):
        new = type(self)()
        for item in self:
            try:
                new.append(func(item))
            except Exception: # does not catch keyboardinterrupt, systemexit etc
                break
        return new
    
    def map_drop_error(self, func):
        new = type(self)()
        for item in self:
            try:
                new.append(func(item))
            except Exception: # does not catch keyboardinterrupt, systemexit etc
                ...
        return new
    
    def filter(self, pred):
        return type(self)(filter(pred, self))
    select = filter
    
    def filter_until_error(self, pred):
        new = type(self)()
        for item in self:
            try:
                result = pred(item)
            except Exception:
                break
            if result:
                new.append(item)
        return new
    
    def filter_drop_error(self, pred):
        new = type(self)()
        for item in self:
            try:
                result = pred(item)
            except Exception:
                ...
            else:
                if result:
                    new.append(item)
        return new
    
    def reject(self, pred):
        return type(self)(filter(lambda *a, **k: not pred(*a, **k), self))

    def overwrite(self, target, start, end=None, strict=False):
        """
        overwrite items starting at [target] with items at self[start:end]
        if [end] is not supplied:
            overwrite item at [target] with item at self[start]
        
            if [strict] is set:
                raise error when there is not enough space to overwrite
        """
        new = self.copy()
        if not self.includes(target):
            raise IndexError("Index out of range (1st argument in overwrite())")
        if not self.includes(start):
            raise IndexError("Index out of range (2nd argument in overwrite())")

        if end is None:
            new[target] = self[start]
        else:
            if not self.includes(end):
                raise IndexError("Index out of range (3rd argument in overwrite())")
            if strict and not self.includes(target + end - start):
                raise IndexError("Not enough space to overwrite")
            new[target:target + end - start] = self[start:end]
        return new
    
    def all(self, pred):
        return all(pred(x) for x in self)
    
    def any(self, pred):
        return any(pred(x) for x in self)
    
    def as_slice(self):
        """Returns a slice that reprsents the list"""
        return slice(len(self))
    
    def zip(self, other):
        """Returns something like L[(x1, y1), (x2, y2), (x3, y3)]"""
        return type(self)(zip(self, other))
    
    def first(self, pred, return_index=False):
        """first item that satisfies predicate"""
        for i, item in enumerate(self):
            if pred(item):
                if return_index:
                    return i
                return item
    
    def flatten1(self):
        """flatten by one level"""
        new = type(self)()
        for item in self:
            if _is_sequence(item):
                new.extend(item)
            else:
                new.append(item)
        return new
    
    def flatten(self, depth=1):
        if not isinstance(depth, int):
            raise TypeError("depth must be int")
        if depth < 1:
            raise ValueError("depth must be greater than 0")
        new = self.copy()
        for _ in range(depth):
            if new.any(_is_sequence):
                new = new.flatten1()
            else: # optimization, checks if there are sequences left
                break
        return new
    
    def foreach(self, func):
        """calls func for each item"""
        for item in self:
            func(item)
    
    def reversed(self):
        """for method chaining"""
        return self[::-1]

    def reduce(self, func, initial_value=_sentinel):
        if initial_value is _sentinel:
            return reduce(func, self)
        return reduce(func, self, initial_value)
    
    def rreduce(self, func, initial_value=_sentinel):
        """reduce() but from the right"""
        if initial_value is _sentinel:
            return reduce(func, reversed(self))
        return reduce(func, reversed(self), initial_value)
    
    def enumerations(self):
        """Returns something like L[(0, item0), (1, item1), (2, item2)]"""
        return type(self)(enumerate(self))
    
    def fill(self, value, start, end=None):
        if not self.includes(start):
            raise IndexError("start out of range")
        if end is None:
            end = len(self)
        elif not self.includes(end):
            raise IndexError("end out of range")
        new = self.copy()
        for i in range(start, end):
            new[i] = value
        return new
    
    def indices(self):
        """Returns a list of indices"""
        return type(self)(range(len(self)))
    
    def indices_range(self):
        """Returns a range representing the indices"""
        return range(len(self))
    
    def rotate(self, count=1):
        """For each rotation, the first element is moved to the last"""
        count = count % len(self)
        new = self.copy()
        if count == 0:
            return new
        new.extend(new[:count])
        new = new[count:]
        return new
    
    def shuffle(self):
        """creates copy unlike random.shuffle"""
        new = self.copy()
        random.shuffle(new)
        return new
    
    def split_at(self, index):
        if not self.includes(index):
            raise IndexError("index out of range")
        return self[:index], self[index:]
    
    def unique(self):
        return type(self)(set(self))
    
    def mismatch(self, other, return_index=False):
        """get mismatch pairs (lazy evaluation)"""
        if not return_index:
            return filter(lambda x: x[0] != x[1], self.zip(other))
            # regular map() and filter() is used for lazy evaluation
        return map(lambda x: x[0], filter(lambda x: x[1][0] != x[1][1], self.zip(other).enumerations()))
    
    def mismatches(self, other, return_index=False):
        """Get mismatch pairs but as a List object (not lazy evaluation)"""
        return type(self)(self.mismatch(other, return_index=return_index))
    
    def first_mismatch(self, other, return_index=False):
        return next(iter(self.mismatch(other, return_index)))
    
    def chunks(self, n, drop_extra=False, strict=False):
        if strict and len(self) % n != 0:
            raise ValueError("length of List is not divisible by n (strict=True)")
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 1:
            raise ValueError("n must be a positive integer")
        new = [self[i:i+n] for i in range(0, len(self), n)]
        if drop_extra and len(new[-1]) != n:
            new.pop(-1)
        return new

L = List # shorthand constructor

if __name__ == "__main__":
    # the demo in docs
    volcano_heights = L([412, 399, 276, 591, 482, 451, 521, 529, 521, 426, 511, 426, 426])
    print("These are some volcano heights:", volcano_heights)
    # find all volcano heights that are 400m-525m tall and remove duplicates
    result = volcano_heights.filter(lambda x: 400 <= x <= 525).unique().sort()
    print("volcano_heights.filter(lambda x: 400 <= x <= 525).unique().sort():", result)
