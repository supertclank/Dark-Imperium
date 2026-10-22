"""Compose the second immutable tier-1 release from individually reviewed paths."""
import copy,json,sys
import content_import as c
import export_tier1_profile as previous
import tier1_catalogue as audit

ORIGINS=['hiveborn','shrine_worlder','penal_worlder','voidborn','forge_world','schola_progenium','militarum_regiment','underhive']

def package(fixed,choices,armour,source,contacts=()):
    display={'fixed':[{'item':{'id':k},'quantity':n} for k,n in fixed], 'choices':[{'id':key,'options':[{'id':k} for k in options],'quantity':1} for key,options in choices], 'source':source}
    steps=[{'kind':'item','itemId':k,'quantity':n} for k,n in fixed]
    for key,options in choices:
        steps.append({'kind':'choice','id':key,'min':1,'max':1,'options':[{'id':k,'steps':[{'kind':'item','itemId':k,'quantity':1}]+([{'kind':'equip','itemId':k}] if k in armour else [])} for k in options]})
    steps += [{'kind':'equip','itemId':k} for k,n in fixed if k in armour]
    steps += [{'kind':'contact','id':'black_market_contact','text':text} for text in contacts]
    return {'display':display,'executable':{'schemaVersion':1,'source':source,'steps':steps},'quantityBasis':'One instance of each singular named kit entry; explicit grenade counts retained. No runtime quantity default.'}

