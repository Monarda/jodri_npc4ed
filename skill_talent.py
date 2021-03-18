import json
import typing

with open('data_4th/skills.json') as f:
    _skills_data = json.load(f)

with open('data_4th/talents.json') as f:
    _talents_data = json.load(f)

def associate(skills : dict, talents : dict, starting_index=1)  -> typing.Tuple[dict, dict, int]:
    if not skills or not talents:
        return skills, talents, starting_index

    class skills_data:
        def __init__(self):
            self._skills = dict(_skills_data)

        def __getitem__(self,key):
            realkey = key.split('(')[0].strip()

            return self._skills[realkey]

    class talents_data:
        def __init__(self):
            self._talents = dict(_talents_data)

        def __getitem__(self,key):
            realkey = key.split('(')[0].strip()

            return self._talents[realkey]       

    t4 = talents_data()
    s4 = skills_data()

    index = starting_index
    for talent in talents:
        for skill in t4[talent]['tests']:
            if skill in skills:
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