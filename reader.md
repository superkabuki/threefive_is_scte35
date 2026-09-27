# threefive.reader


__threefive.reader__ is one function to handle __stdin, files, http(s), multicast, SRT, and UDP__ all the same way.

reader __returns an object with a read method__ no matter which protocol is used. 
 
reader __requires a uri__, and has an __optional arg for http(s) or SRT headers__.

```py3
reader(uri, headers={})
```       
    
### Examples:
```py3
        >>> from threefive import reader
    
        >>> with reader('http://iodisco.com/') as disco:
        >>> disco.read()
    
        >>> with reader('http://iodisco.com/',headers={"myHeader":"DOOM"}) as doom:
        >>> doom.read()
    
        >>> with reader("udp://@227.1.3.10:4310") as data:
        >>> data.read(8192)
    
        >>> with reader("/home/you/video.ts") as data:
        >>> fu = data.read()
    
        >>> udp_data =reader("udp://1.2.3.4:5555")
        >>> chunks = [udp_data.read(188) for i in range(0,1024)]
```
