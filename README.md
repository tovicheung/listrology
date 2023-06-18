# Listrology
name is suggested by our good friend chatgpt
Listrology extends the functionality of lists

## Installation
`pip install listrology`

## Usage

Listrology contains a subclass of list which provides a number of methods that are useful
```py
from listrology import List
assert List([1, 2, 3]) == [1, 2, 3]
```
Square bracket prefix is also supported
```py
from listrology import List
assert List[4, 5, 6] == [4, 5, 6]
```
There is also a shorthand constructor
```py
from listrology import L, List
assert L[7, 8, 9] == List[7, 8, 9] == [7, 8, 9]
```
Some methods include
```py
mylist = L[0, 1, 2, 3, 4, 5, 6]

mylist.foreach(print) # prints all elements one by one
mylist.reject(lambda x: x == 2) # [0, 1, 3, 4, 5, 6]

# copy elements mylist[5:7] and use it to overwrite elements starting at mylist[1]
mylist.overwrite(target=1, start=5, end=7) # [0, 5, 6, 3, 4, 5, 6]

mylist.first(lambda x: x % 2 == 1) # 1 (first one that is odd)

mylist.fill("yo", 2, 4) # [0, 1, "yo", "yo", 4, 5, 6]

# each rotation the first element is put to last (inspired by Ruby)
mylist.rotate(1) # [1, 2, 3, 4, 5, 6, 0]
mylist.rotate(2) # [2, 3, 4, 5, 6, 0, 1]
```
listrology's lists supports method chaining (each method produces a new instance)
```py
volcano_heights = L[412, 399, 276, 591, 482, 451, 521, 529, 521, 426, 511, 426, 426]
# find all volcano heights that are 400m-525m tall and remove duplicates and sort then
result = volcano_heights.filter(lambda x: 400 <= x <= 525).unique().sort()
# [412, 426, 451, 482, 511, 521]

```