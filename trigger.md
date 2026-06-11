# Trigger on SCTE-35 Cues in MPEGTS Streams.

By default, threefive.Stream prints the SCTE-35 data to stderr. The reason it prints the stream is so you can see threefive working right out of the box. 
How threefive.Stream prints the message is by passing it a function as an arg.

* These threefive.Stream methods all accept an optional func arg.
```py3
def decode(self, func=show_cue):

def decode_pcr(self, func=show_cue):

def decode_pids(self, scte35_pids=None, func=show_cue):

def proxy(self, func=show_cue):
```

* The interface for the function is 
```py3
func(cue)
```
The function can accept only one arg, a threefive.Cue instance.
___

# A better Way

> I used a function arg like that for years, but then a guy sent me a pull request with a decode_next() method.
> decode_next() is a python generator that yields a threefive.Cue instance when SCTE-35 is found in an mpegts Stream. 

* Stream.decode_next() works great in a for loop 
* You can do anything you want with the SCTE-35 Cue.

```py3
 from threefive import Stream
 s=Stream('/home/a/mpegts/msnbc.ts')
 for cue in s.decode_next():

     # Custom Cue handling goes here here
     #  for example.....

     pts = cue.command.has('pts_time') # get pts from the Cue instance
     dsptr = cue.descriptors[0]
     if dsptr.tag== 2:  # if the first descriptor is a Segmentation Descriptor
         seg_mesg=dsptr.has('segmentation_message')  #  get segmentation message
         if 'Program' not in seg_mesg and 'Start' in seg_mesg:
             # Add on segmentation duration if it exists
             seg_mesg = f"{seg_mesg} {dsptr.has('segmentation_duration')}"
         print(pts,seg_mesg)
```

* output
```py3
24722.499289 Program End
24722.499289 Program Start
25732.332622 Break Start 59.966667
25792.365956 Break End
26483.399289 Break Start 270.0
26693.399289 Distributor Placement Opportunity Start 60.033333
26753.432622 Distributor Placement Opportunity End
26753.399289 Break End
27156.965956 Break Start 209.966667
27306.932622 Distributor Placement Opportunity Start 60.066667
27366.965956 Distributor Placement Opportunity End
27366.932622 Break End
27554.132622 Break Start 239.966667
27794.132622 Break End
28192.565956 Program End
28192.565956 Program Start
28938.565956 Break Start 59.933333
28998.565956 Break End
29451.599289 Break Start 270.0
29631.632622 Distributor Placement Opportunity Start 89.966667
29721.632622 Distributor Placement Opportunity End
29721.599289 Break End
30078.232622 Break Start 270.033333
30258.265956 Distributor Placement Opportunity Start 89.966667
30348.299289 Distributor Placement Opportunity End
30348.265956 Break End
30662.832622 Break Start 269.966667
30932.799289 Break End
31316.099289 Break Start 239.966667
31496.132622 Distributor Placement Opportunity Start 60.033333
31556.132622 Distributor Placement Opportunity End
31556.099289 Break End
31858.599289 Program End
```


