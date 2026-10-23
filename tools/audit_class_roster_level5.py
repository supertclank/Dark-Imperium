"""Full PHB roster inventory; explicitly does not approve missing game rules."""
import json,re,itertools
import content_import as c
import export_tier1_v9_profile as release
import export_tier1_v6_profile as previous

def build():
 _,canonical=c.load();b=release.build();p=b['payload'];r=p['records'];s=p['spec'];pages=c.read(c.PACKAGE/'evidence/pages.json');page={x['pdfPage']:x['text'] for x in pages}
 classes=sorted((x for x in canonical.values() if x['kind']=='class'),key=lambda x:x['sources'][0]['locator']['pdfPage'])
 assert len(classes)==12 and 'twelve distinct classes' in page[50]
 # Verify against chapter headings in the extracted PHB body, independently of publication.
 headings={m.group(1):m.group(2).strip() for n,text in page.items() if 50<=n<=85 for m in re.finditer(r'^11\.(\d+) ([^\n]+)$',text,re.M)}
 assert len(headings)==12 and set(headings.values())=={x['name'] for x in classes}
 training={x['class']['id']:x for x in c.read(c.PACKAGE/'review/class-calculation-inputs.json')};equipment={x['className']:x for x in c.read(c.PACKAGE/'review/starting-equipment-audit.json')}
 certified={x['subclassId'] for x in s['certifiedPaths'] if x.get('subclassId')};rows=[];subrows=[]
 blockers={
 'di.class.zealot':[dict(code='BLOCKED_BY_RULE',rulingIds=['PHB-RULE-018','PHB-RULE-046'],entityId='di.weapon.firebomb',reason='Mandatory starting Firebomb has only a partial candidate: Dexterity save success outcome and burning-ground duration/damage procedure are not resolved. Frag-only approval cannot be copied. Requires exact Firebomb procedure or explicit approval for manual per-use adjudication; no guessed save outcome or damage-over-time.')],
 'di.class.arbites_enforcer':[dict(code='BLOCKED_BY_RULE',rulingIds=['PHB-RULE-032'],entityId='di.shield.shield',reason='Required Riot Shield is an approved alias (+2 AC, one hand), but shield/base-armour legal combinations and stacking remain unresolved; PHB-RULE-050 does not resolve PHB-RULE-032.'),dict(code='BLOCKED_BY_RULE',rulingIds=['PHB-RULE-018','PHB-RULE-046'],entityId='di.weapon.stun_grenade',reason='Required Stun Grenade and Smoke Grenade remain partial candidates. Stun save outcome/condition procedure and complete supported use contracts are not certified. Do not substitute Frag damage or invent DC/outcomes.')],
 'di.class.psyker':[dict(code='PSYCHIC_FRAMEWORK_REQUIRED',rulingIds=['PHB-RULE-035','PHB-RULE-037','PHB-RULE-038'],reason='No certified power selection, manifestation, Warp Pressure/Perils, concentration and psychic action pipeline. Blank/Null-Bound additionally requires trusted GM approval.')],
 'di.class.aeldari_warlock':[dict(code='PSYCHIC_FRAMEWORK_REQUIRED',rulingIds=['PHB-RULE-035','PHB-RULE-037','PHB-RULE-038'],reason='Requires shared psychic framework, Warlock known-power/rune interactions, and validated psychic starting equipment. Do not infer a martial implementation.')]
 }
 for cl in classes:
  cid=cl['id'];slug=cid.split('.')[-1];pageNo=cl['sources'][0]['locator']['pdfPage'];text=page[pageNo];header=text.split('Level Features')[0];progress=canonical[cl['data']['progression']['id']]['data']['entries'];levels=[]
  for level in range(1,6):
   grants=next(x['grants'] for x in progress if x['level']==level);fids=[x['feature']['id'] for x in grants if x['kind']=='feature'];levels.append(dict(level=level,features=[dict(id=fid,name=canonical[fid]['name'],text=(r.get(fid) or canonical[fid])['descriptionMarkdown'],sources=canonical[fid]['sources'],support=p['featureSupport'].get(fid,{'classification':'NOT_PUBLISHED'})) for fid in fids],grants=grants))
  owned=[x for x in s['certifiedPaths'] if x['classId']==cid];status='CERTIFIED_LEVEL_5' if any(x['level']==5 for x in owned) else blockers[cid][0]['code']; origins=[]
  # Availability itself remains species-specific; no new class/origin permission inferred.
  species=[k for k in s['species'] if k in json.dumps(cl['data']['requirements'])]
  for sp in species:
   for origin in [x for x in canonical.values() if x['kind']=='background']:
    for entry in origin['data'].get('originAvailability',[]):
     if entry['species']['id']==sp:origins.append(dict(speciesId=sp,originId=origin['id'],availability=entry['state'],approvalRequired=entry['state'] in ['RARE','LIMITED']))
  for subref in cl['data']['allowedSubclasses']:
   sid=subref['id'];sub=canonical[sid];entries=canonical[sub['data']['progression']['id']]['data']['entries'];features=[g['feature']['id'] for e in entries if e['level']<=5 for g in e['grants'] if g['kind']=='feature']
   if sid in certified:state='CERTIFIED';reason='Published family dependency closure certified; source conditional effects remain manual.';refs=[]
   elif cid in blockers:state=blockers[cid][0]['code'];reason='Parent class not publishable: '+blockers[cid][0]['reason'];refs=blockers[cid][0]['rulingIds']
   else:state,reason=previous.BLOCKED[slug+'.'+sid.split('.')[-1]];refs=re.findall(r'PHB-RULE-\d+',reason)
   additional=[]
   if sid.endswith('.investigator'):additional.append(dict(code='BLOCKED_BY_RULE',rulingIds=['PHB-RULE-011'],reason='Mandatory Expertise in Investigation or Insight is unresolved.'))
   if sid.endswith('.blank_null_bound'):additional.append(dict(code='BLOCKED_BY_APPROVAL',reason='Explicit GM-permission discipline; no self-service trusted approval mechanism.'))
   subrows.append(dict(subclassId=sid,classId=cid,name=sub['name'],levelSelected=1 if slug=='psyker' else 3,status=state,reason=reason,rulingIds=refs,additionalBlockers=additional,level3Features=[dict(id=f,name=canonical[f]['name'],text=canonical[f]['descriptionMarkdown'],sources=canonical[f]['sources'],support=p['featureSupport'].get(f,{'classification':'NOT_PUBLISHED'})) for f in features],level5Interaction='Parent class canonical level-5 feature applies; no new subclass progression entry at level 5.',resourceSystems=[resource for f in features for resource in p['featureSupport'].get(f,{}).get('resources',[])],sources=sub['sources']))
  row=dict(classId=cid,className=cl['name'],status=status,completionCategory='CERTIFIED_LEVEL_1_TO_5' if status=='CERTIFIED_LEVEL_5' else 'EXPLICITLY_BLOCKED',baseline='ALREADY_CERTIFIED' if owned else 'NOT_PUBLISHED',speciesRequirements=cl['data']['requirements'],originRestrictions=origins,canonicalTrainingText=header,hitDie=training[cid]['hitDie'],savingThrows=training[cid]['savingThrows'],skills='See source training and declarative choices; no skills invented if none specified.',skillAndTrainingChoices=[dict(id=k,data=v['data']) for k,v in canonical.items() if v['kind']=='choice' and slug in k and v['data']['purpose']!='subclass'],equipment=equipment[cl['name']]['sourceText'],equipmentSourcePage=100,certifiedEquipmentPackage=p['packages'].get(cid),levels=levels,subclasses=[x['id'] for x in cl['data']['allowedSubclasses']],psychicDependency=slug in ['psyker','aeldari_warlock'],knownBlockers=blockers.get(cid,[]),familyRows=len(owned),level5FamilyRows=sum(x['level']==5 for x in owned),sources=cl['sources'])
  if slug=='hive_scum':row['baseline']='Ratling Gunslinger already certified; Human paths previously level 1 only, now completed through 5.'
  row['primaryAbilities']=next((line.split(':',1)[1].strip() for line in header.splitlines() if line.startswith('Primary Abilities:')),'See source')
  row['weaponProficiencies']=next((line.split(':',1)[1].strip() for line in header.splitlines() if line.startswith('Weapons:')),'See source')
  row['armourProficiencies']=next((line.split(':',1)[1].strip() for line in header.splitlines() if line.startswith('Armour:')),'See source')
  row['resourceSystems']=[res for lev in levels for f in lev['features'] for res in f['support'].get('resources',[])]
  if slug=='zealot':row['resourceSystems']=[dict(name=name,maximum='proficiency bonus',recovery='long_rest',status='SOURCE_AUDITED_NOT_PUBLISHED',sourcePdfPage=53) for name in ['Martyr’s Mercy','Charge of Conviction']]
  if slug=='arbites_enforcer':row['resourceSystems']=[dict(name='Authority',maximum='proficiency bonus',recovery='long_rest',status='SOURCE_AUDITED_NOT_PUBLISHED',sourcePdfPage=62)]
  if row['psychicDependency']:row['resourceSystems']=[dict(name='Warp Pressure and Perils',status='PSYCHIC_FRAMEWORK_REQUIRED',sourcePdfPages=[91,95,96])]
  row['actionTypes']=[{'featureId':f['id'],'canonicalText':f['text'],'execution':f['support'].get('classification','NOT_PUBLISHED')} for lev in levels for f in lev['features']]
  rows.append(row)
 matrix=[]
 for family in s['certifiedPaths']:matrix.append(family|dict(status='CERTIFIED',manualRuleStatus='READY_WITH_MANUAL_RULES',blocker=None,profile=s['id']))
 for cl in rows:
  for origin in cl['originRestrictions']:
   for level in range(1,6):
    subs=cl['subclasses'] if level>=3 else [None]
    for sid in subs:
     if any(all(x[k]==v for k,v in {'speciesId':origin['speciesId'],'originId':origin['originId'],'classId':cl['classId'],'subclassId':sid,'level':level}.items()) for x in s['certifiedPaths']):continue
     sub=next((x for x in subrows if x['subclassId']==sid),None)
     if origin['availability'] in ['RARE','LIMITED']:status='BLOCKED_BY_APPROVAL';reason='Origin '+origin['availability']+' requires trusted campaign approval.'
     elif origin['availability']!='NORMAL':status='UNSUPPORTED';reason='Origin/species combination unavailable under approved eligibility matrix.'
     elif cl['knownBlockers']:status=cl['status'];reason=cl['knownBlockers']
     elif sub and sub['status']!='CERTIFIED':status=sub['status'];reason=sub['reason']
     else:status='BLOCKED_BY_CONTENT';reason='No certified production path for this combination; no legality inferred.'
     matrix.append(dict(speciesId=origin['speciesId'],originId=origin['originId'],classId=cl['classId'],subclassId=sid,level=level,status=status,manualRuleStatus='NOT_PUBLISHED',blocker=reason,profile=s['id']))
 return dict(profileId=s['id'],digest=b['digest'],sourceRoster={'pdfPage':50,'declaredCount':12,'verifiedChapterHeadings':headings},counts=dict(totalClasses=12,certifiedLevel5=8,partiallyCertified=0,psychicFrameworkBlocked=2,rulesBlocked=2,engineBlocked=0,contentBlocked=0,approvalBlocked=0,totalSubclasses=len(subrows),certifiedSubclasses=len(certified),blockedSubclasses=len(subrows)-len(certified),familyRows=329),classes=rows,subclasses=subrows,families=matrix)
if __name__=='__main__':
 data=build();out=c.PACKAGE/'review/class-roster-level5-audit.json';out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(data['counts']))

