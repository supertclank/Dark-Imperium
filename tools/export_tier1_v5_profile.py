"""Source-backed v5 overlay. Earlier profile bytes are never regenerated or rewritten."""
import copy,itertools,sys
import content_import as c
import tier1_catalogue as audit
CHOICE='di.choice.veteran.level4_improvement'
MANUAL={
 'rapid_reload':'Reload timing is manual; no inventory/ammunition automation.',
 'hip_fire':'Conditional bonus-action permission; resolve the qualifying movement manually.',
 'close_quarters_killer':'Contextual disadvantage exception is manually applied.',
 'heavy_weapon_training':'Contextual movement penalty exception is manual.',
 'iron_discipline':'Source-specific fear benefit; no global condition or stacking policy.',
 'combat_medic':'Healing targets and uses are manually tracked; new resource has explicit full initial uses.',
 'brawler':'Hand-dependent unarmed damage remains manual; no baseline weapon changes.',
 'point_blank_execution':'Conditional extra die is manual, with one short-rest use.',
 'field_armourer':'Source explicitly leaves the repair/restoration to the GM.',
 'bayonet_fighter':'Conditional basic-firearm melee mode is manual; no invented proficiency or attack formula.',
 'breacher':'Object/terrain benefits are contextual and manual.',
 'crisis_runner':'Conditional Dash terrain exception is manual.',
 'tactical_reposition':'Conditional ally movement is manual.',
 'armour_familiarity':'Incoming conditional reduction is manual; no automated target damage.',
 'relic_bearer':'Manual saving-throw die and source flavour item; one long-rest use.',
 'hive_blooded':'Structured Human-or-Ratling requirement; contextual navigation advantage is manual.',
 'weapon_specialist':'Source-listed weapon-group choice; standalone +1 weapon damage is calculated. Ambiguous combined stacking remains manual (PHB-RULE-058).',
 'cybernetic_implant':'Exactly one selection from the already approved PHB-RULE-051 minor-augmetic pool; item benefits remain manual.'}
BLOCKED={
 'grenadier':('BLOCKED_BY_ENGINE','Grenade range/DC changes require a separate action-mode certification; not published as an incorrect baseline.'),
 'suppressive_discipline':('BLOCKED_BY_RULE','PHB-RULE-022: the mandatory Suppression DC procedure remains unresolved.'),
 'dead_calm':('BLOCKED_BY_RULE','PHB-RULE-022/046: condition-specific disadvantage exceptions not certified in this slice.')}
def eligible(p,selected):
 if not p:return True
 if p['kind']=='selected':return p['content']['id'] in selected
 if p['kind']=='all':return all(eligible(x,selected) for x in p['predicates'])
 if p['kind']=='any':return any(eligible(x,selected) for x in p['predicates'])
 return False

