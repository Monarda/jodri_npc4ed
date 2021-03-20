import collections
import json
import random
import importlib.resources

with importlib.resources.open_text('data_4th','talents.json') as f:
    _talents_data = json.load(f)

class Talents4:
    def __init__(self):
        self._combat_talents  = set()
        self._social_talents  = set()
        self._utility_talents = set()

        for talent in _talents_data:
            if _talents_data[talent]['combat']: self._combat_talents.update([talent])
            if _talents_data[talent]['social']: self._social_talents.update([talent])
            if _talents_data[talent]['utility']: self._utility_talents.update([talent])

    def get_talents(self):
        return list(_talents_data.keys())

    def __getitem__(self, key):
        return _talents_data[key]

    def filter(self, talentlist, type : str, noextra=False):
        if not type: return talentlist

        combat_talents  = set(talentlist).intersection(self._combat_talents)
        social_talents  = set(talentlist).intersection(self._social_talents)
        utility_talents = set(talentlist).intersection(self._utility_talents)

        if type == 'combat':
            output = combat_talents
        elif type == 'social':
            output = social_talents
        elif type == 'utility':
            output = utility_talents
        else:
            raise TypeError(f'Invalid talent filter {type}')

        if noextra:
            return output
        
        if type != 'combat':
            talent_choices = combat_talents - output
            if talent_choices: output.update((random.choice(list(talent_choices)),))
        
        if type != 'social':
            talent_choices = social_talents - output
            if talent_choices: output.update((random.choice(list(talent_choices)),))
        
        if type != 'utility':
            talent_choices = utility_talents - output
            if talent_choices: output.update((random.choice(list(talent_choices)),))

        return collections.OrderedDict({key: talentlist[key] for key in list(output)})

def main():
    with open('data_4th/careers.json') as f:
        _careers_data = json.load(f)

    print("Searching for talents in careers but not in talents file:")
    for careername in _careers_data:
        for rank in range(1,5):
            careerlevel = _careers_data[careername]['rank {}'.format(rank)]
            for talent in careerlevel['talents']:
                checktalent = talent.split('(')[0].strip()
                if checktalent not in _talents_data: print(f'\t{careername} {rank} - {talent}')
    print()

    # Reformat talents
    for talent in _talents_data:
        if 'addskill' not in _talents_data[talent]: _talents_data[talent]['addskill'] = None
        if 'addtalent' not in _talents_data[talent]: _talents_data[talent]['addtalent'] = None
        if 'combat' not in _talents_data[talent]: _talents_data[talent]['combat'] = False
        if 'group' not in _talents_data[talent]: _talents_data[talent]['group'] = False
        if 'max' not in _talents_data[talent]: 
            print(f'Max not found for {talent}')
            _talents_data[talent]['max'] = None
        if 'social' not in _talents_data[talent]: _talents_data[talent]['social'] = False
        if 'stat_mod' not in _talents_data[talent]: _talents_data[talent]['stat_mod'] = None
        if 'tests' not in _talents_data[talent]: 
            print(_talents_data[talent]['tests'])
            _talents_data[talent]['tests'] = None
        if 'utility' not in _talents_data[talent]: _talents_data[talent]['utility'] = False

        if not isinstance(_talents_data[talent]['tests'], list):
            _talents_data[talent]['tests'] = [_talents_data[talent]['tests']]
        
    with open('talents_reformat.json','w') as f:
        json.dump(_talents_data,f,indent=4,sort_keys=True)

if __name__ == "__main__":
    # execute only if run as a script
    main()