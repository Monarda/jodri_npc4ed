import collections, itertools
import random

from npc4 import Npc4
from npc4 import _careers_data
from npc4 import pretty_print_npc

import bot_char_dat

## From Archives of the Empire
# ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
bot_char_dat.career_table_4e += ['Ghost Strider', 0, 0, 0, 0, 2, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Field Warden', 0, 0, 2, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Karak Ranger', 0, 2, 0, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Badger Rider', 0, 0, 3, 0, 0, 0, 0, 0, 0]

class RandomNPC4(Npc4):
    def __init__(self, species=None, starting_career=None, young=False, target=None):
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

        if target:
            self.reverse_random_careers(target,young)
        else:
            self.add_random_careers(young)

    def add_random_careers(self,young=False):
        # Young people start at career rank 1, adults at career rank 2
        career = self._random_career()
        rank = 1 if young else 2
        self.add_career(career,rank)

        # careers by class
        careers_by_class = dict()
        for careername in _careers_data:
            classname = _careers_data[careername]['class']
            if classname in careers_by_class:
                careers_by_class[classname].update([careername])
            else:
                careers_by_class[classname] = set([careername])

        more_careers = True
        while (more_careers):
            # Roll a dice to determine what to do
            # If an adult it's a d6, if young it's a d8 (higher numbers make us stop)
            dtype = 6 if not young else 8
            val = random.randint(1,dtype)

            if val<=2:
                # Keep in the career but go up a rank
                rank += 1
                self.add_career_rank(career,rank)                    
                if rank == 4: more_careers = False  # Stop if this is max career rank
            elif val==3:
                # Change to a career within the same class
                # Determine what the other classes are
                thisclass = _careers_data[career]['class']
                newcareers = careers_by_class[thisclass].difference([career])
                career = self._random_career(careerslist=newcareers,firstcareer=False)
                self.add_career_rank(career,rank)
            elif val==4:
                # Change to a career in another class
                # Find this class, then find all careers in careers_by_class which are not that class
                thisclass = _careers_data[career]['class']
                newcareers = itertools.chain.from_iterable([careers for classname,careers in careers_by_class.items() if classname!=thisclass])

                career = self._random_career(careerslist=newcareers,firstcareer=False)

                # If we've been in this career before then perhaps we should rejoin at that rank?
                rank = 1
                self.add_career_rank(career,rank)
            else:
                # Just stop, we're finished
                more_careers = False


    def reverse_random_careers(self,target,young=False):
        career = target['career']
        rank   = target['rank']
        careers_list = [(career,rank)]

        # careers by class
        careers_by_class = dict()
        for careername in _careers_data:
            classname = _careers_data[careername]['class']
            if classname in careers_by_class:
                careers_by_class[classname].update([careername])
            else:
                careers_by_class[classname] = set([careername])

        more_careers = True
        while (more_careers):
            # Roll a dice to determine what to do
            # If an adult it's a d6, if young it's a d8 (higher numbers make us stop)
            dtype = 6 if not young else 8
            val = random.randint(1,dtype)

            if val==3:
                # Change to a career within the same class
                # Determine what the other classes are
                thisclass = _careers_data[career]['class']
                newcareers = careers_by_class[thisclass].difference([career])
                career = self._random_career(careerslist=newcareers,firstcareer=False)
                careers_list.append((career,rank))
            elif val==4:
                # Change to a career in another class
                # Find this class, then find all careers in careers_by_class which are not that class
                if rank==1:
                    thisclass = _careers_data[career]['class']
                    newcareers = itertools.chain.from_iterable([careers for classname,careers in careers_by_class.items() if classname!=thisclass])

                    career = self._random_career(careerslist=newcareers,firstcareer=False)

                    # If we've been in this career before then perhaps we should rejoin at that rank?
                    rank = random.choices([1,2,3,4], weights=[2,3,2,1])[0]
                    careers_list.append((career,rank))
                else:
                    rank -= 1
                    careers_list.append((career,rank))
            else:
                # Keep in the career but go down a rank
                rank -= 1

                if rank>0:
                    careers_list.append((career,rank))
                else:
                    more_careers = False

        careers_list.reverse()
        for careerdata in careers_list:
            career = careerdata[0]
            rank   = careerdata[1]
            self.add_career_rank(career,rank)


    def _random_career(self, firstcareer=True, careerslist=None) -> str:
        # Extract the information we need from the bot_char_dat.career_table_4e array
        species_indexer = ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
        careers = bot_char_dat.career_table_4e[0::10]
        probs = bot_char_dat.career_table_4e[species_indexer.index(self._species)+1::10]

        # Append Cult Magus of Tzeentch to the probabilities as appropriate
        if not firstcareer:
            careers += ['Cult Magus Of Tzeentch', 'Warrior of Tzeentch']
            if self._index_species not in ['dwarf','halfling','gnome']:
                probs += [1, 1]
            else:
                probs += [0, 0]

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
    # Generate a Wood Elf Ghost Strider
    npc = RandomNPC4(species="Wood Elf",young=False,target={"career":"Ghost Strider","rank":2})
    pretty_print_npc(npc)

    # Generate a random NPC
    npc = RandomNPC4()
    pretty_print_npc(npc)


if __name__ == "__main__":
    # execute only if run as a script
    main()