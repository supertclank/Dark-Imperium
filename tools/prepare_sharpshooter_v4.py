"""Review-only Sharpshooter preparation; no canonical content mutation."""
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'tools/content_import.py').exists():ROOT=Path(r'C:/Users/tgccl/OneDrive/Documents/localdev/Dark-Imperium')
sys.path.insert(0,str(ROOT/'tools'))
import content_import as c
from export_tier1_v2_profile import package

def build():
    pages={p['pdfPage']:p['text'] for p in c.read(c.PACKAGE/'evidence/pages.json')}
    assert 'Tools: Cook’s utensils or thieves’ tools.' in pages[68]
    assert 'Long-las or lasgun; stub pistol or laspistol; knife; heavy clothing or flak armour; camo cloak;' in pages[100]
    def source(page,section,heading):
        return {'sourceId':'di.source.phb','sourceVersion':'1.0@a58335b1264a','locator':{'pdfPage':page,'printedPage':page-13,'sectionKey':section,'heading':heading}}
    kit=package([('di.weapon.knife',1),('di.equipment.camo_cloak',1)],[
        ('primary',['di.weapon.long_las','di.weapon.lasgun']),
        ('pistol',['di.weapon.stub_pistol','di.weapon.laspistol']),
        ('armour',['di.armour.heavy_clothing','di.armour.flak_armour']),
        ('tools',['di.tool.cooks_utensils','di.tool.thieves_tools'])],
        ['di.armour.heavy_clothing','di.armour.flak_armour'],source(100,'17.1','Ratling Sharpshooter starting equipment'))
    candidates=[]
    for relative in ['weapon/long_las.json','armour/heavy_clothing.json']:
        path=c.PACKAGE/'review/candidates'/relative
        raw=path.read_bytes();candidate=json.loads(raw)
        candidates.append({'path':path.relative_to(c.PACKAGE).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'proposedId':candidate['proposedId'],'proposedData':candidate['proposedData'],'evidence':candidate['evidence']})
    training={'source':source(68,'11.7','Ratling Sharpshooter training'),'hitDie':8,'savingThrows':['dexterity','wisdom'],'armourLabels':['Light armour','Flak armour'],
        'weaponGroups':['pistol','shotgun','sniper'],'individualWeapons':['di.weapon.knife','di.weapon.lasgun','di.weapon.long_las'],
        'toolChoice':{'id':'di.choice.ratling_sharpshooter.training_tool','min':1,'max':1,'options':[
            {'id':'cooks_utensils','proficiencyId':'di.proficiency.tool.cooks_utensils','toolId':'di.tool.cooks_utensils'},
            {'id':'thieves_tools','proficiencyId':'di.proficiency.tool.thieves_tools','toolId':'di.tool.thieves_tools'}]},
        'note':'Training and package possession are independent source choices. No rule requiring matching answers is supplied. Specific knife/lasgun/long-las training must not grant entire simple-melee/basic-firearm groups.'}
    return {'schemaVersion':1,'status':'PREPARATION_ONLY_NOT_PUBLISHED','classId':'di.class.ratling_sharpshooter','level':1,
        'trainingProposal':training,'packageProposal':kit,'preservedCandidates':candidates,
        'itemProposals':[
            {'id':'di.tool.cooks_utensils','kind':'tool','name':"Cook’s utensils",'source':source(100,'17.1','Ratling Sharpshooter equipment'),'functionalTags':['tool'],'automaticBonuses':[]},
            {'id':'di.tool.thieves_tools','kind':'tool','name':"Thieves’ tools",'source':source(100,'17.1','Ratling Sharpshooter equipment'),'functionalTags':['tool'],'automaticBonuses':[]}],
        'equipmentReview':[
            {'id':'di.weapon.long_las','sourcePages':[35,37,68,100],'damage':'1d10 radiant','rangeFeet':[150,600],'properties':{'accurate':True,'reload':10},'hands':2,'handsBasis':'Existing approved weapon_hands sniper policy','automation':'Baseline attack/damage only. Accurate conditional +1 and reload lifecycle remain manual.'},
            {'id':'di.armour.heavy_clothing','sourcePages':[42,100],'baseAC':11,'dexterityBonus':{'enabled':True},'automation':'No Dexterity cap in source.'},
            {'id':'di.equipment.camo_cloak','sourcePages':[100],'automation':'Canonical manual utility under PHB-RULE-051; no numerical bonus.'}],
        'featureReview':[
            {'id':'di.feature.class.ratling_sharpshooter.level_1.small_target','classification':'MANUAL','sourcePages':[68],'note':'Conditional light-to-heavy cover and extra -2 versus ranged attacks while prone. No baseline AC bonus; do not stack duplicated Species/Class cover benefits.','rulingIds':['PHB-RULE-046','PHB-RULE-058']},
            {'id':'di.feature.class.ratling_sharpshooter.level_1.deadeye','classification':'MANUAL','sourcePages':[68],'note':'Once per turn +1d6 on ranged hit made with advantage; excluded from baseline damage.','rulingIds':[]},
            {'id':'di.feature.subclass.ratling_sharpshooter.underhive_rat.level_3','classification':'BLOCKED','sourcePages':[68],'rulingIds':['PHB-RULE-011'],'note':'Expertise is a level-3 dependency, not a level-1 blocker.'}],
        'publicationBlockers':[
            {'id':'SHARP-TRAINING','kind':'IMPLEMENTATION','detail':'Add specific training grants and required persisted tool proficiency choice. Tool proficiency needs schema and adapter support.'},
            {'id':'SHARP-TOOLS','kind':'CONTENT','detail':'Canonical cook’s utensils and thieves’ tools items/proficiencies need promotion. IDs here are proposals, not selectable content.'},
            {'id':'SHARP-EQUIPMENT','kind':'CONTENT','detail':'Long-las and Heavy Clothing remain candidates. Restricted Lasgun/Flak is source-valid but still needs mandatory tools and training. Preserve candidate bytes when promoting.'},
            {'id':'SHARP-CERTIFICATION','kind':'VALIDATION','detail':'Require full calculations, persistence, rolls, golden and browser acceptance before publication. This preparation certifies no family.'}]}

if __name__=='__main__':
    data=c.canonical(build())+b'\n'
    output=Path(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1]!='--check' else c.PACKAGE/'review/starting-packages/ratling_sharpshooter-prepared.json'
    if '--check' in sys.argv:assert output.read_bytes()==data,'Sharpshooter preparation differs'
    else:output.write_bytes(data)
    print('Sharpshooter preparation verified; no production publication')
