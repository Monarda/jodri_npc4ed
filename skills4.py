import json
import random
from typing import OrderedDict

with open('data_4th/skills.json') as f:
    _skills_data = json.load(f)

class Skills4:
    def __init__(self):
        self._combat_skills  = set()
        self._social_skills  = set()
        self._utility_skills = set()

        for skill in _skills_data:
            if _skills_data[skill]['combat']: self._combat_skills.update([skill])
            if _skills_data[skill]['social']: self._social_skills.update([skill])
            if _skills_data[skill]['utility']: self._utility_skills.update([skill])

    def filter(self, skilldict, type : str, noextra=False) -> set:
        if not type: return skilldict

        skilllist = skilldict.keys()
        skilllist = [x.split('(')[0].strip() for x in skilllist]
        if 'Language (Battle)' in skilldict:
            skilllist.append('Language (Battle)')

        combat_skills  = set(skilllist).intersection(self._combat_skills)
        social_skills  = set(skilllist).intersection(self._social_skills)
        utility_skills = set(skilllist).intersection(self._utility_skills)

        if type == 'combat':
            output = combat_skills
        elif type == 'social':
            output = social_skills
        elif type == 'utility':
            output = utility_skills
        else:
            raise TypeError(f'Invalid skill filter {type}')

        if noextra:
            return output
        
        if type != 'combat':
            skill_choices = combat_skills - output
            if skill_choices: output.update((random.choice(list(skill_choices)),))
        
        if type != 'social':
            skill_choices = social_skills - output
            if skill_choices: output.update((random.choice(list(skill_choices)),))
        
        if type != 'utility':
            skill_choices = utility_skills - output
            if skill_choices: output.update((random.choice(list(skill_choices)),))

        # Slightly complex bit of logic here. We're doing two things
        # First we're making sure we have all the instances of group skills
        # BUT we're only allowing through one example if it's not of the desired type
        newskilllist = []
        for shortskill in output:
            for skill in skilldict.keys():
                if skill.startswith(shortskill):
                    newskilllist.append(skill)
                    if not _skills_data[shortskill][type]: 
                        break

        newskilllist = sorted(newskilllist)
        return OrderedDict({key: skilldict[key] for key in newskilllist})
