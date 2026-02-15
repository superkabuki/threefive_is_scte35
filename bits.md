# Python Bit Manipulation slicing test.


# The Test

* Testing the performance of threefive's bit slicer module, __bitn__, against the __suggested python approach__, and the __package bitarray__.

# Test criteria

* With a string of bytes : 
    * convert the bytes to an big integer
    * slice off 11 bits as an integer value
    * slice off 32 bits as an integer value
    * slice off 32 bits as an integer value
    * slice off 5 bits as an integer value
    * slice off 1 bit as an integer value
    * slice off 23 bits as an integer value

* The bits slices are intentionally not all byte aligned

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
    bits = bin( int.from_bytes(BITES, byteorder="big"))[2:]
    bits = bitarray(bits)
    a=ba2int(bits[3:14])
    b=ba2int(bits[14:46])
    c=ba2int(bits[46:78])
    d=ba2int(bits[0:3])
    e= ba2int(bits[78:79])
    f=ba2int(bits[79:102])

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
        print('\tbitarray' ,timeit.timeit('babits()',setup = "from __main__ import babits",number=COUNT))
```

# The Results ( lower is better)
```js
a@fu:~/scratch$ python3 bittime.py 

Testing with b'Adrian is super cool.' * 1

	bitn	 1.0533314130007057
	Python	 1.0576630479990854
	bitarray 4.63300140100182

Testing with b'Adrian is super cool.' * 5

	bitn	 1.1732930180005496
	Python	 1.6305488669968327
	bitarray 7.181534543000453

Testing with b'Adrian is super cool.' * 10

	bitn	 1.258845651995216
	Python	 2.3609297400034848
	bitarray 10.367007496999577

Testing with b'Adrian is super cool.' * 20

	bitn	 1.3913910670016776
	Python	 3.685456153994892
	bitarray 16.468871650999063

Testing with b'Adrian is super cool.' * 40

	bitn	 1.6337268499992206
	Python	 6.356403646997933
	bitarray 28.879704566999862

Testing with b'Adrian is super cool.' * 80

	bitn	 2.203413962997729
	Python	 11.787694664999435
	bitarray 54.989689134999935

Testing with b'Adrian is super cool.' * 160

	bitn	 3.237896588005242
	Python	 22.546146710999892
	bitarray 104.07794349399774
```

### Try the test yourself.
