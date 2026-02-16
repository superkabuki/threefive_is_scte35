# Python Bit Manipulation slicing test.


# The Test

* Testing the performance of threefive's pure python bit slicer module, __bitn__, against the __suggested python approach__, the __bitstring__ python package and __bitarray__, a  python wrapper for a c library.

# Test criteria

* I'm going to test with python 3.11 and pypy3 7.3.11

* With a string of bytes : 
    * convert the bytes to an big integer
    * slice off 11 bits as an integer value
    * slice off 32 bits as an integer value
    * slice off 32 bits as an integer value
    * slice off 5 bits as an integer value
    * slice off 1 bit as an integer value
    * slice off 23 bits as an integer value

* The bits slices are intentionally not all byte aligned.

* testing with timeit.timeit and a count of 1,000,000

* To see how well each of them deal with larger amounts of data, we are going to test the following byte strings:
    * b'Adrian is super cool.'* 1
    * b'Adrian is super cool.'* 5
    * b'Adrian is super cool.'* 10
    * b'Adrian is super cool.'* 20
    * b'Adrian is super cool.'* 40
    * b'Adrian is super cool.'* 80
    * b'Adrian is super cool.'* 160

* The criteria of the test won't change,the same six slices each time, it will just be performed on a longer string of bytes.


# The Code
```py3
import timeit
from bitarray import bitarray
from  bitarray.util import ba2int
from threefive.bitn import Bitn
from bitstring import BitStream

BITES=b'Adrian is super cool.'
COUNT=1000000

def pbits():
    """
    Python's way: https://wiki.python.org/moin/BitManipulation
    """
    bits=bin( int.from_bytes(BITES, byteorder="big"))
    a=int(bits[3:14],2)
    b=int(bits[14:46],2)
    c=int(bits[46:78],2)
    d=int(bits[0:3],2)
    e=int(bits[78:79],2)
    f=int(bits[79:102],2)

def babits():
    """
    the bitarray package suggested as an alternative approach
    https://wiki.python.org/moin/BitManipulation
    """
    bits= bitarray(BITES)
    a=ba2int(bits[3:14])
    b=ba2int(bits[14:46])
    c=ba2int(bits[46:78])
    d=ba2int(bits[0:3])
    e= ba2int(bits[78:79])
    f=ba2int(bits[79:102])


def bstring():
    """
    bitstring package
    """
    bs = BitStream(BITES)
    a= bs.read(11).int
    b= bs.read(32).int
    c=bs.read(32).int
    d= bs.read(5).int
    e= bs.read(1).int
    f= bs.read(23).int
   
    

def bitn():
    """
    the bitn package was not mentioned. 
    """
    bn=Bitn(BITES)
    a=bn.as_int(11)
    b=bn.as_int(32)
    c=bn.as_int(32)
    d =bn.as_int(5)
    e =bn.as_int(1)
    f=bn.as_int(23)



if __name__=='__main__':
    for i in [1,5,10,20,40,80,160]:
        print(f"\nTesting with b'Adrian is super cool.' * {i}\n")
        BITES=b'Adrian is super cool.'*i
        print('\tbitn\t' ,timeit.timeit('bitn()',setup = "from __main__ import bitn",number=COUNT))
        print('\tPython\t', timeit.timeit('pbits()',setup = "from __main__ import pbits",number=COUNT))
        print('\tbitstring' ,timeit.timeit('bstring()',setup = "from __main__ import bstring",number=COUNT))
        print('\tbitarray' ,timeit.timeit('babits()',setup = "from __main__ import babits",number=COUNT))
```

# The Results ( lower is better)

### python 3.11
```js
a@fu:~/scratch$ python3 bittime.py 

Testing with b'Adrian is super cool.' * 1

	bitn	 1.0355922620074125
	Python	 1.0693426499929046
	bitarray 3.763978589006001
	bitstring 32.37975915199786

Testing with b'Adrian is super cool.' * 5

	bitn	 1.1405158970010234
	Python	 1.604970675005461
	bitarray 3.7265305500040995
	bitstring 32.28187718099798

Testing with b'Adrian is super cool.' * 10

	bitn	 1.2007743300055154
	Python	 2.3177184740052326
	bitarray 3.756743436009856
	bitstring 32.09028386899445

Testing with b'Adrian is super cool.' * 20

	bitn	 1.3562619209988043
	Python	 3.6830913059966406
	bitarray 3.7226608199998736
	bitstring 32.190319449000526

Testing with b'Adrian is super cool.' * 40

	bitn	 1.5767212390055647
	bitarray 3.7760885330062592
	Python	 6.321009808991221
	bitstring 32.37259433399595

Testing with b'Adrian is super cool.' * 80

	bitn	 2.160727769994992
	bitarray 3.879471256004763
	Python	 11.691836536992923
	bitstring 32.51724394399207

Testing with b'Adrian is super cool.' * 160

	bitn	 3.163175793000846
	bitarray 3.9027684749889886
	Python	 22.485538794993772
	bitstring 32.828337710991036

```
#### Python 3.11  test Results
#### bitn won every round of testing.
___

### Pypy3 7.3.11
```


### Try the test yourself.
