import itertools
import random
from typing import List, Mapping, Tuple

from .npc.buildNPC4 import BuildNPC4
from .npc.randomNPC4 import RandomNPC4

from .npc.careers4 import Careers4
from .npc.skills4 import Skills4
from .npc.talents4 import Talents4

from .npc import skill_talent

from .utility.convert_to_superscript import *

import sys, traceback

class NPC4e:
    """ Make either a fully defined or randomly generated NPC"""

    def __init__(self,
                 species : str=None,
                 careers : list=None,
                 type    : str=None,
                 age     : str=None,
                 filter  : str=None,
                 lore    : str=None,
                 characteristics   : dict=None,
                 initial_skills    : dict=None,
                 initial_talents   : dict=None,
                 initial_trappings : dict=None):
        """
        Create a new WFRP 4th edition NPC.

        Parameters
        ----------
        All parameters are optional. If none are given a completely random NPC will be generated.

        random:  bool, optional
        whether to build an NPC with user-defined career history (random=False), or one with a randomly 
        generated career history.
        
        species: str, optional
        the species of the NPC. Note that the defined and random NPCs have different species possible. 
        The class will return an error explanation if the user inputs a species the associated generator 
        can't handle
        
        careers: list, optional
        either a list of tuples of (career, level) for the defined NPC builder, **OR** a single tuple 
        of (career, level) for the random NPC builder. In the latter case the behaviour varies depending 
        on the level in the tuple. If the level is 1 then the career is used as a starting career, if 
        the level is >1 then it becomes the final (i.e. target) career of the NPC
        
        type: str, optional
        NOT IMPLEMENTED. As an alternative to careers, set a broad type of NPC such as 'medical', or 'holy'

        ages: str, optional
        a string which applies to randomly generated NPCs and means that the probabilities are adjusted 
        to make shorter or longer career histories more likely

        filter: str, optional
        apply a filter to *presentation* of the NPC, emphasing a particular aspect, currently valid 
        values are 'combat' and 'social'
        NOTE: the filter is the only option that can be changed once an NPC is generated

        characteristics:
        Override the generation of characteristics and input them directly. Takes a dictionary of the 
        form {"M":4, "WS":31, "BS":37, "S":30, "T":28, "I":36, "Agi":34, "Dex":28, "Int":29, "WP":30, "Fel":32}

        initial_skills:
        Directly add skills to the NPC. Takes a dictionary of the form {"Consume Alcohol":5, "Haggle":5}

        initial_talents:
        Directly add talents to the NPC. Takes a list of the form {"Linguistics", "Marksman"}
        NOTE: characteristics are modified by talents which do so, e.g. Marksman

        initial_trappings:
        Directly add talents to the NPC. These are always printed at the end, irrespective of status, etc.
        """

        # Check for ages we understand
        if age=='young' in age: young = True 
        else: young = False
        self._age = age

        # If no species is set then we choose a random species from the probabilities defined
        # in the rulebook for PCs. That means we never generate a random 'monster' if no
        # species is defined
        if not species:
            species = RandomNPC4.random_species()

        # If no career is defined then engage the random generator
        if not careers:
            careers = ['any']

        self._error            = None
        self._error_diagnostic = None
        try:
            # Deduplicate the input career list since something like ['any','any','any']
            # will cause problems later. We have to be careful though as ['any', ('Guard',2), 'any']
            # is valid. We only want to remove duplicates where they're next to each other
            dedup_careers = [k for k, g in itertools.groupby(careers)]
            firstcareer = True

            # Search the input career list for 'any'
            # If it's not present then this is trivial and we just pass everything to the defined NPC builder
            # Then check the species based on this information to see if it's something the available classes
            # can handle
            if not 'any' in dedup_careers:
                # We can immediately build this NPC
                self._npc = BuildNPC4(species=species,
                                        lore=lore, 
                                        characteristics=characteristics, 
                                        starting_skills=initial_skills, 
                                        starting_talents=initial_talents,
                                        starting_trappings=initial_trappings)
                for career in dedup_careers or []:
                    self._add_career(firstcareer, career)
                    firstcareer = False
            else:
                # There is a random element to this NPC
                # The easiest case is one where the only input is any
                # In that case just generate a completely random NPC
                self._npc = RandomNPC4(species=species, 
                                    starting_career=None, 
                                    target=None, 
                                    young=young, 
                                    lore=lore,
                                    characteristics=characteristics, 
                                    starting_skills=initial_skills, 
                                    starting_talents=initial_talents,
                                    starting_trappings=initial_trappings,
                                    init_only=True)

                target_career = None
                
                while dedup_careers:                                             
                    careers_left = len(dedup_careers)
                    careers_copy = list(dedup_careers)

                    if careers_left==1:
                        if careers_copy[0]=='any':
                            self._npc._add_random_careers(None,young, force_first=True)
                        else:
                            self._add_career(firstcareer, careers_copy[0])
                        dedup_careers = []
                    elif careers_left==2:
                        # This is either ['any',(career,level)], [(career,level),(career,level)] or [(career,level),'any']
                        if careers_copy[0]=='any':
                            target_career = {'career': careers_copy[1][0], 'rank': careers_copy[1][1]}
                            self._npc._reverse_random_careers(target_career,young)

                            dedup_careers = dedup_careers[2:] # Remove 'any' and the subsequent career
                        elif careers_copy[1]=='any':
                            # Then add the career path which is random until the end
                            self._prep_career_history(firstcareer, careers_copy)

                            self._npc._add_random_careers(careers_copy[0],young, force_first=True)
                            dedup_careers = []
                        else:
                            self._add_career(firstcareer, careers_copy[0])
                            dedup_careers = dedup_careers[1:]
                    else:
                        # Must be 3 or greater
                        if careers_copy[1] == 'any':
                            # Must be of form [(career,n), 'any', (career,n)]
                            self._prep_career_history(firstcareer, careers_copy)
                            self._npc._span_random_careers(careers_copy[0], careers_copy[2])
                            dedup_careers = dedup_careers[3:]
                        else:
                            # Must be of form ['any', (career,n), 'any']
                            career_name = careers_copy[1][0]
                            career_rank = careers_copy[1][1]

                            if career_rank>1:
                                target_career = {'career': career_name, 'rank': career_rank-1}
                            else:
                                target_career = {'career': career_name, 'rank': career_rank}

                            self._npc._reverse_random_careers(target_career,young)
                            dedup_careers = dedup_careers[1:]

                    firstcareer = False

            self._filter = filter
            self._format()
        except RandomNPC4.NoCareersSpecies as e:
            self._error = str(e)
        except Exception as e:
            print('Exception triggered')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self._error_diagnostic = '\n'.join(traceback.format_exception(e, exc_value, exc_traceback))

    def _prep_career_history(self, firstcareer, careers_copy):
        career_name = careers_copy[0][0]
        career_rank = careers_copy[0][1]
        if firstcareer and career_rank>1: 
            for i in range(1,career_rank):
                self._npc.add_career_rank(career_name, i)

    def _add_career(self, firstcareer, career):
        if firstcareer:
            self._npc.add_career(career[0].title(), career[1])
        else:
            self._npc.add_career_rank(career[0].title(), career[1])

    @property
    def error_msg(self) -> str:
        """ Helpful error messages for Jodri users"""
        return self._error

    @property
    def error_msg_diagnostic(self) -> str:
        """ Helpful error messages for Jodri developers """
        return self._error_diagnostic

    @classmethod
    def known_careers(cls) -> List[str]:
        """ All known careers """
        return Careers4().careers

    @classmethod
    def known_career_levels(cls) -> dict:
        """ All known career levels. Note that some may be the same, e.g.  Nun and 
            Warrior Priest both start with Novitiate """
        return Careers4().career_levels

    @classmethod
    def known_filters(cls) -> list:
        """ Modes that the filters can use when presenting an NPC. Does not affect the 
            NPC actually built """
        return ['combat', 'social']


    @classmethod
    def known_humans(cls) -> List[str]:
        """ Known types of human which can be used by the random NPC builder """
        return RandomNPC4.known_humans()

    @classmethod
    def known_ages(cls) -> List[str]:
        return ['young']

    @classmethod
    def known_species(cls) -> List[str]:
        """ List known species of all kind, including the known types of human """
        known_species_build  = set([x.lower() for x in cls.known_species_build()])
        known_species_random = set([x.lower() for x in cls.known_species_random()])
        known_species = set(known_species_build.union(known_species_random))

        # With or without known types of humans? Comment or uncomment these lines
        known_humans  = set([x.lower() for x in cls.known_humans()])
        known_species -= known_humans

        return sorted( list(known_species) )

    @classmethod
    def known_species_build(cls):
        """ Known species which can be used by the directed NPC builder """
        return BuildNPC4.known_species()

    @classmethod
    def known_species_random(cls) -> List[str]:
        """ Known species which can be used by the random NPC builder """
        return RandomNPC4.known_species()

    @classmethod
    def known_types(cls) -> List[str]:
        """ NOT IMPLEMENTED!!! Broad categories of NPC as an alternative to careers, e.g. 'medical', 'religious' """
        return None

    @property
    def filter(self) -> str:
        """ The current presentation filter set on the NPC """
        return self._filter

    @filter.setter
    def filter(self, filter: str):
        """ Change the presentation of the NPC, simplifying it to show social or combat relevant stats """
        self._filter = filter
        self._format()

    def _format_talents(self, talents) -> str:
        """ Return all talents as a footnoted list joined with commas """
        return ', '.join('{}{}'.format(convert_number_to_footnote(v.get('skill_ref', 0)), k) for k, v in talents.items())

    def _format(self):
        """ Apply a filter to the NPC, allowing presentation to be simplified """
        type = self._filter

        # Skills
        skills_list = list()
        filtered_skills_dict = Skills4().filter(self._npc.skills_verbose, type)

        # Talents
        t4 = Talents4()
        if self._npc.talents_initial:
            talents_initial = t4.filter(
                self._npc.formatted_starting_talents, type)
        else:
            talents_initial = {}

        talents_suggested = t4.filter(self._npc.talents_suggested, type)
        talents_additional = t4.filter(self._npc.talents_additional, type)

        # Association between skills and talents
        filtered_skills_dict, talents_initial, index = skill_talent.associate(
            filtered_skills_dict, talents_initial,   starting_index=1)
        filtered_skills_dict, talents_suggested, index = skill_talent.associate(
            filtered_skills_dict, talents_suggested,  starting_index=index)
        filtered_skills_dict, talents_additional, index = skill_talent.associate(
            filtered_skills_dict, talents_additional, starting_index=index)

        # Format skills data
        for skill, values in filtered_skills_dict.items():
            for value in values:
                superscripts = sorted(list(value.get('talent_ref', {0})))
                if not superscripts[0] == 0:
                    footnotes = [convert_number_to_footnote(i) for i in superscripts]
                    superscript = ' '.join(footnotes)
                    superscript = convert_to_superscript(f'({superscript})')
                else:
                    superscript = ''

                if value['source'] and len(values) > 1:
                    skills_list.append("{!s}: {!r}{} [{}; +{}]".format(
                        skill, value['total'], superscript, value['source'], value['add']))
                else:
                    skills_list.append("{!s}: {!r}{}".format(
                        skill, value['total'], superscript))
                    #print("{}".format(', '.join("{!s}: {!r}".format(key,val) for (key,val) in npc.skills.items())))

        self.__skills_crossedref = skills_list
        self.__talents_applied_crossedref = talents_initial
        self.__talents_suggested_crossedref = talents_suggested
        self.__talents_additional_crossedref = talents_additional

    ##################################################################################################
    # Output properties

    @property
    def age(self) -> Tuple[str, int]:
        if self._age == 'young':
            age = random.randint(12,19)
        elif self._age == 'old':
            age = random.randint(61,99)
        else:
            age = 12
            # For each career level add a random number of years to the age based on
            # the career level
            for career, level in self._npc._career_history:
                if level==0:
                    age += random.randint(1,3)
                elif level==1:
                    age += random.randint(3,5)
                elif level>1:
                    age += random.randint(5,10)
            
            # If the character's final career level is greater than 1 then add
            # an additional random age factor which could make them any age between
            # their current unmodified age and 70. But include a random factor that
            # means some old NPCs can still be inexperienced
            if level>1 or random.randint(0,100)<10:
                age += random.randint( -2, max(0,70-age) )
            else:
                age += random.randint( -1, max(0,20-age) )

        # Turn the age in years into a description, i.e. 'young', 'mature', 'old'
        age_descrip = 'mature'
        if age<20: age_descrip = 'young'
        elif age>=60: age_descrip = 'old'

        # Compensate for species when return an age
        # The extra randint is so that every member of the species isn't suspiciously a multiple
        # of some integer in age
        if 'elf' in self._npc._index_species.lower():
            age = (age*5) + random.randint(0,4)
        elif self._npc._index_species.lower() in ['dwarf', 'halfling']:
            age = (age*2) + random.randint(0,1)

        return (age_descrip, age)

    @property
    def careername(self) -> str:
        """ The final careername of the NPC """
        return self._npc.careername

    @property
    def career_history_unambiguous(self) -> str:
        """ The career history of the NPC with ambiguities resolved """
        return ' \u2192 '.join(self._npc.career_history_unambiguous)

    @property
    def characteristics(self) -> dict:
        """ The NPC's characteristics """
        return self._npc.characteristics

    @property
    def skills(self) -> str:
        """ A skills list, formatted with footnotes linking to taletnts, and joined by commas """
        return ', '.join(self.__skills_crossedref)

    @property
    def species(self) -> str:
        """ The notional species of the NPC, e.g.. if Estalian was input the generator may  
            have used 'human' rules. This function will return 'Estalian' """
        return self._npc.species

    @property
    def species_used(self) -> str:
        """ The species actually used by the NPC generator, i.e. if Estalian was input the 
            generator may have used 'human' rules. This function will return 'human' """
        return self._npc.species_used.title()

    @property
    def statblock(self) -> str:
        """ The formatted (as a grid) statblock of the NPC, showing starting characteristics
            which do include modifications like Savvy, and final characteristics """
        outstr = "`|{}|`\n".format(
            '|'.join([f'{x:>3}' for x in self._npc.characteristics.keys()]))
        outstr += "`|{}|`\n".format(
            '|'.join([f'{x:3}' for x in self._npc.characteristics_base.values()]))
        outstr += "`|{}|`".format(
            '|'.join([f'{x:3}' for x in self._npc.characteristics.values()]))

        return outstr

    @property
    def talents_initial(self) -> str:
        """ Any talents passed into the NPC generator. Where appropriate these will have 
            been applied, e.g. Suave. The string returned is formatted with italics for
            stat modifications applied, with footnotes linking to skills, and joined with
            commas. """
        return self._format_talents(self.__talents_applied_crossedref)

    @property
    def talents_suggested(self) -> str:
        """ Talents suggested during the build of the NPC. These are generated randomly
            one per career level, except where the careers data overrides. The string 
            returned is formatted with footnotes linking to skills, and joined with
            commas. """
        return self._format_talents(self.__talents_suggested_crossedref)

    @property
    def talents_additional(self) -> str:
        """ Talents the NPC could have picked up in its career history, excluding those
            already mentioned in the initial or suggested talents. The string 
            returned is formatted with footnotes linking to skills, and joined with
            commas. """
        return self._format_talents(self.__talents_additional_crossedref)

    @property
    def traits(self) -> str:
        """ Traits are taken without modification from the bestiary data """
        return ', '.join(self._npc.traits)

    @property
    def traits_optional(self) -> str:
        """ Optional traits are taken without modification from the bestiary data """
        return ', '.join(self._npc.optional_traits)

    @property
    def trappings(self) -> str:
        """ The final trappings of the NPC, determined purely by their final career level 
            and including any initial trappings."""
        return ', '.join(self._npc.trappings)

    @property
    def trappings_additional(self) -> str:
        """ Trappings accumulated over the couse of the whole career history.
        
            This is generated by accumulating all trappings during the NPC's career history, 
            and dropping those no longer appropriate when Status drops. """
        return ', '.join(self._npc.additional_trappings)

    @property
    def xp_spend(self) -> int:
        """XP required to build this NPC. Note that this includes the cost of the suggested
           talents but does not include XP discounts from talents such as Artistic"""
        return self._npc.xp_spend

    @property
    def spells(self) -> str:
        """ The spells known to the NPC (if any) """
        return self._npc.spells

    @classmethod
    def help_message(cls) -> str:
        return """Generates a fully described 4e non-player character with a career path and stats, plus info on appearence, background, family, etc., taking account of any info provided in the command. NPCs may be generated with user-defined species and career path, random species and career path, or a combination of the two.
The syntax is:

`jodri:npc4 [species] [<career(s)>] [<place>] [<info>]`

... where <species> can be any 4e playable species or human variant or any race from the core rulebook's bestiary, 
....<career(s)> can be a series of career ranks (e.g., `scholar 3`) or career level names (e.g., `professor`) between which Jodri will insert valid career steps if required. Use of the `any` keyword will insert a random career (only valid for playable races).
... <place> can specify a place, e.g., Nuln (see help places for more info)
... and <info> can specify further NPC details (see NPC info below for more info)."""

    @classmethod
    def examples_message(cls) -> str:
        return """> `j:npc4` a completely random NPC (equivalent to `j:npc4 any`)
> `j:npc4 dwarf` a dwarf NPC with a random career path (equivalent to `j:npc4 dwarf any`)
> `j:npc4 fellow` an NPC (of random race) with career path: `student → scholar → fellow`
> `j:npc4 fimir guard 2` a fimir NPC with career path: `sentry → guard`
> `j:npc4 middenlander merchant witch23` a human Middenlander with career path: `trader → merchant → witch → wyrd`
> `j:npc4 reiklander any scholar3` a human Reiklander with a random career path that ends with `Scholar 3` (i.e., `Fellow`)
> `j:npc4 wood elf ghost strider any` a wood elf NPC with an initial career path of `forest ranger → ghost strider`, followed by a random onward career path
> `j:npc4 stormvermin any` not a valid command as only playable races may have random career paths"""

    @classmethod
    def info_message(cls) -> str:
        return """
Jodri understands:
> Nationality: border princes / bretonnian / estalian / imperial / kislevite (ungol / gospodar) / norse / tilean
> Region: e.g., reikland, skaeling, brionne, magritta, etc.
> Birthplace: e.g., Nuln, Tobaro, etc. (check if I know about a place using j:lookup <place>)
> Life Stage: boy / girl, young / mature / old, married / single
> Build: emaciated / skinny / slight / slim / average / stocky / bulky / fat / huge (and tall / small)

NPCs are generated according to the rules in the corebook p.314 ("Random Creatures and Custom PC Species") and Enemy in Shadows p.144 ("NPCs").

Additional notes:
- Characteristic modifying suggested or additional talents are not applied to the NPC.
- The XP spend includes only characteristic and skill advances. Talents are not included.

(Many thanks to @Monarda for this command!)"""

    @classmethod
    def help_messages(cls) -> List[tuple]:
        big_string = """~~~NPC4~~~
Generates a fully described 4e non-player character with a career path and stats, plus info on appearence, background, family, etc., taking account of any info provided in the command. NPCs may be generated with user-defined species and career path, random species and career path, or a combination of the two.
The syntax is:

`jodri:npc4 [species] [<career(s)>] [<place>] [<info>]`

... where <species> can be any 4e playable species or human variant or any race from the core rulebook's bestiary, 
....<career(s)> can be a series of career ranks (e.g., `scholar 3`) or career level names (e.g., `professor`) between which Jodri will insert valid career steps if required. Use of the `any` keyword will insert a random career path (only valid for playable races).
... <place> can specify a place, e.g., Nuln (see help places for more info)
... and <info> can specify further NPC details (see NPC info below for more info).

~~~NPC4 Examples~~~
> `j:npc4` a completely random NPC (equivalent to `j:npc4 any`)
> `j:npc4 dwarf` a dwarf NPC with a random career path (equivalent to `j:npc4 dwarf any`)
> `j:npc4 fellow` an NPC (of random race) with career path: `student → scholar → fellow`
> `j:npc4 fimir guard 2` a fimir NPC with career path: `sentry → guard`
> `j:npc4 middenlander merchant witch23` a human Middenlander with career path: `trader → merchant → witch → wyrd`
> `j:npc4 reiklander any scholar3` a human Reiklander with a random career path that ends with `Scholar 3` (i.e., `Fellow`)
> `j:npc4 wood elf ghost strider any` a wood elf NPC with an initial career path of `forest ranger → ghost strider`, followed by a random onward career path
> `j:npc4 stormvermin any` not a valid command as only playable races may have random career paths
> `j:npc young emaciated mutated reikland rat catcher`

~~~NPC4 Info~~~
Jodri understands:
> Nationality: `border princes` / `bretonnian` / `estalian` / `imperial` / `kislevite` (`ungol` / `gospodar`) / `norse` / `tilean`
> Region: e.g., `reikland`, `skaeling`, `brionne`, `magritta`, etc.
> Birthplace: e.g., `Nuln`, `Tobaro`, etc. (check if I know about a place using `j:lookup <place>`)
> Life Stage: `boy` / `girl`, `young` / `mature` / `old`, `married` / `single`
> Build: `emaciated` / `skinny` / `slight` / `slim` / `average` / `stocky` / `bulky` / `fat` / `huge` (and `tall` / `small`)
> Imperial Pronunciation: turn it off using `nopro`
...and many other aspects of an npc can be specified using =: e.g., `eyes=Grey-Green`, `name=Hans`, `surname=Schmeckl`, `god=Sigmar`, `mutations=4`, etc.

~~~NPC4 Explanations~~~
NPCs are generated according to the rules in the corebook p.314 ("Random Creatures and Custom PC Species") and Enemy in Shadows p.144 ("NPCs").

Additional notes:
- Characteristic modifying suggested or additional talents are not applied to the NPC.
- The XP spend includes only characteristic and skill advances. Talents are not included.

(Many thanks to @Monarda for this command!)"""


        # Split the big help text message into lines
        little_strings = big_string.splitlines(True)

        # Divide the lines into a title (may be blank) and chunks of less than 1024 characters
        output_strings = []
        title = ''
        chunk = ''
        for line in little_strings:
            # See if we've detected a new title
            if line.strip().startswith('~~~') and line.strip().endswith('~~~'):
                # We have a new title so we need to start a new tuple
                # and store the old tuple (if it exists)
                if chunk:
                    output_strings.append((title, chunk))
                    chunk = ''
                    char_count = 0

                title = line.strip().strip('~')
                continue

            # Continue building up the chunk
            if len(chunk) + len(line) < 1024:
                chunk += line
            else:
                output_strings.append((title, chunk))
                title = title + ' [cont...]'
                chunk = line

        if chunk:
            output_strings.append((title, chunk))
            
        return output_strings



        
