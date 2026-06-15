# Multicast video with gums and parse it with threefive. 

### Receiving Multicast with threefive

* set multicast on the interface
```js
ip link set dev wlan0 multicast on
```

* To receive multicast, increase net.core.rmem_max from  212992 to 16777216
```js
sysctl -w net.core.rmem_max=16777216 

```
* increasing net.core.rmem_max allows threefive to scale up socket.SO_RCVBUF. 


* fire up threefive with the multicast address

```js
a@fu:~$ threefive udp://@235.35.3.5:3535
# SO_RCVBUF Was 212992 
# SO_RCVBUF Now 33554432 
# IP_MULTICAST_LOOP 1 
# SO_REUSEADDR 1 
# SO_REUSEPORT 1 
# Socket Timeout 60.0 


# Opening Multicast socket 


# IP_MULTICAST_TTL 32 

```

### Sendng Multicast with Gums


* set multicast on the interface
```js
ip link set dev wlan0 multicast on
```

* add a route for multicast
```js
ip route add 224.0.0.0/4 dev wlan0
```

* To send multicast, increase net.core.wmem_max from  212992 to 16777216
```js
sysctl -w net.core.wmem_max=16777216 

```
* increasing net.core.wmem_max allows Gums to scale up socket.SO_SNDBUF. 

* fire up gums 

```js
a@fu:~$ gums -i ~/mpegts/msnbc.ts
# SO_SNDBUF Was 212992 
# SO_SNDBUF Now 33554432 
# IP_MULTICAST_LOOP 1 
# SO_REUSEADDR 1 
# SO_REUSEPORT 1 
# Socket Timeout 60.0 


# Opening Multicast socket 


# IP_MULTICAST_TTL 32 

	Multicast Stream
	udp://@235.35.3.5:3535

	Source
	0.0.0.0:60591

```




