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

## From The Horned Rat Companion, p.81
bot_char_dat.career_table_4e += ['Ironbreaker',  0, 3, 0, 0, 0, 0, 0, 0, 0]

class RandomNPC4(BuildNPC4):
    """Create a randomly generated NPC"""

    def __init__(self, species=None, starting_career=None, young=False, target=None, lore=None,
                       characteristics=None, starting_skills = None, starting_talents=None, starting_trappings=None,
                       init_only=False):
        """Options are to define the species, a starting career, whether the NPC is young
           and a final career. The last uses a dictionary of the form {'career':'string', rank:n}
        """
        if not species:
            # Generate random species
            species = self.random_species()
        
        if species.lower()=='human':
            species = self.random_human()

        # Initialise base class
        BuildNPC4.__init__(self, species, lore,
                            characteristics=characteristics,
                            starting_skills=starting_skills, 
                            starting_talents=starting_talents,
                            starting_trappings=starting_trappings)

        # Record anything we might need to use to rebuild the class
        self._young = young

        if init_only: return

        if starting_career: starting_career = starting_career.title()

        if target:
            self._reverse_random_careers(target,young)
        else:
            self._add_random_careers(starting_career,young)

    class NoCareersSpecies(Exception):
        def __init__(self, species):
            super().__init__(f'Cannot generate random career for {species}. This species does not have a career probability table (e.g. corebook, p.30-31).')


    @classmethod
    def known_species(cls):
        return ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']

    @classmethod
    def known_humans(cls):
        return ['Reiklander','Nordlander','Middenheimer','Middenlander']

    @classmethod
    def random_species(cls):
        """ Generate a random valid species, with defined probabilities """
        species = random.choices(['Human','Dwarf','Halfling','High Elf','Wood Elf'], cum_weights=[90,94,98,99,100])[0]
        
        if species.lower()=='human':
           species = cls.random_human()

        return species

    @classmethod
    def random_human(cls):
        """ Generate a random valid human type (from the defined types), with defined probabilities """
        return random.choices(['Reiklander','Middenheimer','Middenlander','Nordlander'], weights=[5,1,2,2])[0]


    def _careers_by_class(self):        
        careers_by_class = dict()
        for careername in Careers4().careers:
            classname = Careers4()[careername]['class']
            if classname in careers_by_class:
                careers_by_class[classname].update([careername])
            else:
                careers_by_class[classname] = set([careername])

        return careers_by_class


    def _add_random_careers(self, career, young=False, force_first=False):
        # If no career tuple given create one
        if career != None:
            career_name = career[0].title()
            career_rank = career[1]
        else:
            career_name = self._random_career()
            career_rank = 1

            # if young:
            #     career_rank = 1
            # else:
            #     self.add_career_rank(career_name,1)
            #     career_rank = 2

        # Add the specified career and carry on from here
        self.add_career_rank(career_name,career_rank)

        careers_by_class = self._careers_by_class()

        more_careers = True
        while (more_careers):
            # Roll a dice to determine what to do
            # If an adult it's a d6, if young it's a d8 (higher numbers make us stop)
            if (force_first):
                dtype = 4
                force_first = False
            else:
                dtype = 6 if not young else 8
            val = random.randint(1,dtype)

            if val<=2:
                # Keep in the career but go up a rank
                career_rank += 1
                self.add_career_rank(career_name,career_rank)                    
                if career_rank == 4: more_careers = False  # Stop if this is max career rank
            elif val==3:
                # Change to a career within the same class
                # Determine what the other classes are
                thisclass = Careers4()[career_name]['class']
                newcareers = careers_by_class[thisclass].difference([career_name])
                career_name = self._random_career(careerslist=newcareers,firstcareer=False)
                self.add_career_rank(career_name,career_rank)
            elif val==4:
                # Change to a career in another class
                # Find this class, then find all careers in careers_by_class which are not that class
                thisclass = Careers4()[career_name]['class']
                newcareers = itertools.chain.from_iterable([careers for classname,careers in careers_by_class.items() if classname!=thisclass])

                career_name = self._random_career(careerslist=newcareers,firstcareer=False)

                # If we've been in this career before then perhaps we should rejoin at that rank?
                career_rank = 1
                self.add_career_rank(career_name,career_rank)
            else:
                # Just stop, we're finished
                more_careers = False


    def _reverse_random_careers(self,target,young=False):
        career = target['career'].title()
        rank   = target['rank']
        careers_list = [(career,rank)]

        careers_by_class = self._careers_by_class()

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


    def _span_random_careers(self, startcareer, endcareer, young=False):
        # First go, let's not be clever, use the existing random generator and then simply append
        # the required final career
        self._add_random_careers(startcareer, young)

        # Then handle the special case of the startcareer and endcareer being the same
        if (startcareer == endcareer):
            self._reverse_random_careers({'career':endcareer[0], 'rank':endcareer[1]}) 

        # Details about where we are and where we want to be
        end_career = endcareer[0].title()
        end_level  = endcareer[1]
        current_career = self._career_history[-1][0].title()
        current_level = self._career_history[-1][1]

        # Check whether we're currently in the desired career. If so we just need to adjust levels
        if end_career == current_career:
            if end_level == current_level:
                pass
            elif end_level>current_level:
                # Add career levels until we're in the right place
                for level in range(current_level+1,end_level+1):
                    self.add_career_rank(end_career,level)
            elif end_level<current_level:
                # Damn, we have to remove career levels. The simplest way is simply to rebuild
                # without those career levels. To do that we need to assemble a new revised 
                # career history to apply
                # This is trickier than it might seem because there are two ways we could get here
                # Consider that we want a Priest (priest,2) but have generated a High Priest (priest,3)
                # The most likely case is that we've simply overshot and the career history looks
                # something like [... (priest,1), (priest,2), (priest,3)]. In this case we just need to
                # delete the extar career levels
                # But we could also have a case like [(wizard,3),(priest,3)] in which case we need to
                # change the final career level
                new_career_history = list(self._career_history)
                while new_career_history[-1]!=(end_career,end_level):
                    if new_career_history[-2][0] != end_career:
                        new_career_history[-1] = (end_career,end_level)
                    else:
                        new_career_history.pop()
                print(new_career_history)

                newNPC = RandomNPC4(species=self._species, starting_career=None, young=self._young, 
                                    characteristics=self._starting_characteristics,
                                    starting_skills=self._starting_skills, starting_talents=self._starting_talents,
                                    starting_trappings=self._starting_trappings,
                                    init_only=True)

                for career, level in new_career_history:
                    newNPC.add_career_rank(career, level)
                
                self.__dict__.update(newNPC.__dict__)
            
            return

        # We need to move the NPC to the new career and level
        # Are we in the right class?
        careers_by_class = self._careers_by_class()
        class_by_careers = {}
        for k,value in careers_by_class.items():
            for v in value:
                class_by_careers.setdefault(v,[]).append(k)

        current_class = class_by_careers[current_career]
        end_class     = class_by_careers[end_career]
        if current_class == end_class:
            if current_level>=end_level:
                self.add_career_rank(end_career,end_level)
            else:
                for level in range(current_level,end_level+1):
                    self.add_career_rank(end_career,level)
        else:
            for level in range(1,end_level+1):
                self.add_career_rank(end_career,level)


    def _random_career(self, firstcareer=True, careerslist=None) -> str:
        # Extract the information we need from the bot_char_dat.career_table_4e array
        species_indexer = self.known_species()
        careers = bot_char_dat.career_table_4e[0::10]
        try:
            probs = bot_char_dat.career_table_4e[species_indexer.index(self._species.title())+1::10]
        except ValueError:
            raise self.NoCareersSpecies(self._species.title())
        except:
            raise

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
