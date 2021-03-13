import collections, json, math, sys
import bot_char_dat
from pprint import pprint

class npc_4e:

    def __init__(self, species, 
                 characteristics=None, starting_skills=None, starting_talents=None, starting_trappings=None):
        # Load data about careers, talents and skills
        with open('4th_ed_data/careers.json') as f:
            self._careers_data = json.load(f)

        with open('4th_ed_data/skills.json') as f:
            self._skills_data = json.load(f)

        with open('4th_ed_data/talents.json') as f:
            self._talents_data = json.load(f)

        # For now we assume if we don't know the species it's a type of human unless it contains the word 'elf'
        self._species = species

        known_species = {"human", "dwarf", "halfling", "elf", "gnome"}
        if species.lower() in known_species:
            index_species = species
        else:
            if 'elf' in species.lower():
                index_species = 'elf'
            else:
                index_species = 'human'

        # Either use characteristics based on species (see 4th Ed Corebook p.311)
        # or use characteristics passed in by caller
        if not characteristics:
            species_npc_characteristics_4e = {
                "human":    {"M":4, "WS":30, "BS":30, "S":30, "T":30, "I":30, "Agi":30, "Dex":30, "Int":30, "WP":30, "Fel":30},
                "dwarf":    {"M":4, "WS":40, "BS":30, "S":30, "T":40, "I":30, "Agi":20, "Dex":40, "Int":30, "WP":50, "Fel":20},
                "halfling": {"M":4, "WS":20, "BS":40, "S":20, "T":30, "I":30, "Agi":30, "Dex":30, "Int":30, "WP":30, "Fel":30},
                "elf":      {"M":5, "WS":40, "BS":40, "S":30, "T":30, "I":50, "Agi":40, "Dex":40, "Int":40, "WP":40, "Fel":30},
                "gnome":    {"M":3, "WS":30, "BS":20, "S":20, "T":25, "I":40, "Agi":40, "Dex":40, "Int":40, "WP":50, "Fel":25}
            }
            self._characteristics = species_npc_characteristics_4e[index_species]
        else:
            self._characteristics = characteristics

        # Traits are always set based on species, which poses a problem if species is 'Reiklander'!
        species_npc_traits_4e = {
            "human": 'Prejudice (choose one), Weapon +7',
            "dwarf" : 'Animosity (choose one), Hatred (Greenskins), Magic Resistance (2), Night Vision, Prejudice (choose one), Weapon +7',
            "halfling": 'Night Vision, Size (Small), Weapon +5',
            "elf": 'Animosity (choose one), Prejudice (choose two), Night Vision, Weapon+7',
            "gnome": 'Night vision, Size (Small), Weapon +7'
        }
        species_npc_optional_traits_4e = {
            "human": 'Disease, Ranged +8 (50), Spellcaster',
            "dwarf" : 'Fury, Ranged +8 (50)',
            "halfling": 'Ranged +7 (25), Stealthy',
            "elf": 'Arboreal, Magical, Magical Resistance, Ranged+9 (150), Stealthy, Spellcaster (any one), Tracker' ,
            "gnome": ''       
        }
        self._traits            = species_npc_traits_4e[index_species]
        self._optional_traits   = species_npc_optional_traits_4e[index_species]

        self._starting_skills    = starting_skills if starting_skills is not None else set() # Need to record these to allow XP calculating
        self._starting_talents   = starting_talents if starting_talents is not None else set()
        self._starting_trappings = starting_trappings if starting_trappings is not None else set()

        self._careers_taken     = {}                    # Careers taken and their max rank
        self._career_history    = collections.deque()   # The order in which careers and ranks were taken
        self._skills            = starting_skills if starting_skills is not None else {}
        self._suggested_talents = set()
        self._talents           = set()
        self._trappings         = set()



    def __str__(self):
        # Species and most recent career level name
        lastcareer, lastrank = next(reversed(self._career_history))
        lastcareername = self._careers_data[lastcareer]['rank {}'.format(lastrank)]['name']

        retstr  = self._species.title() + " " + lastcareername + '\n'
        retstr += 'Career history: ' + str(self.career_history) + '\n'

        # Characteristics
        retstr += str(self.characteristics) + '\n'

        # Skills       
        simple_skills, complex_skills = self.skills
        retstr += "Skills: " + str(simple_skills) + '\n'
        # retstr += "Skills: " 
        # for key, value in complex_skills.items():
        #     retstr += "{} {} [{}+{}], ".format(key, value['total'], value['characteristic'], value['add'])
        # retstr += '\n'

        # Talents
        if self.starting_talents:
            retstr += "Starting Talents:  " + str(self.starting_talents) + "\n"
        retstr += "Suggested Talents: " + str(self.suggested_talents) + "\n"
        retstr += "Additional Talents: " + str(self.additional_talents) + "\n"

        # Traits
        retstr += 'Traits: ' + self._traits + '\n'
        retstr += 'Optional Traits: ' + self._optional_traits + '\n'

        # Trappings
        retstr += "Trappings: " + str(self.trappings) + "\n"

        # Verbose
        retstr += "\n\nTalents by Career: " + str(self.talents_by_career) + "\n"
        retstr += "Suggested Talents by Career: " + str(self.suggested_talents_by_career) + "\n"
        retstr += "Additional Talents by Career: " + str(self.alternate_talents_by_career) + "\n"

        return retstr


    @property 
    def career_history(self):
        return [self._careers_data[career]['rank {}'.format(rank)]['name'] for career,rank in self._career_history]

    @property
    def characteristics(self):
        output_chars = dict(self._characteristics)
        output_chars.update({'W':self._wounds})

        return output_chars


    def _characteristic_bonus(self, charb):
        def _get_digit(number, n):
            return number // 10**n % 10        

        return _get_digit(self._characteristics[charb[:-1]],1)

    @property
    def _wounds(self):
        def _get_digit(number, n):
            return number // 10**n % 10

        if self._species != 'gnome':
            wounds =    self._characteristic_bonus('SB') \
                    + 2*self._characteristic_bonus('TB') \
                    +   self._characteristic_bonus('WPB')
        else:
            wounds =  2*self._characteristic_bonus('TB') \
                    +   self._characteristic_bonus('WPB')

        return wounds

    @property
    def _money(self):
        # Get the most recent career and rank
        lastcareer, lastrank = next(reversed(self._career_history))
        status = self._careers_data[lastcareer]['rank {}'.format(lastrank)]['status']

        tokens = status.split(' ')

        money = "{}d10 {}".format(tokens[1],tokens[0])

        return money

    @property
    def trappings(self):
        # Most recent career and rank
        lastcareer, lastrank = next(reversed(self._career_history))
        
        trappings = [] 
        for i in range(1,lastrank+1):
            trappings += self._careers_data[lastcareer]['rank {}'.format(i)]['trappings']

        trappings += [self._money]

        return sorted(trappings)

    def __template_gettalents(self, selector):
        out_talents = {}
        for talent in sorted(selector):
            # Check if this talent is in the talent list
            talent_index = talent
            if talent in self._talents_data:
                # It is
                out_talents[talent] = self._talents_data[talent]
            else:
                # It isn't... That might mean it's a group talent
                talentfound = False
                for shortform in bot_char_dat.talent_groups_4e:
                    if talent.startswith(shortform):
                        out_talents[talent] = self._talents_data[shortform]
                        talent_index = shortform
                        talentfound = True
                        break
                
                if not talentfound:
                    out_talents[talent] = {}

            try:
                if not isinstance(out_talents[talent]['max'],int) and not isinstance(out_talents[talent]['max'],float):
                    out_talents[talent]['max'] = self._characteristic_bonus(out_talents[talent]['max'])
            except KeyError:
                pass

        return out_talents

    @property
    def talents(self):
        return self.__template_gettalents(set(self._talents) + self._starting_talents)

    @property
    def starting_talents(self):
        return self.__template_gettalents(self._starting_talents)

    @property 
    def suggested_talents(self):
        # We don't remove starting talents from the list, because career talents can potentially 
        # be taken multiple times without needing GM approval. Though since this is an NPC the
        # GM could probably approve!
        return self.__template_gettalents(self._suggested_talents)

    @property
    def additional_talents(self):
        return self.__template_gettalents(self._talents-self._suggested_talents)

    def __template_by_career(self, selector):
        out_talents = {}

        # We have two different career histories for an NPC.
        # The first is the 'true' history, of the career ranks we actually took
        # And the other is the one that includes career ranks that were not taken
        # but still have talents available. For example, an NPC takes Doctor 2 but
        # not Doctor 1: they still have all talents from Doctor 1 available
        true_history = []
        for career,rank in self._career_history:
            careerrankname = self._careers_data[career]['rank {}'.format(rank)]['name']
            true_history.append(careerrankname)

        avail_history = set()
        for career,rank in self._careers_taken.items():
            avail_history.update([(career, i) for i in range(1,rank+1)])

        # Go through the career ranks for all could contribute talents
        # Add a star to the end of the careername if it was not really taken
        for careername,rank in avail_history:
            careerrank = self._careers_data[careername]['rank {}'.format(rank)]
            careerrankname = careerrank['name']

            if careerrankname not in true_history:
                careerrankname += '*'

            out_talents[careerrankname] = self.__template_gettalents(selector(careerrank))

        return out_talents

    @property 
    def talents_by_career(self):
        selector = lambda careerrank : careerrank['talents']

        return self.__template_by_career(selector)

    @property
    def suggested_talents_by_career(self):
        selector = lambda careerrank : careerrank['npc_essential_talents']

        return self.__template_by_career(selector)
      
    @property
    def alternate_talents_by_career(self):
        selector = lambda careerrank : set(careerrank['talents']) - set(careerrank['npc_essential_talents'])

        return self.__template_by_career(selector) 

    # We return two takes on the NPC's skills list. The first is a simple one which is just ("skill:value") pairs
    # The second is a more complex dictionary of the form 
    #    '"Melee (Any)" : {"characteristic":"WS", "total":45, "add":10}'
    # where total is the same as the value in the simple case and add is the amount to be added to the 
    # characteristic 
    @property
    def skills(self):
        calced_skills = {}
        complex_skills = {}
        for skill, value in sorted(self._skills.items()):
            if skill in self._skills_data:
                skillchar  = self._skills_data[skill]['characteristic']
                skilltotal = self._characteristics[skillchar] + value

                calced_skills[skill] = skilltotal
                complex_skills[skill] = {"total":skilltotal, "characteristic":skillchar, "add":value}
            else:
                # This is presumably a group skill, so we need to find the longest match instead of the exact match
                skillfound = False
                for key in self._skills_data:
                    if skill.startswith(key):
                        skillchar  = self._skills_data[key]['characteristic']
                        skilltotal = self._characteristics[skillchar] + value

                        calced_skills[skill] = skilltotal
                        complex_skills[skill] = {"total":skilltotal, "characteristic":skillchar, "add":value}

                        skillfound = True
                        break

                if not skillfound:
                    raise KeyError("{} is not a known skill".format(skill))

        return calced_skills, complex_skills


    # Add a single career rank to the NPC, e.g. Soldier 2
    def _add_career_rank(self, careername, rank):
        # Validate input
        if rank<1 or rank>4:
            raise IndexError('Rank less than 0 or greater than 4')

        try:
            self._careers_data[careername]
        except KeyError:
            raise KeyError("{} is not a valid career name".format(careername))

        # Check if we've been in this career before. Only update the NPC if 
        # we haven't been in this career before or only at a lower rank
        # We thus support something slightly odd like `soldier 1 soldier 3`
        oldrank = self._careers_taken.get(careername,0)
        if rank <= oldrank:
            # We've been in this career and rank before so there's nothing to do
            # Except that we need to record that this is the current career and
            # rank of the NPC
            self._careers_taken[careername] = rank

            self._career_history.append((careername,rank))
            return        

        # We need to update the NPC with the new career rank
        # This means applying the characteristic advances and skills of this rank
        # and all previous ranks in the career. We also update the suggested and
        # available talents. 
        for i in range(1,rank+1):
            # Get the information about this career rank
            careerrank = self._careers_data[careername]['rank {}'.format(i)]

            # Apply all applicable characteristic advances
            for advance in careerrank['advances']:
                self._characteristics[advance] += 5
            
            # Either start tracking a new skill or add to an existing one
            for skill in careerrank['skills']:
                if skill in self._skills:
                    self._skills[skill] += 5
                else:
                    self._skills[skill] = 5

            # Update the list of suggested talents
            self._suggested_talents.update(careerrank['npc_essential_talents'])

            # And update the list of all available talents
            self._talents.update(careerrank['talents'])

        # Update career history
        self._careers_taken[careername] = rank
        self._career_history.append((careername,rank))


    # Utility function to apply all career ranks up to the specified one to an NPC
    # So calling with Soldier 3 will apply Soldier 1, Soldier 2, and Soldier 3
    def add_career(self, careername, rank):
        careername = careername.title()
        # Validate input
        career = self._careers_data[careername] # Blow up early if career not in list of careers
        if rank<1 or rank>4:
            raise IndexError('Rank less than 0 or greater than 4')

        for i in range(1, rank+1):
            self._add_career_rank(careername, i)


def main():
    # npc = npc_4e("human")
    # npc.add_career("Engineer", 2)

    ## Hospitaller Cristina González
    # npc = npc_4e("Estalian", 
    #              characteristics={"M":4, "WS":31, "BS":37, "S":30, "T":28, "I":36, "Agi":34, "Dex":28, "Int":29, "WP":30, "Fel":32},
    #              starting_skills={"Consume Alcohol":5, "Haggle":5, "Language (Brettonian)":3, "Lore (Estalia)":3, "Sail (Caravel)": 5, "Swim":3},
    #              starting_talents={"Linguistics", "Marksman", "Resistance (Mutation)", "Rover", "Very Strong"})
    # npc.add_career("Soldier", 2)
    # npc.add_career("Riverwarden", 1)
    # npc.add_career("Knight", 2)

    # Doktor Helga Langstrasse
    npc = npc_4e("human")
    npc._add_career_rank("Scholar", 1)
    npc._add_career_rank("Physician", 2)
    npc._add_career_rank("Physician", 3)

    print(npc)

if __name__ == "__main__":
    # execute only if run as a script
    main()