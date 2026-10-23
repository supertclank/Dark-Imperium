"""Human advancement and reviewed Ratling level-one families; retain prior snapshots."""
import copy,sys
import content_import as c
import export_tier1_v2_profile as previous
import tier1_catalogue as audit

def compose_historical_v3():
    _,records=c.load();c.validate_records(records)
    payload=copy.deepcopy(previous.build()['payload']);spec=payload['spec'];payload['records']=records
    spec.update(id='di-phb-1.0-tier1-v3',name='PHB 1.0 · Human and Ratling',speciesComposition=True)
    spec['species'].append('di.species.ratling')
    for suffix in ['hiveborn','penal_worlder','voidborn','militarum_regiment','underhive']:
        origin='di.background.'+suffix
        assert next(x for x in records[origin]['data']['originAvailability'] if x['species']['id']=='di.species.ratling')['state']=='NORMAL'
        for klass in spec['classes']:
            dep=audit.selected_features(records,['di.species.ratling',origin,klass],1)
            choices=set(dep['choices'])-{'di.choice.creation.universal_trait'}
            if klass=='di.class.veteran':choices|={'di.choice.veteran.starting_skills','di.choice.veteran.specialist_group'}
            config=dict(speciesId='di.species.ratling',originId=origin,classId=klass,level=1,choices=sorted(choices),features=sorted(dep['features']))
            spec['pathConfigurations'].append(config)
            spec['certifiedPaths'].append({k:v for k,v in config.items() if k not in ('choices','features')}|dict(subclassId=None,traitId='di.feature.universal.twitchy'))
    spec['choices']=sorted(set(x for config in spec['pathConfigurations'] for x in config['choices']))
    spec['availability'][0]['message']='Human NORMAL Origins: Veteran levels 1–3 and Hive Scum level 1. Ratling NORMAL Hiveborn, Penal, Voidborn, Militarum and Underhive: Veteran or Hive Scum level 1. Twitchy and reviewed kit branches only. Conditional features require manual adjudication.'
    spec['availability'][-1]['message']='Other species, Ratling higher levels and Sharpshooter remain uncertified. Existing characters retain their pinned profile.'
    payload['featureSupport']['di.feature.species.ratling.traits']={'classification':'PARTIAL','playerNote':'Stealth and 60 ft darkvision are calculated. Small Target, Sniper’s Eye, Lucky Shot and Bad in a Straight Fight are manual. No generic Small weapon penalty is applied. Darkvision uses the longest granted range; it does not penetrate smoke, solids or psychic darkness.','rulingIds':[],'resources':[{'key':'lucky_shot','maximum':1,'recovery':'short_rest','automation':'manual'}]}
    return {'digest':c.digest(payload),'payload':payload}

def build():
    b=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v3.json')
    assert b['digest']=='5c4d81d1cf9a55be138d5e73a58acfccd96fb2dcb0eeadb157fbcfde08b2a795'
    assert c.digest(b['payload'])==b['digest']
    return b

if __name__=='__main__':
    result=build()
    for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v3.json',result),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v3.json',result['payload']['spec'])]:
        data=c.canonical(value)+b'\n'
        if '--check' in sys.argv or path.exists():assert path.read_bytes()==data,'Immutable release differs: '+str(path)
        else:path.write_bytes(data)
    print(result['digest'])
