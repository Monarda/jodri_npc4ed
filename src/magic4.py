import collections
import json
import importlib.resources
import random
from typing import List
from .utility.find_best_match import find_best_match

from .. import data
with importlib.resources.open_text(data,'spells.json') as f:
    _magic_data = json.load(f)

from ..data import miscasts

class Magic4:
    class Lore:
        def __init__(self, lore : str):
            self._lore = lore

        def __getitem__(self, spellkey : str) -> dict:
            return dict(_magic_data[self._lore][spellkey])

    def __init__(self):
        self._error = None

        self._all_lores = dict()
        for lore in self.lores:
            lorename = lore.lower().lstrip('lore of ')

            self._all_lores[lorename] = lore
            self._all_lores[lore]     = lore

            if 'names' in _magic_data[lore]:
                for value in _magic_data[lore]['names'].values():
                    self._all_lores[value.lower()] = lore

    @property
    def error(self):
        return self._error

    def _lore_best_match(self, lore : str) -> str:
        if lore.lower() in self._all_lores:
            lorekey = self._all_lores[lore.lower()]
        else:
            bm = find_best_match(lore, self._all_lores.keys())
            if bm in self._all_lores:
                lorekey = self._all_lores[bm]
            else:
                self._error = f"I don't know the lore {lore}"
                return None
        
        return lorekey

    def __getitem__(self, lore : str) -> dict:
        lorekey = self._lore_best_match(lore)
        if not lorekey: return None

        return dict(_magic_data[lorekey])


    def spells(self, lore : str) -> dict:
        return dict(self[lore]['spells'])

    @property
    def lores(self) -> List[str]:
        return list(_magic_data.keys())

    @property 
    def lores_all(self) -> List[str]:
        return list(alllores.keys())

    def iscolour(self, lore : str) -> bool:
        return bool(self[lore]['colour'])

    def get_random_spells(self, lore : str, request_spells : int) -> dict:
        spells = self.spells(lore)

        actual_spells = len(spells)
        if request_spells > actual_spells:
            request_spells = actual_spells
            canon_lore = self._lore_best_match(lore)
            self._error = f'{canon_lore.title()} ({lore.title()}) has only {actual_spells} spells, listing all spells'
            print('error')

        random_spells = sorted(random.sample(list(spells), k=request_spells))
        return collections.OrderedDict({key: spells[key] for key in random_spells})

    def _miscast_template(self, miscast_table):
        miscast_names = miscast_table[0::3]
        miscast_prob  = miscast_table[1::3]
        miscast_rules = miscast_table[2::3]

        miscast_result = random.choices(miscast_names, cum_weights=miscast_prob,k=1)[0]

        d10  = random.randint(1,10)
        d100 = random.randint(1,100)
        rolld10    = f'({d10})'
        rolld100   = f'({d100})'
        rolld10by5 = f'({d10}×5= {d10*5})'

        idx = miscast_names.index(miscast_result)
        miscast_text = f'**{miscast_result}**: {miscast_rules[idx]}'.format(rolld10=rolld10, rolld100=rolld100, rolld10by5=rolld10by5)

        return miscast_text, miscast_result

    def miscast_minor(self) -> str:
        miscast_text, miscast_result = self._miscast_template(miscasts.magic_miscasts_minor)

        if miscast_result == 'Multiplying Misfortune':
            miscast_text += '\n\nRolling again twice:\n'
            miscast_text += self._miscast_template(miscasts.magic_miscasts_minor[:-6])[0] + '\n'
            miscast_text += self._miscast_template(miscasts.magic_miscasts_minor[:-6])[0]

        if miscast_result == 'Cascading Chaos':
            miscast_text += '\n\nResult from Major Miscast Table:\n' + self._miscast_template(miscasts.magic_miscasts_major)[0]

        return miscast_text

    def miscast_major(self) -> str:
        return self._miscast_template(miscasts.magic_miscasts_major)[0]
