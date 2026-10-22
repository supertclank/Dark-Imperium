"""Export the independently certified initial tier-1 branch; never mutate narrow."""
import copy
import sys
import content_import as c
import export_narrow_profile
import tier1_catalogue

def build():
    result=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v1.json')
    assert result['digest']=='d75739125210dd704ca0b3362a2c864a0fdd32b6b2765b0bbc137f5792971f32'
    assert c.digest(result['payload'])==result['digest']
    assert result['payload']['spec']==c.read(c.ROOT/'content/profiles/di-phb-1.0-tier1-v1.json')
    return result

if __name__=='__main__':
    result=build()
    for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v1.json',result),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v1.json',result['payload']['spec']),(c.PACKAGE/'review/starting-packages/veteran-certified.json',result['payload']['executablePackage'])]:
        data=c.canonical(value)+b'\n'
        if '--check' in sys.argv:assert path.read_bytes()==data,'Immutable profile differs: '+str(path)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():assert path.read_bytes()==data,'Released profile is immutable; use a new ID: '+str(path)
            else:path.write_bytes(data)
    print(result['digest'])
