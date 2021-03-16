import collections, itertools
import random

from npc4 import Npc4
from npc4 import _careers_data
from npc4 import pretty_print_npc

import bot_char_dat

## From Archives of the Empire
bot_char_dat.career_table_4e += ['Ghost Strider', 0, 0, 0, 0, 2, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Fieldwarden', 0, 0, 2, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Karak Ranger', 0, 2, 0, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Badger Rider', 0, 0, 3, 0, 0, 0, 0, 0, 0]

class RandomNPC4(Npc4):
    def __init__(self, species=None, starting_career=None, young=False):
        if not species:
            # Generate random species
            species_roll = random.randint(1,100)
            if species_roll<=90:
                species = 'Human'
            elif species_roll<=94:
                species = 'Halfling'
            elif species_roll<=98:
                species = 'Dwarf'
            elif species_roll<=99:
                species = 'High Elf'
            elif species_roll<=100:
                species = 'Wood Elf'
        
        if species.lower()=='human':
            human_roll = random.randint(1,10)
            if human_roll<=5:
                species = 'Reiklander'
            elif human_roll<=6:
                species = 'Middenheimer'
            elif human_roll<=8:
                species = 'Middenlander'
            elif human_roll<=10:
                species = 'Nordlander'

        Npc4.__init__(self,species)

        self.add_random_careers()

    def add_random_careers(self):
        career = self._random_career()
        rank = 2
        self.add_career(career,rank)

        more_careers = True
        while (more_careers):
            val = random.randint(1,6) 
            if val<=2:
                # Keep in the career but go up a rank
                rank += 1
                self.add_career_rank(career,rank)                    
                if rank == 4: more_careers = False
            elif val==3:
                # Change to a career within the same class
                thisclass = _careers_data[career]['class']
                newcareers = set()
                for careername in _careers_data:
                    if _careers_data[careername]['class']==thisclass:
                        newcareers.update([careername])
                newcareers -= set([career])

                career = self._random_career(careerslist=newcareers,firstcareer=False)
                self.add_career_rank(career,rank)
            elif val==4:
                # Change to a career in another class
                thisclass = _careers_data[career]['class']
                newcareers = set()
                for careername in _careers_data:
                    if _careers_data[careername]['class']!=thisclass:
                        newcareers.update([careername])

                career = self._random_career(careerslist=newcareers,firstcareer=False)

                # If we've been in this career before then perhaps we should rejoin at that rank?
                rank = 1
                self.add_career_rank(career,rank)
            else:
                # Just stop, we're finished
                more_careers = False


    def _random_career(self, firstcareer=True, careerslist=None) -> str:
        # Extract the information we need from the bot_char_dat.career_table_4e array
        species_indexer = ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
        careers = bot_char_dat.career_table_4e[0::10]
        probs = bot_char_dat.career_table_4e[species_indexer.index(self._species)+1::10]

        # Append Cult Magus of Tzeentch to the probabilities as appropriate
        if not firstcareer:
            careers.append('Cult Magus Of Tzeentch')
            if self._index_species not in ['dwarf','halfling','gnome']:
                probs.append(1)
            else:
                probs.append(0)

        # If we've been provided a careerslist we still use the species weightings, but that means
        # we need to assemble them
        if careerslist:
            newcareers = []
            newprobs   = []
            for careername in careerslist:
                idx = careers.index(careername)
                newcareers.append(careername)
                newprobs.append(probs[idx])
            careers = newcareers
            probs   = newprobs

        return random.choices(careers,weights=probs)[0]


def main():
    npc = RandomNPC4("Halfling")
    pretty_print_npc(npc)


if __name__ == "__main__":
    # execute only if run as a script
    main()