import collections
import random
import re
from math import inf
from collections import Counter

from ..magic4e import Magic4e
from ...data.bestiary import *
from ...data import bot_char_dat
from .skills4 import Skills4
from .careers4 import Careers4
from .talents4 import Talents4
from ..utility.find_best_match import find_best_match

class BuildNPC4:
    """Generate and manage a 4th Edition NPC"""

    def __init__(self, species : str, lore : str = None,
                 characteristics=None, starting_skills=None, starting_talents=None, starting_trappings=None,
                 randomise=True):

        # initialise random number generator with OS (or time) seed
        random.seed()

        # For now we assume if we don't know the species it's a type of human unless contains
        # one of the known species words (i.e. dwarf, halfing, elf or gnome)
        self._species = species

        # Can't use self.known_species because RandomNPC4 has a different list of species it knows
        # but that list doesn't have stats for Reiklanders, etc.
        lookup_species = species.lower()
        species_with_stats = [*species_npc_characteristics_4e.keys(), *species_npc_aliases_4e.keys()]

        if lookup_species in species_with_stats:
            if lookup_species in species_npc_aliases_4e:
                index_species = species_npc_aliases_4e[lookup_species]
            else:
                index_species = lookup_species
        else:
            # Default to human if we don't otherwise understand the species requested
            index_species = 'human'

            # Check if the species text contains any of the known types of species
            # So if 'Dark Elf' is supplied the index_species will be set to 'elf'
            # This could have strange results if someone decides 'human-slayer' is a 
            # species, but that doesn't seem like something worth guarding against!
            for test_species in species_with_stats:
                if test_species in lookup_species:
                    index_species = test_species
                    break
                
        self._index_species = index_species

        # Either use characteristics based on species (see 4th Ed Corebook p.311)
        # or use characteristics passed in by caller
        if not characteristics:
            
            base_characteristics = dict(species_npc_characteristics_4e[index_species])

            # Apply randomisation to the stats
            if randomise:
                for stat,value in base_characteristics.items():
                    if stat!="M":
                        if value>=10:
                            base_characteristics[stat] = (value - 10) + random.randint(1,10) + random.randint(1,10)
                        else:
                            base_characteristics[stat] = random.randint(1,10)

            self._base_characteristics  = base_characteristics
            self._characteristics       = dict(base_characteristics)
        else:
            self._base_characteristics  = characteristics
            self._characteristics       = dict(characteristics)

        # Traits are always set based on species
        self._traits            = species_npc_traits_4e[index_species]
        self._optional_traits   = species_npc_optional_traits_4e[index_species]

        if index_species=="mutant" or index_species=="cultist":
            self._index_species = "human"

        # Record starting skills, talents, etc.
        self._starting_skills    = starting_skills if starting_skills is not None else set() # Need to record these to allow XP calculating
        self._starting_talents   = starting_talents if starting_talents is not None else set()
        self._starting_trappings = starting_trappings if starting_trappings is not None else set()

        self._apply_statmod_stating_talents()
        self._starting_characteristics = dict(self._characteristics) # Apply stat mods before recording

        self._careers_taken     = {}                    # Careers taken and their max rank
        self._career_history    = collections.deque()   # The order in which careers and ranks were taken
        self._skills            = dict(starting_skills) if starting_skills is not None else {}
        self._suggested_talents = set()
        self._talents           = set()
        self._trappings         = set()

        self._lore              = lore
        self._spells            = {}
        
        self._xp_spend          = 0

    @classmethod
    def known_species(cls) -> list:
        """List known species. Most useful for listing 'monsters' that can have careers applied."""
        return [*species_npc_characteristics_4e.keys(), *species_npc_aliases_4e.keys()]

    def __str__(self) -> str:
        retstr = ''
        # Species and most recent career level name
        if self._career_history:
            lastcareer, lastrank = next(reversed(self._career_history))
            lastcareername = Careers4()[lastcareer][f'rank {lastrank}']['name']

            retstr  = self._species.title() + " " + lastcareername + '\n'
            retstr += 'Career history: ' + str(self.career_history) + '\n'

        # Characteristics
        retstr += str(self.characteristics) + '\n'

        # Skills       
        retstr += "Skills: " 
        for key, values in self.skills_verbose.items():
            for value in values:
                retstr += "{} {} [{}+{}], ".format(key, value['total'], value['characteristic'], value['add'])
        retstr += '\n'

        # Talents
        if self.starting_talents:
            retstr += "Starting Talents:  " + str(self.starting_talents) + "\n"
        retstr += "Suggested Talents: " + str(self.suggested_talents) + "\n"
        retstr += "Additional Talents: " + str(self.additional_talents) + "\n"

        # Traits
        retstr += 'Traits: ' + str(self.traits) + '\n'
        retstr += 'Optional Traits: ' + str(self.optional_traits) + '\n'

        # Trappings
        retstr += "Trappings: " + str(self.trappings) + "\n"
        retstr += "Additional Trappings: " + str(self.additional_trappings) + "\n"

        # Verbose
        retstr += "\n\nTalents by Career: " + str(self.talents_by_career) + "\n"
        retstr += "Suggested Talents by Career: " + str(self.suggested_talents_by_career) + "\n"
        retstr += "Additional Talents by Career: " + str(self.additional_talents_by_career) + "\n"

        return retstr

    def _apply_statmod_stating_talents(self):
        """Apply Talents which modify Characteristics if they're in the starting talents list"""
        for talent in self._starting_talents:
            try:
                if Talents4()[talent]['stat_mod']:
                    # Parse the stat mod and apply it
                    tokens = Talents4()[talent]['stat_mod'].split(' ')
                    try:
                        self._characteristics[tokens[1]] += int(tokens[0][1:])
                    except ValueError:
                        self._characteristics[tokens[1]] += self._characteristic_bonus(tokens[0][1:])
            except KeyError:
                # Could mean the talent isn't in our list, or it could mean it doesn't have a stat_mod
                # Or it could be 'Hardy'!
                # Either way we ignore the error
                pass

    @property
    def _get_latest_career_info(self):
        """Get information about the current career rank, i.e. the last one 
           entered by the user
        """
        if self._career_history:
            lastcareer, lastrank = next(reversed(self._career_history))
            return Careers4()[lastcareer][f'rank {lastrank}']
        else:
            return {}

    @property 
    def species(self) -> str:
        """User supplied species, e.g. 'Reiklander Human'"""
        return self._species

    @property
    def species_used(self) ->str:
        """Species used when generating character, e.g. 'Estalian' is converted to 'human'"""
        return self._index_species

    @property
    def careername(self) -> str:
        """The current career name, e.g. 'Wizard Lord', 'Physician's Apprentice', etc."""
        if self._career_history:
            return self._get_latest_career_info['name']
        else:
            return None

    @property 
    def career_history(self) -> list:
        """Career history as a list of career rank name, e.g. {'Novitiate', 'Nun', 'Warrior Priest'}"""
        return [Careers4()[career][f'rank {rank}']['name'] for career,rank in self._career_history]

    @property
    def career_history_unambiguous(self) -> list:
        """Career history as a list of career rank names, but when career changes it is included
           e.g. {'Tax Collector (Bailiff)', 'Bailiff', 'Custodian (Warden)'} """
        career_history_list = list()
        previous_career = ''
        for career,rank in self._career_history:
            rankname = Careers4()[career][f'rank {rank}']['name']
            if career!=previous_career:
                career_history_list.append(f'{rankname} ({career} {rank})')
            else:
                career_history_list.append(rankname)
            
            previous_career = career

        return career_history_list

    @property
    def traits(self) -> list:
        """ Racial traits """
        return sorted(self._traits)

    @property
    def optional_traits(self) -> list:
        """ Optional racial traits """
        return sorted(self._optional_traits)

    @property
    def characteristics(self) -> dict:
        """Characteristics as a dictionary, e.g. {"WS":45, "BS":30, ..., "Fel":35, "W":13}
           Note that wounds are calculated when this function is called
        """
        output_chars = dict(self._characteristics)
        output_chars.update({'W':self._wounds})

        return output_chars

    @property
    def characteristics_base(self) -> dict:
        """The original rolled or passed in  characteristics as a dictionary, e.g. {"WS":45, 
           "BS":30, ..., "Fel":35, "W":13}
           Note that wounds are calculated when this function is called
        """
        output_chars = dict(self._base_characteristics)
        output_chars.update({'W':self._template_wounds(self._base_characteristics)})

        return output_chars

    def _characteristic_bonus(self, charb) -> int:
        """Get the specified characteristic bonus (e.g. 'WSB') of the NPC"""
        def _get_digit(number, n):
            return number // 10**n % 10        

        return _get_digit(self._characteristics[charb[:-1]],1)

    def _template_wounds(self, charactertistics):
        """Calculate wounds based on passed in characteristics, and size"""
        def _get_digit(number):
            return number // 10#10**n % 10

        sb  = _get_digit(charactertistics['S'])
        tb  = _get_digit(charactertistics['T'])
        wpb = _get_digit(charactertistics['WP'])
        wounds = sb + 2*tb + wpb

        if "Size (Tiny)" in self._traits:
            wounds = 1
        elif "Size (Little)" in self._traits:
            wounds = tb
        elif "Size (Small)" in self._traits:
            wounds =  2*tb + wpb
        elif "Hardy" in self._starting_talents: 
            # Use the weirdness of Python's if evaluation to support Hardy
            # It's simply added in the case of creatures of Size (Average)
            # or lower but multiplicative at larger sizes
            wounds += tb
        elif "Size (Large)" in self._traits:
            wounds *= 2
        elif "Size (Enormous)" in self._traits:
            wounds *= 4
        elif "Size (Monstrous)" in self._traits:
            wounds *= 8

        return wounds

    @property
    def _wounds(self):
        """Calculate the NPCs wounds based on their size"""
        wounds =    self._characteristic_bonus('SB') \
                + 2*self._characteristic_bonus('TB') \
                +   self._characteristic_bonus('WPB')

        return self._template_wounds(self._characteristics)

    @property
    def _money(self) -> str:
        """Calculate the money for the trappings from the NPC's most recent career and rank
           This fully determined by Status.
        """
        # Get the most recent career and rank, and use that to find the NPC's status
        lastcareer, lastrank = next(reversed(self._career_history))
        status = Careers4()[lastcareer][f'rank {lastrank}']['status']

        # Use some string manipulation to turn status into money
        tokens = status.split(' ')
        money = f"{tokens[1]}d10 {tokens[0]}"

        return money

    @property
    def trappings(self) -> list:
        """All trappings appropriate to the current career rank. This includes all 
           trappings at that rank and lower, but not outside the current career.
           Currently class trappings are not included.
        """
        # Most recent career and rank
        if self._career_history:
            lastcareer, lastrank = next(reversed(self._career_history))
            
            trappings = set() 
            for i in range(1,lastrank+1):
                trappings.update( Careers4()[lastcareer][f'rank {i}']['trappings'] )

            trappings.update( [self._money] )
            trappings = trappings.union(self._starting_trappings)

            # Remove 'None' from trappings. Stupid penniless peasants!
            # Note even peasants always have 2d10 Brass
            trappings.discard('None')

            return sorted(trappings)
        else:
            return list()

    @property
    def additional_trappings(self) -> list:
        """Some complex logic to include trappings from previous careers.

        The idea here is that we include all previous trappings so long as there 
        wasn't a fall in status. So a Scholar (Silver) only gets to keep what they
        had as a Student (Brass) if they become a mere Peasant (Brass)
        """

        # Process careers history
        # Find unique careers and find details about careername, rank, and status for later
        unique_careers  = set()
        career_status_history  = []
        for careername, rank in self._career_history:
            unique_careers.update([careername])

            status_tokens = Careers4()[careername][f'rank {rank}']['status'].split(' ')
            career_status_history.append({"name":careername, "rank":rank, "status":status_tokens[0]})

        # If we've only been in one career then there can't be additional trappings
        if len(unique_careers)==1:
            return {}

        # Keep track of any additional trappings by status
        additional_trappings_by_status = {"Brass":set(), "Silver":set(), "Gold":set()}

        # Run through the career history
        # If there's a status drop then remove all higher status stuff
        # In either case add any new trappings
        last_status = "Brass"
        for career_status in career_status_history:
            name   = career_status["name"]
            rank   = f'rank {career_status["rank"]}'
            status = career_status["status"]

            # If status has fallen remove all trappings at the higher status
            status_order = {"Brass":1,"Silver":2,"Gold":3}
            if status_order[status]<status_order[last_status]:
                additional_trappings_by_status["Gold"] = set()

                if status == "Brass":
                    additional_trappings_by_status["Silver"] = set()

            last_status = status

            for i in range(1,career_status['rank']+1):
                additional_trappings_by_status[status].update(set(Careers4()[name][f'rank {i}']['trappings']))

        # Combine all the additional trappings into one list
        additional_trappings =   additional_trappings_by_status["Brass"] \
                                .union(additional_trappings_by_status["Silver"]) \
                                .union(additional_trappings_by_status["Gold"])

        # Remove any trappings already in the definite trappings
        additional_trappings -= set(self.trappings)
        additional_trappings.discard("None")

        # Return a sorted list
        return sorted(additional_trappings)


    def __template_gettalents(self, selector):
        out_talents = {}
        for talent in sorted(selector):
            # Check if this talent is in the talent list
            talent_index = talent
            if talent in Talents4().get_talents():
                # It is
                out_talents[talent] = dict(Talents4()[talent])
            else:
                # It isn't... That might mean it's a group talent
                talentfound = False
                for shortform in bot_char_dat.talent_groups_4e:
                    if talent.startswith(shortform):
                        out_talents[talent] = Talents4()[shortform]
                        talent_index = shortform
                        talentfound = True
                        break
                
                if not talentfound:
                    out_talents[talent] = {}

            try:
                talentmax = Talents4()[talent]['max']
                if talentmax == None:
                    out_talents[talent]['max'] = inf
                elif not isinstance(talentmax,int):
                    out_talents[talent]['max'] = self._characteristic_bonus(Talents4()[talent]['max'])             
            except KeyError: # Remove when all telents in data file
                pass

        return out_talents

    @property
    def talents(self) -> dict:
        """All talents available to the NPC across all careers and ranks taken, and 
           including starting talents (if any).

           Returns a dictionary where the key is the talent name, and each value is
           a sub-dictionary containing information about the associated tests
           (if any), and the calculated max times the talent may be taken (usually 
           based on a characterisic bonus).
        """
        return self.__template_gettalents(set(self._talents) + self._starting_talents)

    @property
    def starting_talents(self) -> dict:
        """Starting talents (if any).

           Returns a dictionary where the key is the talent name, and each value is
           a sub-dictionary containing information about the associated tests
           (if any), and the calculated max times the talent may be taken (usually 
           based on a characterisic bonus).
        """
        return self.__template_gettalents(self._starting_talents) 

    @property
    def formatted_starting_talents(self) -> dict:
        """Starting talents (if any), formatted to indicate if a stat_mod has been 
           applied to a characteristic. For example, if Marksman has been taken as a
           as a starting talent the +5 BS will have been factored into the characteristics
           of the NPC, and the dictionary returned will include a key '*Marksman*'
           (rather than 'Marksman')

           Returns a dictionary where the key is the talent name, and each value is
           a sub-dictionary containing information about the associated tests
           (if any), and the calculated max times the talent may be taken (usually 
           based on a characterisic bonus).
        """
        starting_talents = self.starting_talents
        formatted_talents = {}
        for talent in starting_talents:
            try:
                if Talents4()[talent]['stat_mod']:
                    formatted_talents[f'*{talent}*'] = starting_talents[talent]
                else:
                    formatted_talents[talent] = starting_talents[talent]
            except KeyError:
                # Group talents make things go bang. Ignore those errors
                formatted_talents[talent] = starting_talents[talent]
    
        return formatted_talents 

    @property 
    def suggested_talents(self):
        """A talent from each career level. Generally randomly chosen, but the careers file
           includes suggested Talents for some career ranks which are then used instead of a 
           randomly selected one."""
        # We don't remove starting talents from the list, because career talents can potentially 
        # be taken multiple times without needing GM approval. Though since this is an NPC the
        # GM could probably approve!
        return self.__template_gettalents(self._suggested_talents)

    @property
    def additional_talents(self):
        """All the other talents (not in the suggested list) that the NPC can access."""
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
            careerrankname = Careers4()[career][f'rank {rank}']['name']
            true_history.append(careerrankname)

        avail_history = set()
        for career,rank in self._careers_taken.items():
            avail_history.update([(career, i) for i in range(1,rank+1)])

        # Go through the career ranks for all could contribute talents
        # Add a star to the end of the careername if it was not really taken
        for careername,rank in avail_history:
            careerrank = Careers4()[careername][f'rank {rank}']
            careerrankname = careerrank['name']

            if careerrankname not in true_history:
                careerrankname += '*'

            out_talents[careerrankname] = self.__template_gettalents(selector(careerrank))

        return out_talents

    @property 
    def talents_by_career(self):
        """All talents available to the NPC sorted by career"""
        selector = lambda careerrank : careerrank['talents']

        return self.__template_by_career(selector)

    @property
    def suggested_talents_by_career(self):
        """All suggested talents available to the NPC sorted by career"""
        selector = lambda careerrank : careerrank['npc_suggested_talents']

        return self.__template_by_career(selector)
      
    @property
    def additional_talents_by_career(self):
        """All additional talents available to the NPC sorted by career,
           i.e. all talents - suggested talents"""
        selector = lambda careerrank : set(careerrank['talents']) - set(careerrank['npc_suggested_talents'])

        return self.__template_by_career(selector) 

    # We return two takes on the NPC's skills list. The first is a simple one which is just ("skill:value") pairs
    # The second is a more complex dictionary of the form 
    #    '"Melee (Any)" : {"characteristic":"WS", "total":45, "add":10}'
    # where total is the same as the value in the simple case and add is the amount to be added to the 
    # characteristic 
    def __template_skills(self, verbose=False):
        simple_skills  = collections.defaultdict(list)
        complex_skills = collections.defaultdict(list)
        for skill, value in sorted(self._skills.items()):
            # Drop everything before brackets to make life easier
            skillbits = re.split('\(|\)',skill)
            baseskill = skillbits[0].strip()

            # Handle advanced skills, or more specifically those that have an "Any" specialisation
            source = None
            if len(skillbits)>1:
                specialisation = skillbits[1].strip()
                if specialisation[0] == '[':
                    source = specialisation[1:-1]
                    specialisation = "Any"

                fullskill = f"{baseskill} ({specialisation})"
            else:
                fullskill = baseskill

            skillchar  = Skills4()[baseskill]['characteristic']
            skilltotal = self._characteristics[skillchar] + value

            simple_skills[fullskill].append(skilltotal)
            complex_skills[fullskill].append({"total":skilltotal, "characteristic":skillchar, "add":value, "source":source})

        if verbose:
            return complex_skills
        else:
            return simple_skills

    @property
    def skills(self):
        """All the NPC's skills as a dictionary of the form {"skillname":[value]}
           In most case the list of values will have only one item, e.g. {"Charm":[55]}
           but general skills with an (Any) may need to be recorded seperately
           in which case the result could be {"Melee (Any)":[55, 44]}
        """
        return self.__template_skills(verbose=False)

    @property
    def skills_verbose(self):
        """All the NPC's skills as a dictionary of lists of dictionaries the form
            {"skillname": [{"total":skilltotal, "characteristic":skillchar, "add":value, "source":career_and_rank}],
            where "characteristic" : str is the characteristic associated with the skill,
            "add" : int is what is added to the characteristic to get the skill total,
            "source" : str is the source career and rank (e.g. 'Scholar 2')
        """
        return self.__template_skills(verbose=True)

    @property
    def xp_spend(self):
        """Estimate of the XP spend that would be required to create this NPC"""
        # Careers completed
        xp = max(100 * (len(self.career_history)-1),0)

        # Characteristics
        characteristic_advance_costs = [25,30,40,50,70,90,120,150,190,230,280,330,390,450,520,590,670,750]
        for char,value in self._characteristics.items():
            advance_to_cost = value - self._starting_characteristics[char]

            for i in range(advance_to_cost, 0,-1):
                sac_idx = int((i-1) / 5)

                xp += characteristic_advance_costs[sac_idx]
        
        # Skills
        skill_advance_costs = [10,15,20,30,40,60,80,110,140,180,220,270,320,380,440,510,580]
        for skill,value in self._skills.items():
            advance_to_cost = value

            if skill in self._starting_skills:
                advances_no_cost = self._starting_skills[skill]
            else:
                advances_no_cost = 0
        
            for i in range(advance_to_cost, advances_no_cost,-1):
                sac_idx = int((i-1) / 5)

                xp += skill_advance_costs[sac_idx]

        # Talents
        xp += 100 * len(self.suggested_talents)

        return xp

    def add_career_rank(self, careername, rank) -> None:
        """Add a single career rank to the NPC, e.g. 'Soldier 2'"""

        # Validate input
        if rank<1 or rank>4:
            raise IndexError(f'Rank less than 0 or greater than 4. Rank was {rank}')

        try:
            Careers4()[careername]
        except KeyError:
            raise KeyError(f"{careername} is not a valid career name")

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
            careerrank = Careers4()[careername][f'rank {i}']

            # Apply all applicable characteristic advances
            for advance in careerrank['advances']:
                self._characteristics[advance] += 5
            
            # Either start tracking a new skill or add to an existing one
            for skill in careerrank['skills']:
                modskill = skill.replace("(Any)",f"([{careername} {i}])")

                if modskill in self._skills:
                    self._skills[modskill] += 5
                else:
                    self._skills[modskill] = 5

            # We only need to add new talents if we've not been in this rank before
            # (Remember we visit ranks multiple times to up skills and characteristics)
            if i==rank:
                # Update the list of suggested talents, but don't add any more that can only be taken once
                onetakers = set()
                for talentname in (self._suggested_talents.union(self._starting_talents)):
                    try:
                        talent_info = Talents4()[talentname]
                        if isinstance(talent_info['max'],int) and talent_info['max']==1:
                            onetakers.update([talentname])
                    except KeyError:
                        pass    # Ignore key errors, they ought to come from talent group issues

                modified_suggested_talents = set(careerrank['npc_suggested_talents']) - onetakers
                modified_available_talents = list(set(careerrank['talents']) - onetakers)
                
                # If there are no suggested talents then we're still required to pick one talent per rank
                # And sometimes the suggested talent is from an earlier career rank
                # So we pick a random talent from those that are valid
                if not modified_suggested_talents or not set(modified_available_talents).intersection(modified_suggested_talents):
                    self._suggested_talents.update(random.choices(modified_available_talents))

                if modified_suggested_talents:
                    self._suggested_talents.update(modified_suggested_talents)

                # And update the list of all available talents
                self._talents.update(modified_available_talents)

        # Update career history
        self._careers_taken[careername] = rank
        self._career_history.append((careername,rank))


    def add_career(self, careername, rank) -> None:
        """ Utility function to apply all career ranks up to the specified one to an NPC.
            So calling with Soldier 3 will apply Soldier 1, Soldier 2, and Soldier 3
        """
        careername = careername.title()
        # Validate input
        career = Careers4()[careername] # Blow up early if career not in list of careers
        if rank<1 or rank>4:
            raise IndexError('Rank less than 0 or greater than 4')

        for i in range(1, rank+1):
            self.add_career_rank(careername, i)

    def advance_skill(self, skill, value):
        """Allow a skill to be advanced manually. Useful for tweaks or out-of-career advances"""
        if skill in self._skills:
            self._skills[skill] += value
        else:
            self._skills[skill] = value


    def _check_lore(self):
        if self._lore == None:# and 'Wizard' in self._careers_taken.keys():
            self._lore = random.choice(['Lore of Beasts', 'Lore of Death', 'Lore of Fire',
                                        'Lore of Heavens', 'Lore of Life', 'Lore of Light', 
                                        'Lore of Metal', 'Lore of Shadows'])

        m4 = Magic4e()
        wind_name = m4[self._lore]['names']['wind']

        if 'Channelling (Any Colour)' in self._skills:
            self._skills[f'Channelling ({wind_name})'] = self._skills.pop('Channelling (Any Colour)')

        if 'Arcane Magic (Any Arcane Lore)' in self._suggested_talents:
            self._suggested_talents.add(f'Arcane Magic ({wind_name})')
            self._suggested_talents.remove('Arcane Magic (Any Arcane Lore)')

        if 'Arcane Magic (Any Arcane Lore)' in self._talents:
            self._talents.add(f'Arcane Magic ({wind_name})')
            self._talents.remove('Arcane Magic (Any Arcane Lore)')


    def _choose_spells(self, spell_lists):
        # Remove any lores which are already at max spells
        if 'Arcane Lore (Any)' in spell_lists:
            spell_lists.append(self._lore)
            spell_lists.remove('Arcane Lore (Any)')

        #choose four spells from the available lists. First thing is to distribute them
        spells_from = random.choices(spell_lists, k=4)

        for item in spells_from:
            if item not in self._spells:
                self._spells[item] = set()

        m4 = Magic4e()
        for k,v in Counter(spells_from).items():
            self._spells[k].update( m4.get_random_spells(k.lower(),v).keys() )


    def _format_spells(self):
        formatted_text = ""
        for spell_list in self._spells:
            formatted_text += f'__{spell_list}__: {", ".join(self._spells[spell_list])}\n'

        return formatted_text.strip()


    @property
    def spells(self):
        # Scan through the careers in the history and find each that has a spell-list associated with it
        spells = []
        uch = set(self._career_history)
        for career in uch:
            careerrank = Careers4()[career[0]][f'rank {career[1]}']
            if 'spell-lists' in careerrank:
                self._choose_spells(careerrank['spell-lists'])

        return self._format_spells()