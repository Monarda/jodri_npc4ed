import collections
import json
import importlib.resources
import random
from ..src.magic import miscast
from typing import List
from .utility.find_best_match import find_best_match

from .. import data
with importlib.resources.open_text(data,'spells.json') as f:
    _magic_data = json.load(f)


class Magic4e:
    """ Class to contain all commands and related information for 4th ed lores, spells, and casting """
    class Lore:
        def __init__(self, lore : str):
            self._lore = lore

        def __getitem__(self, spellkey : str) -> dict:
            return dict(_magic_data[self._lore][spellkey])

    def __init__(self):
        self._error = None

        self._all_lores = dict()
        self._all_lores['all'] = 'all'
        for lore in self.lores:
            #lorename = lore.lower().removeprefix('lore of')
            lorename = lore.lower().strip()
            if lorename.startswith('lore of'): lorename = lorename[8:].strip()
            #lorename = lore.lower().removeprefix('lore of')

            self._all_lores[lorename] = lore
            self._all_lores[lore]     = lore

            if 'names' in _magic_data[lore]:
                for value in _magic_data[lore]['names'].values():
                    self._all_lores[value.lower()] = lore

    @property
    def error(self):
        return self._error

    def _lore_best_match(self, lore : str) -> str:
        """ Find the lore that best matches what was input """

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

    def canonise_lore(self, lore):
        """ Return the lore that best matches the input text, e.g. 'ulgu becomes "Lore of Shadows" """

        return self._lore_best_match(lore)

    def __getitem__(self, lore : str) -> dict:
        lorekey = self._lore_best_match(lore)
        if not lorekey: raise KeyError(f"'{lore}' is not valid key for spells dictionary")

        if lore.lower()!='all':
            return dict(_magic_data[lorekey])
        else:
            lores = {'spells':{}, 'colour':True}
            for lore in _magic_data:
                if 'colour' in self[lore] and self[lore]['colour'] == True:
                    lores['spells'].update(self.spells(lore))
            return lores

    def spells(self, lore : str) -> dict:
        """ Get all the spells for the specified lore """
        return dict(self[lore]['spells'])

    @property
    def lores(self) -> List[str]:
        """ Get a list of all the lores as keys used in the data lookup """
        return list(_magic_data.keys())

    @property 
    def lores_all(self) -> List[str]:
        """ Get a list of all the lores, including alternate names"""
        return list(self._all_lores.keys())

    def iscolour(self, lore : str) -> bool:
        """ Is this lore one of the colour magics? """
        return bool(self[lore]['colour'])

    def get_random_spells(self, lore : str, request_spells : int) -> dict:
        """ Get n random spells from a lore """
        spells = self.spells(lore)

        actual_spells = len(spells)
        if request_spells > actual_spells:
            request_spells = actual_spells
            canon_lore = self._lore_best_match(lore)
            self._error = f'{canon_lore.title()} ({lore.title()}) has only {actual_spells} spells, listing all spells'
            print('error')

        random_spells = sorted(random.sample(list(spells), k=request_spells))
        return collections.OrderedDict({key: spells[key] for key in random_spells})

    def miscast_minor(self) -> str:
        """ Return text describing a randomly rolled minor miscast. 
        
            Includes rerolls and escalations to major miscasts """
        return miscast.miscast_minor()

    def miscast_major(self) -> str:
        """ Return text describing a randomly rolled major miscast."""
        return miscast.miscast_major()