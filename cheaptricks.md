## [ Cheap Tricks ]

##### 1) __Parse SCTE-35 from HLS__ 
* ABR HLS master.m3u8 manifests as well as single rendition manifests.
* all HLS SCTE-35 tags are supported as well as embedded SCTE-35 in the segments

```sed
threefive https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8
```

##### 2) Visually verify SCTE-35 splice points using `threefive` with the `proxy` keyword.
* threefive with the proxy keyword copies all packets from a MPEGTS stream to stdout for piping.

* Play the video while you parse SCTE-35 over Multicast:

```sed
threefive proxy udp://@235.35.3.5:3535  | ffplay -
```

##### 3) threefive incudes The Grand Unified Multicast Sender, gums, for easy multicast.
* gums has a default multicast address of udp://@235.35.3.5.3535, that can be changed.
* gums is setup for mpegts streams. 1316 datagrams and video is throttled to playback speed _(fake live)_
* `gums -h` for all the details.

```smalltalk
a@fu:~$ gums -i ~/mpegts/cnn.ts
```
___

##### 4) Show pts for iframes.
```sed
a@fu:~$ threefive iframes ~/mpegts/longb2.ts
/home/a/mpegts/longb2.ts
1.433
6.772
9.141
12.11
17.449
22.788
```

