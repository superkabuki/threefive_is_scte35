## [ Cheap Tricks ]




### How to know what is required when encoding SCTE-35
* Whenever you encode a Cue, a Splice Info Section,  a Splice Command, or a Splice Descriptor, threefive will point out your mistakes.
<img width="1193" height="331" alt="image" src="https://github.com/user-attachments/assets/3e6f8df9-023f-4795-854f-ef0d311627b8" />
___

###  How to Parse SCTE-35 from HLS
* ABR HLS master.m3u8 manifests as well as single rendition manifests.
* all HLS SCTE-35 tags are supported as well as embedded SCTE-35 in the segments

```sed
threefive https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8
```
___

###  How to Visually verify SCTE-35 splice points
* use `threefive` with the `proxy` keyword.
* threefive with the proxy keyword copies all packets from a MPEGTS stream to stdout for piping.
* Play the video while you parse SCTE-35 over Multicast:
```sed
threefive proxy udp://@235.35.3.5:3535  | ffplay -
```
___

### How to send a Multicast Stream
* threefive includes The Grand Unified Multicast Sender, gums, for easy multicast.
* gums has a default multicast address of udp://@235.35.3.5.3535, that can be changed.
* gums is setup for mpegts streams. 1316 datagrams and video is throttled to playback speed _(fake live)_
* `gums -h` for all the details.

```smalltalk
a@fu:~$ gums -i ~/mpegts/cnn.ts
```
___

###  How to Show pts for iframes.
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