def build():
    _,records=c.load();c.validate_records(records);old=previous.build()['payload'];spec=copy.deepcopy(old['spec'])
    spec.update(id='di-phb-1.0-tier1-v2',name='PHB 1.0 · Human Veterans and Hive Scum',compositionVersion=2,levels=[1,2,3],origins=['di.background.'+o for o in ORIGINS],classes=['di.class.veteran','di.class.hive_scum'])
    spec['equipment']=sorted(set(spec['equipment']+['di.weapon.knife','di.weapon.autogun','di.weapon.autopistol','di.weapon.stub_pistol']))
    configs=[];paths=[];choices=set()
    for origin in spec['origins']:
        assert audit.eligible(records[origin],'di.species.human') is True
        assert next(x for x in records[origin]['data']['originAvailability'] if x['species']['id']=='di.species.human')['state']=='NORMAL'
        for klass,levels in [('di.class.veteran',[1,2,3]),('di.class.hive_scum',[1])]:
            for level in levels:
                dep=audit.selected_features(records,['di.species.human',origin,klass],level)
                selected=set(dep['choices'])|{'di.choice.human.broad_training_proof'}
                # Human/class source features may refer to choice grants; all dependencies must be explicit.
                if klass=='di.class.veteran':selected|={'di.choice.veteran.starting_skills','di.choice.veteran.specialist_group'}
                selected.discard('di.choice.creation.universal_trait')
                choices|=selected
                config={'speciesId':'di.species.human','originId':origin,'classId':klass,'level':level,'choices':sorted(selected),'features':sorted(dep['features'])}
                configs.append(config)
                subs=records[klass]['data']['allowedSubclasses'] if level==3 else [None]
                for sub in subs:paths.append({**{k:v for k,v in config.items() if k not in ('choices','features')},'subclassId':sub['id'] if sub else None,'traitId':'di.feature.universal.twitchy'})
    spec.update(choices=sorted(choices),pathConfigurations=configs,certifiedPaths=paths)
    spec['availability']=[{'status':'SUPPORTED','message':'Human NORMAL Origins: Veteran levels 1–3 (three manually adjudicated doctrines), or Hive Scum level 1. Twitchy and reviewed equipment branches only. Suppressing Fire is unavailable pending a ruling.'}, {'status':'RARE','message':'Rare Origins require trusted GM approval and are unavailable for self-service creation.'},{'status':'LIMITED','message':'Limited Origins require combination-specific campaign approval and are unavailable for self-service creation.'},{'status':'COMING_LATER','message':'Zealot, Arbites, psychic paths, non-Humans and other levels remain uncertified. Older characters retain their original profile.'}]
    source=old['package']['source'];vet={'display':old['package'],'executable':old['executablePackage'],'quantityBasis':'Previously reviewed Veteran branch'}
    scumSource=copy.deepcopy(source);scumSource['locator']['heading']='Hive Scum starting kit'
    scum=package([('di.weapon.knife',1),('di.weapon.frag_grenade',1)],[('pistol',['di.weapon.autopistol','di.weapon.stub_pistol']),('primary',['di.weapon.autogun']),('armour',['di.armour.flak_armour'])],spec['armour'],scumSource,['Black-market contact: identity and relationship are agreed with the GM.'])
    training={x['class']['id']:x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json') if x['class']['id'] in spec['classes']}
    support={}
    for origin in spec['origins']:
        for ref in records[origin]['data']['features']:
            support[ref['id']]={'classification':'PARTIAL','playerNote':'Skill training is included. Apply conditional benefits manually; baseline rolls do not apply them.','rulingIds':[],'resources':[]}
    resourceOrigins={'penal_worlder':('dirty_survival','long_rest'),'shrine_worlder':('litany_of_resolve','long_rest'),'forge_world':('logic_before_fear','long_rest'),'militarum_regiment':('field_discipline','short_rest'),'underhive':('never_fight_fair','short_rest')}
    for origin,(key,recovery) in resourceOrigins.items():support['di.feature.origin.'+origin]['resources']=[{'key':key,'maximum':1,'recovery':recovery,'automation':'manual'}]
    support['di.feature.origin.voidborn']['proceduralProficiencies']=['Basic voidship procedures','Airlocks','Auspex consoles','Pressure doors','Shipboard emergency systems']
    support['di.feature.origin.militarum_regiment']['playerNote']='Choose an eligible ally before initiative to apply Squad Drill manually. Baseline initiative excludes that conditional +1. Field Discipline is unavailable until Suppression is resolved.'
    support['di.feature.origin.militarum_regiment']['rulingIds']=['PHB-RULE-022']
    support['di.feature.class.veteran.level_2.suppressing_fire']={'classification':'BLOCKED','playerNote':'Unavailable: the Suppression procedure is awaiting a ruling. No save DC, condition or automatic roll is supplied. Other character actions remain available.','rulingIds':['PHB-RULE-022'],'resources':[]}
    for sub in ['shock_trooper','marksman','sergeant']:
        support[f'di.feature.subclass.veteran.{sub}.level_3']={'classification':'MANUAL','playerNote':'Apply this feature only when its stated condition occurs. It is not included in baseline rolls. Combined-source stacking requires adjudication; no stacking policy is assumed.','rulingIds':['PHB-RULE-058'],'resources':[]}
    support['di.feature.class.hive_scum.level_1.dirty_fighter']={'classification':'MANUAL','playerNote':'Apply the conditional extra damage manually, once per turn. Baseline damage excludes it. Conditions and combined-source stacking are not automated.','rulingIds':['PHB-RULE-046','PHB-RULE-058'],'resources':[]}
    support['di.feature.class.hive_scum.level_1.streetwise']={'classification':'PARTIAL','playerNote':'The two selected skill proficiencies are calculated. Finding contacts is manual.','rulingIds':[],'resources':[]}
    payload={**copy.deepcopy(old),'spec':spec,'records':records,'packages':{'di.class.veteran':vet,'di.class.hive_scum':scum},'classTraining':training,'featureSupport':support}
    payload['equipmentSupport']={'di.weapon.knife':'Melee mode only. Throwing requires a GM-approved improvised range.','di.weapon.autogun':'Baseline single attack/damage only. Burst and Suppression procedures remain unavailable pending PHB-RULE-020/022.','di.weapon.autopistol':'Baseline single attack/damage only. Burst procedure remains unavailable pending PHB-RULE-020.'}
    return {'digest':c.digest(payload),'payload':payload}

if __name__=='__main__':
    result=build()
    for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v2.json',result),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v2.json',result['payload']['spec'])]:
        data=c.canonical(value)+b'\n'
        if '--check' in sys.argv or path.exists():assert path.read_bytes()==data,'Immutable release differs: '+str(path)
        else:path.write_bytes(data)
    print(result['digest'])
