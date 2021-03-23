import json
import importlib.resources

with importlib.resources.open_text('data','careers.json') as f:
    _careers_data = json.load(f)

class Careers4:
    # Load data about careers, talents and skills
    def __init__(self):
        self._skills_to_careers = {}
        self._talents_to_careers = {}

        self._careers_by_class = dict()
        self._careers_by_earning_skill = dict()
        
        self._skills = set()
        self._talents = set()

        for careername in _careers_data:
            earning_skill = _careers_data[careername]['earning skill']
            if earning_skill in self._careers_by_earning_skill:
                self._careers_by_earning_skill[earning_skill].append(careername)
            else:
                self._careers_by_earning_skill[earning_skill] = [careername]

            for rank in range(1,5):
                rankname = _careers_data[careername]['rank {}'.format(rank)]["name"]

                # Careers which provide this skill
                skills = _careers_data[careername]['rank {}'.format(rank)]['skills']
                self._skills.update(skills)
                for skill in skills:
                    value = {"careername":careername, "rank":rank, "rankname":rankname}

                    if skill in self._skills_to_careers:
                        self._skills_to_careers[skill].append( value)
                    else:
                        self._skills_to_careers[skill] = [value]

                # Careers which provide this talent
                talents = _careers_data[careername]['rank {}'.format(rank)]['talents']
                self._talents.update(talents)
                for talent in talents:
                    value = {"careername":careername, "rank":rank, "rankname":rankname}

                    if talent in self._talents_to_careers:
                        self._talents_to_careers[talent].append( value)
                    else:
                        self._talents_to_careers[talent] = [value]

                # Careers by class
                classname = _careers_data[careername]['class']
                if classname in self._careers_by_class:
                    self._careers_by_class[classname].update([careername])
                else:
                    self._careers_by_class[classname] = set([careername])

    @property
    def careers(self):
        return _careers_data.keys()

    @property
    def career_levels(self):
        career_levels = []
        for career in self.careers:
            for i in range (1,5):
                career_levels.append(self[career][f'rank {i}']['name'])

        return career_levels

    def __getitem__(self, key):
        return _careers_data[key]

    def provides_skills(self):
        return self._skills_to_careers

    def provides_skill(self, skill):
        return self._skills_to_careers[skill]



def main():
    c4 = Careers4()

    print(c4.provides_skill('Sail (Any)'))
    print(c4._talents_to_careers['Sprinter'])
    print(len(c4.list_careers()), sorted(c4.list_careers()))

    for skill in sorted(c4._careers_by_earning_skill.keys()):
        print('{:20s}: {}'.format(skill, ', '.join(c4._careers_by_earning_skill[skill])))

if __name__ == "__main__":
    # execute only if run as a script
    main()