def build():
 old=c.read(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v4.json');p=copy.deepcopy(old['payload']);s=p['spec'];r=p['records']
 for n in (14,15,16):assert audit.validate_approval(next(x for x in c.read(c.PACKAGE/'review/decisions.json')['humanRulings'] if x['id']==f'PHB-RULE-{n:03}'))
 s.update(id='di-phb-1.0-tier1-v5',name='PHB 1.0 · Human Veteran level 4',levels=[1,2,3,4],level4PolicyVersion=1)
 options=[];metadata=[];attrs=s['attributes']
 def option(key,label,branch,grants,**details):
  options.append(dict(id=key,label=label,grants=grants));metadata.append(dict(id=key,label=label,branch=branch,**details))
 for a in attrs:option('plus_two_'+a,a.title()+' +2','ASI_PLUS_TWO',[dict(id='increase',kind='attribute_increase',attributeKey=a,amount=2)],abilities=[a])
 for a,b in itertools.combinations(attrs,2):option('split_'+a+'_'+b,a.title()+' +1; '+b.title()+' +1','ASI_SPLIT',[dict(id='first',kind='attribute_increase',attributeKey=a,amount=1),dict(id='second',kind='attribute_increase',attributeKey=b,amount=1)],abilities=[a,b])
 readiness=[];selected={'di.species.human','di.class.veteran'}
 groups=['pistol','basic_firearm','sniper','shotgun','chain','shock','plasma','melta','heavy']
 for key,record in sorted(r.items()):
  if not key.startswith('di.feature.talent.'):continue
  short=key.split('.')[-1];req=record['data'].get('requirements');ok=eligible(req,selected)
  status,reason=('INELIGIBLE','Structured species/class requirements exclude Human Veteran.') if not ok else BLOCKED.get(short,('READY_WITH_MANUAL_RULES',MANUAL[short]) if short in MANUAL else ('BLOCKED_BY_CONTENT','Individual executable benefit review not complete.'))
  readiness.append(dict(id=key,name=record['name'],status=status,reason=reason,requirements=req,sources=record['sources'],benefit=record['descriptionMarkdown']))
  if status not in ['READY','READY_WITH_MANUAL_RULES']:continue
  p['featureSupport'][key]=dict(classification='PARTIAL' if short=='weapon_specialist' else 'MANUAL',playerNote=reason,rulingIds=['PHB-RULE-016']+(['PHB-RULE-058'] if short=='weapon_specialist' else []),resources=[])
  if short in ['combat_medic','point_blank_execution','relic_bearer']:
   p['featureSupport'][key]['resources']=[dict(key=short,maximum=2 if short=='combat_medic' else 1,recovery='short_rest' if short=='point_blank_execution' else 'long_rest',automation='manual')]
  grant=dict(id='talent',kind='feature',feature=dict(id=key))
  common=dict(talentId=key,requirement=record['descriptionMarkdown'].split('Requirement: ')[1].split('\n')[0] if 'Requirement: ' in record['descriptionMarkdown'] else 'General Talent',benefit=record['descriptionMarkdown'],classification=p['featureSupport'][key]['classification'],note=reason)
  if short=='weapon_specialist':
   for g in groups:option(short+'_'+g,record['name']+' — '+g.replace('_',' '),'TALENT',[grant],subchoiceId=g,subchoiceLabel=g.replace('_',' '),**common)
  elif short=='cybernetic_implant':
   for o in r['di.choice.starting.minor_augmetic']['data']['options']:
    aug=o['grants'][0]['content']['id'];option(short+'_'+o['id'],record['name']+' — '+o['label'],'TALENT',[grant],subchoiceId=aug,subchoiceLabel=o['label'],subchoiceText=r[aug]['descriptionMarkdown'],**common)
  else:option(short,record['name'],'TALENT',[grant],**common)
 template=copy.deepcopy(r['di.choice.human.ability_scores']);template.update(id=CHOICE,name='Ability Score Improvement / Talent',summary='Approved level-four advancement',descriptionMarkdown='Choose +2 to one ability, +1 to two different abilities, or one eligible Talent. ASI increases cannot exceed 20.',sources=copy.deepcopy(r['di.feature.class.veteran.level_4.ability_score_improvement_talent']['sources']))
 template['data'].update(purpose='feature',options=options);r[CHOICE]=template
 f=r['di.feature.class.veteran.level_4.ability_score_improvement_talent'];f['data']['grants']=[dict(id='improvement',kind='choice',choice=dict(id=CHOICE))];f['data']['manualRules']=[]
 p['featureSupport'][f['id']]=dict(classification='AUTOMATED',playerNote='One approved ASI or Talent selection.',rulingIds=['PHB-RULE-015','PHB-RULE-016'],resources=[])
 for cfg in list(s['pathConfigurations']):
  if cfg['speciesId']=='di.species.human' and cfg['classId']=='di.class.veteran' and cfg['level']==3:
   cfg=copy.deepcopy(cfg);cfg.update(level=4,choices=cfg['choices']+[CHOICE],features=cfg['features']+[f['id']]);s['pathConfigurations'].append(cfg)
 for family in list(s['certifiedPaths']):
  if family['speciesId']=='di.species.human' and family['classId']=='di.class.veteran' and family['level']==3:s['certifiedPaths'].append(dict(family,level=4))
 s['choices'].append(CHOICE)
 s['level4Advancement']=dict(kind='ADVANCEMENT_CHOICE',key='ability_score_improvement_or_talent',choiceId=CHOICE,branches=['ASI_PLUS_TWO','ASI_SPLIT','TALENT'],options=metadata,asiMaximum=20,talentRepeatable=False,initialResourcePolicy='full_new_preserve_existing')
 s['upgradeContract']=dict(version='human-veteran-v4-v5-1',fromProfile=old['payload']['spec']['id'],fromDigest=old['digest'],toProfile=s['id'],fromLevel=3,toLevel=4,speciesId='di.species.human',classId='di.class.veteran',preserve=['choices','inventory','resources','currentHp','rollHistory'])
 s['availability'][0]['message']+=' Human Veterans may explicitly upgrade from v4 at level 3 for level-four ASI/Talent advancement.'
 p['level4TalentReadiness']=readiness
 c.validate_records(r)
 return dict(digest=c.digest(p),payload=p)
if __name__=='__main__':
 b=build()
 for path,value in [(c.ROOT/'backend/src/main/resources/profiles/di-phb-1.0-tier1-v5.json',b),(c.ROOT/'content/profiles/di-phb-1.0-tier1-v5.json',b['payload']['spec'])]:
  raw=c.canonical(value)+b'\n'
  if path.exists():assert path.read_bytes()==raw,'Immutable release differs: '+str(path)
  elif '--check' not in sys.argv:path.write_bytes(raw)
  else:raise AssertionError('Missing release '+str(path))
 rows=b['payload']['level4TalentReadiness'];report='# Level-4 Talent readiness\n\nScope: Human Veteran. All '+str(len(rows))+' Chapter 12 Talent records reviewed individually. INELIGIBLE is specific to this publication scope; non-Human advancement is not published. Universal Traits are separate from Talent ownership.\n\n'
 for row in rows:report+='## '+row['name']+'\n\n`'+row['id']+'` — **'+row['status']+'**\n\n'+row['benefit']+'\n\n'+row['reason']+'\n\nSource: '+str(row['sources'][0]['locator'])+'\n\n'
 (c.ROOT/'docs/import/LEVEL4_TALENT_READINESS.md').write_text(report,encoding='utf8')
 print(b['digest'],len([x for x in rows if x['status'].startswith('READY')]),'published Talents; level-4 families',sum(x['level']==4 for x in b['payload']['spec']['certifiedPaths']))
