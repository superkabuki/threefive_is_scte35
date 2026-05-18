"""
SCTE-35 2 Event Descriptors

The Event Descriptor Examples from the SCTE-35 part 2 specification

"""

from threefive import Cue

examples = {
    "Provider Opportunity": "/DBmAQAAAAAA/wAwBQb/Af/Z3wBQBU5DVUVJAAAALAAEAAAAAAAAABbjYAMFb3duZXICCHByb3ZpZGVyB2Fkc0luZm8CEWJyZWFraWQ9NDg1NzQwODA3CHNlcXVlbmNlAgMxLzIO0DXM",
    " Distributor Opportunity": "/DBOAQAAAAAA/wAwBQb/Af/Z3wA4BTZDVUVJAAAJ3QAEAAAAAAAAAAknwAIFb3duZXICC2Rpc3RyaWJ1dG9yCHNlcXVlbmNlAgMxLzIUroa3",
    "Break with Spot Replacement": "/DCWAQAAAAAA///wBQb/Af/Z3wCABSNDVUVJAAAAAQADAAAAAAAAABt3QAEIc2VxdWVuY2UCAzEvNAVZQ1VFSQAAAAsABQAAAAAAAAAEk+AEBGFkSWQCDEFCQ0QwMDAxMDAwSA9zcG90UmVwbGFjZW1lbnQBAQEFb3duZXICCHByb3ZpZGVyCHNlcXVlbmNlAgMxLzbrKnyt",
}

if __name__ == "__main__":
    for k, v in examples.items():
        side="-"*7 
        print(f"\n\n{side} {k} {side}\n")
        print(v, "\n")
        cue = Cue(v)
        methods = {
            "json": cue.json,
            "base64": cue.encode,
            "bytes": cue.bytes,
            "hex": cue.hex,
            "int": cue.int,
            "xml": cue.xml,
            "xmlbin": cue.xmlbin,
        }
        for k, v in methods.items():
            side="-" *3
            print(f"\n\t{side} {k} {side}\n")
            print(f"\t{v()}")
