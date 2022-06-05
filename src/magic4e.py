import collections, copy
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

    def get_wind_name(self, lore):
        """ Return the wind name that best matches the input text, e.g. "Lore of Shadows" becomes 'ulgu' 
            If there is no wind name it will return the lore name, e.g. "Petty Lore"
        """

        lore_name = self._lore_best_match(lore)
        if 'colour' in _magic_data[lore_name] and _magic_data[lore_name]['colour'] == True: 
            return _magic_data[lore_name]["names"]["wind"]
        else:
            return lore_name

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

    def spells(self, lore : str, max_cn : int = None) -> dict:
        """ Get all the spells for the specified lore and maximum Casting Number (CN) """
        spells = self[lore]['spells'] 

        if max_cn:
            for spell in spells.copy():
                if spells[spell]['CN']>max_cn:
                    spells.pop(spell)

        return dict(spells)

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

    def get_random_spells(self, lore : str, request_spells : int, max_cn : int = None) -> dict:
        """ Get n random spells from a lore """
        spells = self.spells(lore, max_cn)

        number_available_spells = len(spells)
        if request_spells > number_available_spells:
            request_spells = number_available_spells
            canon_lore = self._lore_best_match(lore)

            max_cn_msg = ''
            if max_cn: max_cn_msg = f' with maximum CN of {max_cn}'
            self._error = f'{canon_lore.title()} ({lore.title()}) has only {number_available_spells} spells{max_cn_msg}, listing all spells'

        random_spells = sorted(random.sample(list(spells), k=request_spells))
        return collections.OrderedDict({key: spells[key] for key in random_spells})

    def miscast_minor(self) -> str:
        """ Return text describing a randomly rolled minor miscast. 
        
            Includes rerolls and escalations to major miscasts """
        return miscast.miscast_minor()

    def miscast_major(self) -> str:
        """ Return text describing a randomly rolled major miscast."""
        return miscast.miscast_major()

    def miscast_grimoire(self) -> str:
        """ Return text describing a randomly rolled grimoire miscast."""
        return miscast.miscast_grimoire()        

    def random_mark(self, lore) -> str:
        """ Return text describing a randomly rolled arcane mark from the specified lore."""

        # Load the JSON data about arcane marks
        with importlib.resources.open_text(data,'arcane_marks.json') as f:
            _marks_data = json.load(f)

        # Turn the lore into a wind name so we can do a lookup in the json
        wind_name = self.get_wind_name(lore)
        
        # Choose a mark at random
        mark = random.choices(_marks_data[wind_name], k=1)[0]

        # Return the result with some formatting
        return f"**{mark['title']}**: {mark['description']}"