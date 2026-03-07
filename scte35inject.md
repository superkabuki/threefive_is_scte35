# SCTE-35 Packet Injection 

## Cli


```js

a@fu:~/threefive$ scte35inject help
usage: scte35inject [-h] [-i INPUT] [-o OUTPUT] [-s SIDECAR] [-p SCTE35_PID] [-t]
                         [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input source, like "/home/a/vid.ts" or "udp://@235.35.3.5:3535"
                        or "https://futzu.com/xaa.ts" [
                        default:sys.stdin.buffer ]
  -o OUTPUT, --output OUTPUT
                        Output file [ default:sys.stdout.buffer ]
  -s SIDECAR, --sidecar SIDECAR
                        Sidecar file for SCTE35 [ default:sidecar.txt ]
  -p SCTE35_PID, --scte35_pid SCTE35_PID
                        Pid for SCTE-35 packets [ default:0x86 ]
  -t, --time_signals    Flag to insert Time Signal cues at iframes.
  -v, --version         Show version

scte35inject is part of threefive
```
## testing example
* insert a TimeSignal at every iframe
```js

a@fu:~/threefive$ touch sidecar.txt       


@fu:~/threefive$ scte35inject  -t -i ~/mpegts2/mpegts/nmax.ts  -p 777 -o injected-nmax.ts

Output File:	injected-nmax.ts


```


## Usage example

```js
a@fu:~/threefive$ scte35inject --input ~/mpegts2/mpegts/nmax.ts --sidecar ~/sidecar.txt --scte35_pid 777 --output injected-nmax.ts

Output File:	injected-nmax.ts

Inserted Cue:
	@9187.566978, /DAgAAAAAAAAAP/wDwUAAAABf//+AA27oAABAAAAANwB3tE=

Inserted Cue:
	@9189.201944, /DAgAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAAANaNPVc=

Inserted Cue:
	@9189.568978, /DAgAAAAAAAAAP/wDwUAAAABf//+AFJlwAABAAAAAMOOklg=

Inserted Cue:
	@9191.570978, /DAgAAAAAAAAAP/wDwUAAAABf//+AA27oAABAAAAANwB3tE=

Inserted Cue:
	@9193.572978, /DAgAAAAAAAAAP/wDwUAAAABf//+AKTLgAABAAAAANaNPVc=

Inserted Cue:
	@9195.574978, /DAgAAAAAAAAAP/wDwUAAAABf//+AFJlwAABAAAAAMOOklg=
a@fu:~/threefive$ 

```

## Sidecar Files
* insert_pts , SCTE-35 Cue (Base64 or Hex or Int or Bytes)
* example

```sh
130.12,/DAWAAAAAAAAAP/wBQb+ALKOoAAAJte19A==
131.941333,/DAWAAAAAAAAAP/wBQb+ALViYAAAX0rDFg==
133.925333,/DAWAAAAAAAAAP/wBQb+ALghgAAAZ1bwhQ==
136.0,/DAWAAAAAAAAAP/wBQb+ALrgoAAAZcGYgA==
137.957333,/DAWAAAAAAAAAP/wBQb+AL2fwAAA+pqf0g==
139.941333,/DAWAAAAAAAAAP/wBQb+AMBe4AAAxHrXOA==
140.16,/DAWAAAAAAAAAP/wBQb+AMBEoAAAALVriA==
141.925333,/DAWAAAAAAAAAP/wBQb+AMMeAAAAbxYdWg==
144.0,/DAWAAAAAAAAAP/wBQb+AMXdIAAA8W/eBQ==
145.957333,/DAWAAAAAAAAAP/wBQb+AMicQAAAmT+Gzw==
147.941333,/DAWAAAAAAAAAP/wBQb+AMtbYAAAEkrtmw==

```
* insert_pts is when to insert the SCTE-35 data, it should be 4-10 seconds before the splice point.
