"""Reviewed PHB psychic catalogue. No Major powers are published by this module."""
import re
import content_import as c

MINOR='warp_spark kinetic_push mind_lumen static_veil flesh_knit pain_spike ember_flicker ashen_brand danger_sense echo_read whisper_from_below warp_bite null_glare blank_sense conceal reveal'.split()
STANDARD='focused_rupture assail psychic_shield soulfire dominate_nerve warp_step blood_surge toxic_bloom kinetic_bulwark crush_grip fates_nudge prescient_aim cleansing_wave burning_halo terror_echo baleful_rupture null_field silence_the_witch protect jinx quicken restrain_fate'.split()
# Dice contracts represent the base effect, never an inferred target hit/save outcome.
DICE={
 'warp_spark':(1,8,'damage','force',0,0), 'kinetic_push':(1,6,'damage','force',0,0),
 'flesh_knit':(1,6,'healing',None,1,0), 'pain_spike':(1,8,'damage','psychic',0,0),
 'ashen_brand':(1,8,'damage','fire/radiant',0,0), 'danger_sense':(1,4,'bonus',None,0,0),
 'warp_bite':(1,10,'damage','psychic',0,0), 'focused_rupture':(3,8,'damage','force',0,0),
 'assail':(1,6,'damage','force',0,0), 'psychic_shield':(1,8,'temporary_hp',None,1,1),
 'soulfire':(2,6,'damage','fire/radiant',0,0), 'toxic_bloom':(2,8,'damage','poison/necrotic',0,0),
 'kinetic_bulwark':(2,8,'protection',None,1,0), 'crush_grip':(2,8,'damage','force',0,0),
 'fates_nudge':(1,4,'bonus',None,0,0), 'cleansing_wave':(3,6,'damage','fire/radiant',0,0),
 'terror_echo':(2,6,'damage','psychic',0,0), 'baleful_rupture':(4,8,'damage','psychic',0,0),
 'silence_the_witch':(1,4,'bonus',None,0,0), 'restrain_fate':(1,4,'bonus',None,0,0),
}
OPTIONS={
 'overcharged_damage':'If the power deals damage, add one damage die of the same type.',
 'brutal_manifestation':'If the power requires a saving throw, increase its save DC by 1 for this casting.',
 'extended_reach':'Increase range by 30 ft, or cone/area radius by 5 ft.',
 'sustained_focus':'Increase temporary HP, healing, protection, or a bonus by proficiency bonus.',
 'split_manifestation':'One additional creature within 10 ft of the original target receives half the damage/non-damage effect; GM adjudication.',
 'discipline_mastery':'Chosen-discipline power: reroll one damage or healing die.',
}
def build():
 powers=[]
 for slug in MINOR+STANDARD:
  candidate=c.read(c.PACKAGE/f'review/candidates/power/{slug}.json');e=candidate['evidence'][0];text=e['text'];description=text.split('Rule: ',1)[1]
  tags=text.split('Tag: ',1)[1].split(';')[0].split(', ')
  save=next((a.lower() for a in ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma'] if re.search(a+r' (?:saving throw|save)',description)),None)
  power=dict(id=candidate['proposedId'],name=candidate['name'],tier='minor' if slug in MINOR else 'standard',tags=tags,actionType='bonus_action' if description.startswith('Bonus Action') else 'reaction' if description.startswith('Reaction') else 'action',range=re.search(r'(?:Range:? |within )(\d+) ft',description).group(1)+' ft' if re.search(r'(?:Range:? |within )(\d+) ft',description) else 'Touch' if 'Touch' in description else 'Self' if 'Self' in description else 'See canonical description',attack='Psychic attack' in description,save=save,description=description,sources=[e['source']],warpPressureCost=1 if slug in MINOR else 2,extraWarpPressure=1 if slug=='baleful_rupture' else 0,automationStatus='PARTIAL',manualNote='Target selection, hit/save outcome, conditions, duration, and split damage-type adjudication remain manual. Base rolls and Warp Pressure are server-authorised.',empoweredOptions=[])
  if slug in DICE:
   count,sides,kind,damage,ability,pb=DICE[slug];power['roll']=dict(count=count,sides=sides,kind=kind,damageType=damage,abilityMultiplier=ability,proficiencyMultiplier=pb)
  eligible=[]
  if slug in DICE and DICE[slug][2]=='damage':eligible.append('overcharged_damage')
  if save:eligible.append('brutal_manifestation')
  if power['range'] not in ['Self','Touch','See canonical description'] or 'cone' in description or 'radius' in description:eligible.append('extended_reach')
  if (slug in DICE and DICE[slug][2] in ['healing','temporary_hp','protection','bonus']) or slug in ['static_veil','blood_surge','prescient_aim','conceal','protect','quicken']:eligible.append('sustained_focus')
  if slug in ['warp_spark','kinetic_push','flesh_knit','pain_spike','ashen_brand','whisper_from_below','warp_bite','null_glare','reveal','focused_rupture','psychic_shield','soulfire','dominate_nerve','blood_surge','crush_grip','prescient_aim','terror_echo','baleful_rupture','conceal','protect','jinx','quicken']:eligible.append('split_manifestation')
  if slug in DICE and DICE[slug][2] in ['damage','healing']:eligible.append('discipline_mastery')
  power['empoweredOptions']=eligible
  if slug=='warp_step':power['rulePending']={'id':'PHB-RULE-038','text':'The extra immediate Perils instruction requires GM adjudication; the normal post-power check still applies.'}
  powers.append(power)
 page95=next(p["text"] for p in c.read(c.PACKAGE/"evidence/pages.json") if p["pdfPage"]==95)
 effects={name:re.search(r"15\.4\.\d+ "+re.escape(name)+r"\s+(.*?)(?=15\.4\.\d+|15\.5)",page95,re.S).group(1).strip() for name in ["Warp Static","Bleeding Eyes","Soul Echo","Warp Scream","Possession Pressure","Uncontrolled Manifestation","Reality Tear","Catastrophic Perils"]}
 return dict(schemaVersion=1,classes=['di.class.psyker','di.class.aeldari_warlock'],abilityChoiceId='di.choice.psychic.ability',knownByLevel={str(n):dict(minor=m,standard=s,major=0) for n,m,s in [(1,2,2),(2,2,3),(3,3,3),(4,3,4),(5,3,4)]},disciplineTags=dict(biomancer='Biomancy',telekine='Telekinesis',diviner='Divination',pyromancer='Pyromancy',malefic_touched='Malefic',blank_null_bound='Null'),powers=powers,empoweredOptions=[dict(id=k,name=k.replace('_',' ').title(),description=v) for k,v in OPTIONS.items()],pressureMinimum=0,afterPerils='floor_half_after_effect',approvalSource='review/approved-warp-pressure-2026-10-24.md',perilsBands=[dict(minimum=a,maximum=b,name=n,description=effects[n]) for a,b,n in [(2,6,'Warp Static'),(7,10,'Bleeding Eyes'),(11,14,'Soul Echo'),(15,18,'Warp Scream'),(19,22,'Possession Pressure'),(23,26,'Uncontrolled Manifestation'),(27,30,'Reality Tear'),(31,None,'Catastrophic Perils')]])
