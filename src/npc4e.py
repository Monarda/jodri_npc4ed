from typing import List

from .npc.buildNPC4 import BuildNPC4
from .npc.randomNPC4 import RandomNPC4

from .npc.careers4 import Careers4
from .npc.skills4 import Skills4
from .npc.talents4 import Talents4

from .npc import skill_talent

from .utility.convert_to_superscript import *


class NPC4e:
    """ Make either a fully defined or randomly generated NPC"""

    def __init__(self,
                 random  : bool=True,
                 species : str=None,
                 careers : list=None,
                 type    : str=None,
                 age     : str=None,
                 filter  : str=None,
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

        if random == False:
            self._npc = BuildNPC4(species=species, 
                                  characteristics=characteristics, 
                                  starting_skills=initial_skills, 
                                  starting_talents=initial_talents,
                                  starting_trappings=initial_trappings)
            for career in careers or []:
                self._npc.add_career_rank(career[0].title(), career[1])
        else:
            starting_career = None
            target_career = None
            if careers:
                careername = careers[0][0]
                level = careers[0][1]
                if level == 1:
                    starting_career = careername
                else:
                    target_career = {'career': careername, 'rank': level}

            if age=='young' in age: young = True 
            else: young = False

            self._npc = RandomNPC4(species=species, 
                                   starting_career=starting_career, 
                                   target=target_career, 
                                   young=young, 
                                   characteristics=characteristics, 
                                   starting_skills=initial_skills, 
                                   starting_talents=initial_talents,
                                   starting_trappings=initial_trappings)

        self._filter = filter
        self._format()

        self._error = None

    @property
    def error_msg(self) -> str:
        """ Helpful (?!) error messages"""
        return self._error


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
        return ', '.join('{}{}'.format(convert_to_superscript(v.get('skill_ref', '')), k) for k, v in talents.items())

    def _format(self):
        """ Apply a filter to the NPC, allowing presentation to be simplified """
        type = self._filter

        # Skills
        skills_list = list()
        filtered_skills_dict = Skills4().filter(self._npc.skills_verbose, type)

        # Talents
        t4 = Talents4()
        if self._npc.starting_talents:
            starting_talents = t4.filter(
                self._npc.formatted_starting_talents, type)
        else:
            starting_talents = {}

        suggested_talents = t4.filter(self._npc.suggested_talents, type)
        additional_talents = t4.filter(self._npc.additional_talents, type)

        # Association between skills and talents
        filtered_skills_dict, starting_talents, index = skill_talent.associate(
            filtered_skills_dict, starting_talents,   starting_index=1)
        filtered_skills_dict, suggested_talents, index = skill_talent.associate(
            filtered_skills_dict, suggested_talents,  starting_index=index)
        filtered_skills_dict, additional_talents, index = skill_talent.associate(
            filtered_skills_dict, additional_talents, starting_index=index)

        # Format skills data
        for skill, values in filtered_skills_dict.items():
            for value in values:
                superscripts = sorted(list(value.get('talent_ref', {0})))
                if not superscripts[0] == 0:
                    superscript = ' '.join(map(str, superscripts))
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
        self.__talents_applied_crossedref = starting_talents
        self.__talents_suggested_crossedref = suggested_talents
        self.__talents_additional_crossedref = additional_talents

    ##################################################################################################
    # Output properties
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
        return self._npc.species_used

    @property
    def statblock(self) -> str:
        """ The formatted (as a grid) statblock of the NPC, showing starting characteristics
            which do include modifications like Savvy, and final characteristics """
        outstr = "`| {} |`\n".format(
            '| '.join([f'{x:>3}' for x in self._npc.characteristics.keys()]))
        outstr += "`| {} |`\n".format(
            '| '.join([f'{x:3}' for x in self._npc.characteristics_base.values()]))
        outstr += "`| {} |`".format(
            '| '.join([f'{x:3}' for x in self._npc.characteristics.values()]))

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
