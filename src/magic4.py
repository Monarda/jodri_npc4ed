import collections
import json
import importlib.resources
import random
from typing import List
from .utility.find_best_match import find_best_match

from .. import data
with importlib.resources.open_text(data,'spells.json') as f:
    _magic_data = json.load(f)

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
