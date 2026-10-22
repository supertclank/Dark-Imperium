"""Offline PHB conformance functions, not an application rules engine.

Inputs such as ability modifiers must already be resolved. Unknown policy never
falls back to another game. See docs/content/CALCULATION_POLICIES.md.
"""
from content_import import InvalidContent, require, integer

def compare(a, op, b):
    require(op in ('eq','lt','lte','gt','gte'), 'COMPARISON')
    return {'eq':a==b,'lt':a<b,'lte':a<=b,'gt':a>b,'gte':a>=b}[op]

def evaluate(p, snapshot):
    """Three-valued prerequisites; snapshot is pre-grant and may be incomplete."""
    k=p['kind']
    if k in ('all','any'):
        values=[evaluate(x,snapshot) for x in p['predicates']]
        if k=='all': return False if False in values else (None if None in values else True)
        return True if True in values else (None if None in values else False)
    if k=='not':
        v=evaluate(p['predicate'],snapshot);return None if v is None else not v
    if k in ('selected','proficient'):
        field,ref=('selected','content') if k=='selected' else ('proficiencies','proficiency')
        return None if field not in snapshot else p[ref]['id'] in snapshot[field]
    if k=='fact':return None if p['key'] not in snapshot.get('facts',{}) else snapshot['facts'][p['key']]==p['equals']
    if k=='stat':v=snapshot.get('stats',{}).get(p['key'])
    elif k=='level':
        a=p['axis'];v=snapshot.get('totalLevel') if a['kind']=='total_level' else snapshot.get('classLevels',{}).get(a['class']['id'])
    elif k=='health_ratio':
        h=snapshot.get('health',{}).get(p['scope'])
        if h is None or h['maximum']<=0:return None
        return compare(h['current']*p['denominator'],p['operator'],h['maximum']*p['numerator'])
    elif k=='equipped':
        if 'equipped' not in snapshot:return None
        return any(all((i.get('kind')==p['itemKind'] if key=='itemKind' else
                        p['property']['id'] in i.get('properties',[]) if key=='property' else
                        p['slot'] in i.get('slots',[])) for key in p if key!='kind') for i in snapshot['equipped'])
    elif k=='tagged':
        tags=snapshot.get('tags',{}).get(p['scope']);return None if tags is None else p['tag']['id'] in tags
    else:raise InvalidContent('UNSUPPORTED_PREDICATE')
    return None if v is None else compare(v,p['operator'],p['value'])

def proficiency(level):
    integer(level,1,20)
    return next(b for upper,b in [(4,2),(8,3),(12,4),(16,5),(20,6)] if level<=upper)

def check_modifier(ability_modifier, level, proficient):
    require(type(proficient) is bool,'PROFICIENCY_UNRESOLVED')
    integer(ability_modifier,-1000000,1000000)
    return ability_modifier+(proficiency(level) if proficient else 0)

def hp_gain(hit_die, constitution_modifier, first=False, roll=None):
    require(hit_die in (6,8,10,12),'HIT_DIE')
    integer(constitution_modifier,-1000000,1000000)
    if roll is not None:integer(roll,1,hit_die)
    return (hit_die if first else (roll if roll is not None else {6:4,8:5,10:6,12:7}[hit_die]))+constitution_modifier

def advantage(has_advantage, has_disadvantage):
    require(type(has_advantage) is bool and type(has_disadvantage) is bool,'ADVANTAGE_UNRESOLVED')
    return 'normal' if has_advantage==has_disadvantage else ('advantage' if has_advantage else 'disadvantage')

def critical_dice(components):
    """Only ordinary attack damage; property extra dice are separate afterwards."""
    import copy
    out=copy.deepcopy(components)
    for c in out:
        if 'dice' in c:
            c['dice']['count']*=2
            integer(c['dice']['count'],1,100)
    return out

def hull_damage(post_mitigation_components, dt, armour_breaking=False):
    integer(dt,0,1000000)
    require(type(armour_breaking) is bool,'ARMOUR_BREAKING_UNRESOLVED')
    for value in post_mitigation_components:integer(value,0,1000000)
    total=sum(post_mitigation_components);threshold=dt//2 if armour_breaking else dt
    return total if total>=threshold else 0

def pressure_after_power(current, tier, empowered=False):
    integer(current,0,1000000);require(tier in ('minor','standard','major'),'POWER_TIER')
    require(type(empowered) is bool,'EMPOWER_UNRESOLVED')
    return current+{'minor':1,'standard':2,'major':3}[tier]+int(empowered)

def perils_trigger(face, pressure):
    integer(face,1,20);integer(pressure,0,1000000);return face<=pressure

def severity_band(face, pressure):
    require(perils_trigger(1,pressure),'NO_PERILS_AT_ZERO')
    integer(face,1,20);total=face+pressure
    return next(name for upper,name in [(6,'warp_static'),(10,'bleeding_eyes'),(14,'soul_echo'),(18,'warp_scream'),(22,'possession_pressure'),(26,'uncontrolled_manifestation'),(30,'reality_tear'),(1000020,'catastrophic_perils')] if total<=upper)

def armour_ac(base, dexterity_modifier, dexterity_cap=None):
    """Only source expressions that explicitly say base + Dex, max N."""
    integer(base,0,1000000);integer(dexterity_modifier,-1000000,1000000)
    if dexterity_cap is not None:integer(dexterity_cap,0,1000000)
    return base+(min(dexterity_modifier,dexterity_cap) if dexterity_cap is not None else dexterity_modifier)

def unsupported(policy):
    raise InvalidContent('HUMAN_RULING_REQUIRED: '+policy)

def topological_order(dependencies):
    result=[];active=set();done=set()
    def visit(key):
        require(key in dependencies,'DEPENDENCY_NOT_FOUND')
        require(key not in active,'CALCULATION_CYCLE')
        if key in done:return
        active.add(key)
        for dep in dependencies[key]:visit(dep)
        active.remove(key);done.add(key);result.append(key)
    for key in dependencies:visit(key)
    return result
