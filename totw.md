# [ Tip of the Week ]

> I used to work for a guy who came to programming from a literary background and he urged us to make the code read like natural language, to make it easier to follow. 
> threefive __Cues, Commands, and Descriptors__ all have a method called __has__, it returns the value of the attribute if it exists, or None if it doesn't.
> It's very natural to say `cue.command.has("pts_time")` whereas saying  `hasattr(cue.command,"pts_time")` is kind of clunky and awkward.

* instead of doing something like this:
```py3
pts = None
if hasattr(cue.command,'pts_time):
	pts = cue.command.pts_time
```
* __do this__
```py3
pts= cue.command.has("pts_time")
```
* instead of
```py3
if hasattr(cue.command,'break_duration'):
	duration = cue.command.break_duration
elif hasattr(cue.descriptors[0],'segmentation_duration'):
	duration= cue.descriptors[0].segmentation_duration
else:
	duration=None
```
* __do this__
```py3
duration= cue.command.has('break_duration')
if not duration:
	duration= cue.descriptors[0].has('segmentation_duration')
```
> __Readable code is much easier to maintain__.

___
