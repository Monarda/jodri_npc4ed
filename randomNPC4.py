import itertools
import random
import sys

from .npc4 import Npc4
from .npc4 import _careers_data
from .npc4 import pretty_print_npc
from .find_best_match import find_best_match
from .careers4 import Careers4

from . import bot_char_dat

## From Archives of the Empire
# ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
bot_char_dat.career_table_4e += ['Ghost Strider', 0, 0, 0, 0, 2, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Field Warden',  0, 0, 2, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Karak Ranger',  0, 2, 0, 0, 0, 0, 0, 0, 0]
bot_char_dat.career_table_4e += ['Badger Rider',  0, 0, 3, 0, 0, 0, 0, 0, 0]

class RandomNPC4(Npc4):
    """Create a randomly generated NPC"""

    def __init__(self, species=None, starting_career=None, young=False, target=None):
        """Options are to define the species, a starting career, whether the NPC is young
           and a final career. The last uses a dictionary of the form {'career':'string', rank:n}
        """
        if not species:
            # Generate random species
            species = random.choices(['Human','Dwarf','Halfling','High Elf','Wood Elf'], cum_weights=[90,94,98,99,100])[0]
        
        if species.lower()=='human':
            species = random.choices(['Reiklander','Middenheimer','Middenlander','Nordlander'], weights=[5,1,2,2])[0]

        # Initialise base class
        Npc4.__init__(self,species)

        if starting_career: starting_career = starting_career.title()

        if target:
            self._reverse_random_careers(target,young)
        else:
            self._add_random_careers(starting_career,young)


    def _add_random_careers(self,starting_career=None, young=False):
        # Young people start at career rank 1, adults at career rank 2
        career = starting_career if starting_career else self._random_career()
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


    def _reverse_random_careers(self,target,young=False):
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
                
                # Finish this class
                for i in range(rank-1,0,-1):
                    careers_list.append((career,i))

                # Now switch to new class
                thisclass = _careers_data[career]['class']
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
        species_indexer = ['Reiklander','Dwarf','Halfling','High Elf','Wood Elf','Gnome','Nordlander','Middenheimer','Middenlander']
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


def main():
    random.seed()

    import argparse
    parser = argparse.ArgumentParser(description="Generate a random WFRP4 NPC")
    parser.add_argument("--cl", action='store_true', help="List known species and quit.")
    parser.add_argument("--species", type=str, nargs='?',default='Human', 
                        help="""Species of NPC to create. Valid species are Human, Reiklander, Dwarf, 
                                Halfling, High Elf, Wood Elf, Gnome, Nordlander, Middenheimer, and Middenlander.
                                Default is human. Human will be randomly assigned to Reiklander, Nordlander, 
                                Middenheimer, or Middenlander.""")
    parser.add_argument("--type", choices=['combat','social','utility'], help="Remove information not relevant to this type of NPC")
    parser.add_argument("--young", help="Young NPCs have a lower probability of career ranks and changes", action='store_true')
    parser.add_argument("career", help="Final career for NPC. Multi-word arguments must be quoted.", type=str,nargs='?', default=None)
    parser.add_argument("level",help="Final career level for NPC",type=int,nargs='?',default=None)
    parser.parse_args()
    args = parser.parse_args()

    # Produce a list of valid careers, sorted by class
    if args.cl:
        careers_by_class = Careers4()._careers_by_class
        print("Known careers: ")
        for classname, careers in careers_by_class.items():
            print("\t{:9s} - {}".format(classname, ', '.join(sorted(careers))))
        sys.exit()

    # Check if we've been given a target career and level
    if args.career and args.level:
        career = find_best_match(args.career.title(),Careers4().list_careers())
        target = {"career":career,"rank":args.level}
    elif (args.career and not args.level) or (not args.career and args.level):
        print("Career and level must be input as a pair\n")
        parser.print_help()
        sys.exit()
    else:
        target=None

    # Generate a Wood Elf Ghost Strider
    #npc = RandomNPC4(species="Wood Elf",young=False,target={"career":"Ghost Strider","rank":2})
    
    # Generate NPC
    npc = RandomNPC4(species=args.species,young=args.young,target=target)
    pretty_print_npc(npc, args.type)


if __name__ == "__main__":
    # execute only if run as a script
    main()