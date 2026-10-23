"""Regenerate the 4,140 historical family slots; report level-four families separately.
The original inventory remains a historical artifact; no transitions count as families.
"""
from collections import Counter
import content_import as c
import tier1_catalogue as historical
from export_tier1_v6_profile import build

def matrix():
 b=build();p=b['payload'];s=p['spec'];old=historical.build();rows=old['rows']
 keys={(x['speciesId'],x['originId'],x['classId'],x['level'],x['subclassId']) for x in s['certifiedPaths']}
 blocked={x['id']:x for x in p['nonhumanAdvancementAudit']['subclasses'] if not x['status'].startswith('READY')}
 for row in rows:
  key=(row['species'],row['origin'],row['class'],row['level'],row['subclass'])
  row['productionAllowed']=key in keys
  if key in keys:row.update(status='READY_WITH_MANUAL_RULES',gapIds=[],rulingIds=[])
  elif row['status'] not in ['UNSUPPORTED','BLOCKED_BY_APPROVAL'] and row['subclass'] in blocked:
   why=blocked[row['subclass']];row.update(status=why['status'],reason=why['reason'],rulingIds=['PHB-RULE-011'] if 'PHB-RULE-011' in why['reason'] else ['PHB-RULE-046'] if 'PHB-RULE-046' in why['reason'] else [])
 counts={x:0 for x in ['READY','READY_WITH_MANUAL_RULES','BLOCKED_BY_CONTENT','BLOCKED_BY_ENGINE','BLOCKED_BY_RULING','BLOCKED_BY_APPROVAL','UNSUPPORTED']};counts.update(Counter(x['status'] for x in rows))
 return dict(profileId=s['id'],digest=b['digest'],historicalSlotCount=len(rows),counts=counts,families=rows,level4Families=[x for x in s['certifiedPaths'] if x['level']==4],totalPublishedFamilies=len(s['certifiedPaths']),note='The existing 4,140 slots cover levels 1–3. Level-4 tuples are an explicit appendix, not advancement-transition counts.')
if __name__=='__main__':
 result=matrix();assert result['historicalSlotCount']==4140
 (c.PACKAGE/'review/nonhuman-v6-publication-matrix.json').write_bytes(c.canonical(result)+b'\n');print(result['counts'],len(result['level4Families']),'level-four families')
