from listrology import L
import funcy
a = L[12, 2]
assert a == [12, 2]

assert type(a[0:1]) is L

def error_if_even(num):
    if num % 2 == 0:
        raise Exception
    return num

def add_one(num):
    return num + 1

# L[...] can also be used, but this is more type friendly
b = L([1,3,5,7,6,5,999])

assert b.map_until_error(error_if_even) == [1,3,5,7]
assert b.map_until_error(error_if_even).map(add_one) == [2,4,6,8]
assert b.map_until_error(error_if_even).map(add_one).zip([1,1,1,1]) == [(2, 1),(4, 1),(6, 1),(8, 1)]
assert b.map_until_error(error_if_even).map(add_one).zip([1,1,1,1]).flatten() == [2, 1, 4, 1, 6, 1, 8, 1]
assert b.map_until_error(error_if_even).map(add_one).zip([1,1,1,1]).map(lambda x: x[0] + x[1]) == [3, 5, 7, 9]

c = L([10,11,12,13,14,15,16,17,18,19])
assert c.overwrite(2, 4, 6) == [10,11,14,15,14,15,16,17,18,19]
assert c.overwrite(2, 4, 9) == [10,11,14,15,16,17,18,17,18,19]

def is_even(num):
    return num % 2 == 0

d = L([2,4,6,8,10])
assert d.all(is_even)
assert b.any(is_even)
assert not b.all(is_even)

assert b[b.as_slice()] == b

def add(a, b):
    return a + b

assert d.reduce(add) == 30

e = L([1,2,3])
e.reverse()
assert e == [3, 2, 1]
f = L([1,2,3])
assert f.reversed() == [3, 2, 1]
assert f == [1, 2, 3]

g = L([10, 11, 12, 13])
assert g.enumerations() == [(0, 10), (1, 11), (2, 12), (3, 13)]
assert g.fill("hello", 1, 3) == [10, "hello", "hello", 13]
assert g.fill("hello", 1) == [10, "hello", "hello", "hello"]

assert g.indices() == [0, 1, 2, 3]

assert g.select(is_even) == g.filter(is_even) == [10, 12]
assert g.reject(is_even) == [11, 13]
assert g.rotate(1) == [11, 12, 13, 10]
assert g.rotate(7) == [13, 10, 11, 12]
assert g.split_at(2) == ([10, 11], [12, 13])

h = L([1,1,2,3,4,4,4,5])
assert h.unique() == [1,2,3,4,5]

o1 = L([1, 2, 3, 4])
o2 = L([1, 2, 5, 4])
assert o1.first_mismatch(o2) == (3, 5)
assert o1.first_mismatch(o2, return_index=True) == 2
assert o1.mismatches(o2, return_index=True) == [2]
