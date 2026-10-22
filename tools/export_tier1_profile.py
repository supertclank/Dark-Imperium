"""Export the independently certified initial tier-1 branch; never mutate narrow."""
import copy
import sys
import content_import as c
import export_narrow_profile
import tier1_catalogue

def build():
    _,records=c.load();c.validate_records(records)
    approvals=c.read(c.PACKAGE/'review/human-rulings-integration.json')
    assert all(tier1_catalogue.validate_approval(next(x for x in approvals if x['id']==f'PHB-RULE-{n:03}'),origin=True) for n in range(1,8))
    old=export_narrow_profile.build()['payload'];spec=copy.deepcopy(old['spec'])
    spec.update(id='di-phb-1.0-tier1-v1',engineVersion='phb-tier1-kotlin-v1',name='PHB 1.0 · Hiveborn Veteran')
    spec['origins']=['di.background.hiveborn']
    spec['choices']=[x for x in spec['choices'] if not x.startswith('di.choice.schola_progenium.')]+['di.choice.hiveborn.skills']
    spec['certifiedPaths']=[{'speciesId':'di.species.human','originId':'di.background.hiveborn','classId':'di.class.veteran','level':1,'traitId':'di.feature.universal.twitchy'}]
    spec['availability']=[{'status':'SUPPORTED','message':'Human / Hiveborn / Veteran, level 1, Twitchy and the reviewed lasgun/medpack kit. Crowd terrain and situational fear-save advantage require manual adjudication.'},
       {'status':'RARE','message':'Rare Origin — requires GM approval. Ogryn Hiveborn/Voidborn and Ratling Shrine Worlder are unavailable for self-service creation.'},
       {'status':'LIMITED','message':'Limited Origin — requires explicit campaign approval. Skitarii Militarum Regiment is unavailable for self-service creation.'},
       {'status':'COMING_LATER','message':'Other NORMAL paths and levels 2–3 require independent certification. Existing narrow characters retain their original profile.'}]
    kit=copy.deepcopy(old['package'])
    steps=[{'kind':'item','itemId':x['item']['id'],'quantity':x['quantity']} for x in kit['fixed']]
    steps += [{'kind':'equip','itemId':x} for x in spec['armour']]
    steps += [{'kind':'choice','id':x['id'],'min':1,'max':1,'options':[{'id':o['id'],'steps':[{'kind':'item','itemId':o['id'],'quantity':x['quantity']}]} for o in x['options']]} for x in kit['choices']]
    executable={'schemaVersion':1,'source':kit['source'],'steps':steps}
    payload={'spec':spec,'records':records,'package':kit,'executablePackage':executable,'training':old['training'],'proficiencyBands':old['proficiencyBands'],'approvals':c.read(c.PACKAGE/'review/decisions.json'),'originAvailabilityPolicy':c.read(c.PACKAGE/'review/origin-availability-policy.json')}
    return {'digest':c.digest(payload),'payload':payload}

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
