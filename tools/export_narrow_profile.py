"""Verify the frozen narrow release independently of the development catalogue.

The bundled immutable snapshot retains its original canonical source records and
approvals. New approvals and catalogue revisions belong to a new profile ID.
"""
import copy
import json
import sys
from pathlib import Path
import content_import as c

def build():
    result=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json')
    assert result['digest']=='3d1235b3cb86ac5c8939c94a9c55964e07e1ce96d7b05d20966feb7dd78001af'
    assert c.digest(result['payload'])==result['digest'],'Frozen release snapshot corrupted'
    assert result['payload']['spec']==c.read(c.ROOT/'content/profiles/di-phb-1.0-narrow-v1.json')
    return result

if __name__=='__main__':
    result=build();path=c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json'
    data=c.canonical(result)+b'\n'
    if '--check' in sys.argv:
        assert path.read_bytes()==data,'Profile changed: review and version the release; do not silently republish.'
    else:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Narrow profile snapshot:',result['digest'])
