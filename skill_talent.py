import json
import typing
import importlib.resources

with importlib.resources.open_text('data_4th','skills.json') as f:
    _skills_data = json.load(f)

with importlib.resources.open_text('data_4th','talents.json') as f:
    _talents_data = json.load(f)

def associate(skills : dict, talents : dict, starting_index=1)  -> typing.Tuple[dict, dict, int]:
    if not skills or not talents:
        return skills, talents, starting_index
    class talents_data:
        def __init__(self):
            self._talents = dict(_talents_data)

        def __getitem__(self,key):
            realkey = key.split('(')[0].strip()

            if realkey[0]=='*': realkey = realkey[1:-1]

            return self._talents[realkey]       

    t4 = talents_data()

    # Grouped skills remain a nightmare!
    # Here we create a dictionary that maps from both long and shorts skill names to the full name
    # e.g. if the skill 'Ride (Horse)' is in the skills list the dictionary will contain the items
    #      {'Ride': 'Ride (Horse)', 'Ride (Horse)':'Ride'}
    skills_short_to_long = {}
    for skill in skills:
        unspecialised = skill.split('(')[0].strip()     # Word before '('
        if unspecialised[0]=='*': unspecialised[1:-1]   # Strip off stars in e.g. *Savvy*, as used by starting talents

        if unspecialised in skills_short_to_long:
            skills_short_to_long[unspecialised].update([skill])
        else:
            skills_short_to_long[unspecialised] = set([skill])

        skills_short_to_long[skill] = set([skill])

    # So many loops!
    # Loop through all the talents in the talents list and find their associated skills
    # In the case of general skills these may be associated with a specified version, e.g. 'Ride (Horse)'
    # or with all version, e.g. 'Ride'. For this reason we check if the skill is in the 
    # skills_short to long that we geenrated above. If it is then we have one more loop
    # since we have to handle the case of multiple options, e.g. 'Language' talents might 
    # need to be applied to 'Language (Magic)', 'Langauge (Battle)', etc.
    index = starting_index
    for talent in talents:
        for short_skill in t4[talent]['tests']:
            if short_skill in skills_short_to_long:
                for skill in skills_short_to_long[short_skill]:
                    thisindex = index

                    if 'skill_ref' in talents[talent]: thisindex = talents[talent]['skill_ref']
                    else: talents[talent]['skill_ref'] = index

                    for idx in range(len(skills[skill])):
                        if 'talent_ref' in skills[skill][idx]: 
                            skills[skill][idx]['talent_ref'].update({thisindex})
                        else: 
                            skills[skill][idx]['talent_ref'] = set({thisindex})

                    if thisindex == index:
                        index += 1

    return skills, talents, index