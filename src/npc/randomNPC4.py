import itertools
import random
import sys

from .buildNPC4 import BuildNPC4
from ..utility.find_best_match import find_best_match
from .careers4 import Careers4

from ...data import bot_char_dat

## From Archives of the Empire
# ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
bot_char_dat.career_table_4e += ['Ghost Strider', 0, 0, 0, 0, 2, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Field Warden',  0, 0, 2, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Karak Ranger',  0, 2, 0, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Badger Rider',  0, 0, 3, 0, 0, 0, 0, 0, 0]

class RandomNPC4(BuildNPC4):
    """Create a randomly generated NPC"""

    def __init__(self, species=None, starting_career=None, young=False, target=None, 
                       characteristics=None, starting_skills = None, starting_talents=None, starting_trappings=None,
                       init_only=False):
        """Options are to define the species, a starting career, whether the NPC is young
           and a final career. The last uses a dictionary of the form {'career':'string', rank:n}
        """
        if not species:
            # Generate random species
            species = random.choices(['Human','Dwarf','Halfling','High Elf','Wood Elf'], cum_weights=[90,94,98,99,100])[0]
        
        if species.lower()=='human':
            species = random.choices(['Reiklander','Middenheimer','Middenlander','Nordlander'], weights=[5,1,2,2])[0]

        # Initialise base class
        BuildNPC4.__init__(self, species, 
                            characteristics=characteristics,
                            starting_skills=starting_skills, 
                            starting_talents=starting_talents,
                            starting_trappings=starting_trappings)

        if init_only: return

        if starting_career: starting_career = starting_career.title()

        if target:
            self._reverse_random_careers(target,young)
        else:
            self._add_random_careers(starting_career,young)

    @classmethod
    def known_species(cls):
        return ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']

    @classmethod
    def known_humans(cls):
        return ['Reiklander','Nordlander','Middenheimer','Middenlander']
        

    def _add_random_careers(self,starting_career=None, young=False):
        # Young people start at career rank 1, adults at career rank 2
        career = starting_career if starting_career else self._random_career()
        rank = 1 if young else 2

        self.add_career(career,rank)

        # careers by class
        careers_by_class = dict()
        for careername in Careers4().careers:
            classname = Careers4()[careername]['class']
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
                thisclass = Careers4()[career]['class']
                newcareers = careers_by_class[thisclass].difference([career])
                career = self._random_career(careerslist=newcareers,firstcareer=False)
                self.add_career_rank(career,rank)
            elif val==4:
                # Change to a career in another class
                # Find this class, then find all careers in careers_by_class which are not that class
                thisclass = Careers4()[career]['class']
                newcareers = itertools.chain.from_iterable([careers for classname,careers in careers_by_class.items() if classname!=thisclass])

                career = self._random_career(careerslist=newcareers,firstcareer=False)

                # If we've been in this career before then perhaps we should rejoin at that rank?
                rank = 1
                self.add_career_rank(career,rank)
            else:
                # Just stop, we're finished
                more_careers = False


    def _reverse_random_careers(self,target,young=False):
        career = target['career'].title()
        rank   = target['rank']
        careers_list = [(career,rank)]

        # careers by class
        careers_by_class = dict()
        for careername in Careers4().careers:
            classname = Careers4()[careername]['class']
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
                thisclass = Careers4()[career]['class']
                newcareers = careers_by_class[thisclass].difference([career])
                career = self._random_career(careerslist=newcareers,firstcareer=False)
                careers_list.append((career,rank))
            elif val==4:
                # Change to a career in another class
                # Find this class, then find all careers in careers_by_class which are not that class
                
                # Finish this class
                for i in range(rank-1,0,-1):
                    careers_list.append((career,i))

                # Now switch to new class
                thisclass = Careers4()[career]['class']
                newcareers = itertools.chain.from_iterable([careers for classname,careers in careers_by_class.items() if classname!=thisclass])

                career = self._random_career(careerslist=newcareers,firstcareer=False)

                rank = random.choices([1,2,3], weights=[2,3,2])[0]
                
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
        species_indexer = self.known_species()
        careers = bot_char_dat.career_table_4e[0::10]
        probs = bot_char_dat.career_table_4e[species_indexer.index(self._species.title())+1::10]

        # Append Cult Magus of Tzeentch to the probabilities as appropriate
        if not firstcareer:
            careers += ['Cult Magus Of Tzeentch', 'Warrior Of Tzeentch']
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
