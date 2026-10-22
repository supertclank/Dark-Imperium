"""Build/check the immutable production profile snapshot from canonical sources.

Only the declared release allowlist is exposed to clients. The server snapshot
retains source records verbatim, never regenerates canonical IDs or publishes
the full PHB package. Release changes require a new profile ID.
"""
import copy
import json
import sys
from pathlib import Path
import content_import as c

def build():
    _,records=c.load()
    spec=c.read(c.ROOT/'content/profiles/di-phb-1.0-narrow-v1.json')
    kit=copy.deepcopy(c.read(c.PACKAGE/'review/veteran-starting-package.json'))
    for choice in kit['choices']:
        choice['options']=[r for r in choice['options'] if r['id'] in spec['equipment']]
    training=next(x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json') if x['class']['id']==spec['classes'][0])
    table=next(t for t in c.read(c.PACKAGE/'evidence/tables.json') if t['rows'][0]==['Levels','Proficiency Bonus'])
    bands=[{'maximumLevel':int(row[0].split('-')[1]),'bonus':int(row[1])} for row in table['rows'][1:]]
    payload={'spec':spec,'records':records,'package':kit,'training':training,'proficiencyBands':bands,'approvals':c.read(c.PACKAGE/'review/decisions.json')}
    return {'digest':c.digest(payload),'payload':payload}

if __name__=='__main__':
    result=build();path=c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-narrow-v1.json'
    data=c.canonical(result)+b'\n'
    if '--check' in sys.argv:
        assert path.read_bytes()==data,'Profile changed: review and version the release; do not silently republish.'
    else:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Narrow profile snapshot:',result['digest'])
