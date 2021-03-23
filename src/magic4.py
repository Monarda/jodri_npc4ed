import argparse
import collections
import json
import importlib.resources
import random
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
        pass

    def __getitem__(self, lore : str) -> dict:
        lorekey = lore.lower()
        return dict(_magic_data[lorekey]['spells'])

    def iscolour(self, lore : str) -> bool:
        lorekey = lore.lower()
        return _magic_data[lorekey]['colour']

    def get_random_spells(self, lore : str, nospells : int) -> dict:
        lorekey = lore.lower()
        spells = self[lorekey]
        random_spells = sorted(random.sample(list(spells), k=nospells))
        return collections.OrderedDict({key: spells[key] for key in random_spells})

def main():
    random.seed()

    parser = argparse.ArgumentParser(description="Generate spells from the specified lore")
    parser.add_argument("nospells", type=int)
    parser.add_argument("lore", nargs='+')
    parser.parse_args()
    args = parser.parse_args()
 
    m4 = Magic4()
    selection = find_best_match( ' '.join(args.lore), _magic_data.keys() )
    nochoices = min(args.nospells, len(m4[selection]))
    print('Colour: {}'.format(m4.iscolour(selection)))
    print('; '.join( m4.get_random_spells(selection,nochoices) ))

if __name__ == "__main__":
    # execute only if run as a script
    main()