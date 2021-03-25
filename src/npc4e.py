from typing import List

from .npc.buildNPC4 import BuildNPC4
from .npc.randomNPC4 import RandomNPC4

from .npc.careers4 import Careers4
from .npc.skills4 import Skills4
from .npc.talents4 import Talents4

from .npc import skill_talent

from .utility.convert_to_superscript import *

class NPC4e:
    """ Make either a fully defined NPC, or one randomly generated"""

    def __init__(self, 
                 random=False,
                 species=None,
                 careers=None,
                 young=False,
                 filter=None):
        """Create a new WFRP 4th edition NPC"""

        if random==False:
            self._npc = BuildNPC4(species=species)
            for career in careers or []:
                self._npc.add_career_rank(career[0], career[1])
        else:
            starting_career = None
            target_career = None
            if careers:
                careername = careers[0][0]
                level = careers[0][1]
                if level==1:
                    starting_career = careername
                else:
                    target_career = {'career': careername, 'rank':level}

            self._npc = RandomNPC4(species=species, starting_career=starting_career, target=target_career, young=young)

        self._filter = filter
        self._format()

        self._error = None

    @property
    def error_msg(self) -> str:
        """ Helpful (?!) error messages"""
        return self._error

    @classmethod
    def known_species(cls):
        return list(set(cls.known_species_build())+set(cls.known_species_random()))

    @classmethod
    def known_species_build(cls):
        """ Known species which can be used by the directed NPC builder """
        return BuildNPC4.known_species()

    @classmethod
    def known_species_random(cls) -> List[str]:
        """ Known species which can be used by the random NPC builder """
        return RandomNPC4.known_species()

    @classmethod
    def known_humans(cls) -> List[str]:
        """ Known types of human which can be used by the random NPC builder """
        return RandomNPC4.known_humans()

    @classmethod
    def known_careers(cls) -> List[str]:
        """ All known careers """
        return Careers4().careers

    @classmethod
    def known_career_levels(cls) -> List[str]:
        """ All known career levels. Note that some may be the same, e.g.  Nun and 
            Warrior Priest both start with Novitiate """
        return Careers4().career_levels

    @classmethod
    def known_filters(cls):
        """ Modes that the filters can use when presenting an NPC. Does not affect the 
            NPC actually built """
        return ['combat', 'social']

    @property
    def filter(self):
        """ The current presentation filter set on the NPC """
        return self._filter

    @filter.setter
    def filter(self, filter : str):
        """ Change the presentation of the NPC, simplifying it to show social or combat relevant stats """
        self._filter = filter
        self._format()

    def _format_talents(self, talents):
        return ', '.join('{}{}'.format(convert_to_superscript(v.get('skill_ref','')),k) for k,v in talents.items())

    def _format(self):
        type = self._filter

        # Skills
        skills_list = list()
        filtered_skills_dict = Skills4().filter(self._npc.skills_verbose,type)

        # Talents
        t4 = Talents4()
        if self._npc.starting_talents:
            starting_talents = t4.filter(self._npc.formatted_starting_talents,type)
        else: starting_talents = {}

        suggested_talents = t4.filter(self._npc.suggested_talents,type)
        additional_talents = t4.filter(self._npc.additional_talents,type)

        # Association between skills and talents
        filtered_skills_dict, starting_talents, index   = skill_talent.associate(filtered_skills_dict, starting_talents,   starting_index=1)
        filtered_skills_dict, suggested_talents, index  = skill_talent.associate(filtered_skills_dict, suggested_talents,  starting_index=index)
        filtered_skills_dict, additional_talents, index = skill_talent.associate(filtered_skills_dict, additional_talents, starting_index=index)

        # Format skills data
        for skill, values in filtered_skills_dict.items():
            for value in values:
                superscripts = sorted(list(value.get('talent_ref',{0})))
                if not superscripts[0]==0:
                    superscript = ' '.join(map(str, superscripts))
                    superscript = convert_to_superscript(f'({superscript})')
                else: superscript = ''

                if value['source'] and len(values)>1:
                    skills_list.append("{!s}: {!r}{} [{}; +{}]".format(skill,value['total'],superscript,value['source'],value['add']))
                else:
                    skills_list.append("{!s}: {!r}{}".format(skill,value['total'],superscript))
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
    def career_history_unambgious(self) -> str:
        """ The career history of the NPC with ambiguities resolved """
        return ' \u2192 '.join(self._npc.career_history_unambiguous)

    @property
    def characteristics(self) -> dict:
        """ The NPC's characteristics """
        return self._npc.characteristics

    @property
    def skills(self):
        return ', '.join(self.__skills_crossedref)

    @property
    def species(self):
        return self._npc.species

    @property
    def species_used(self):
        return self._npc.species_used

    @property
    def statblock(self):
        outstr  = "`| {} |`\n".format('| '.join([f'{x:>3}' for x in self._npc.characteristics.keys()]))
        outstr += "`| {} |`\n".format('| '.join([f'{x:3}' for x in self._npc.characteristics_base.values()]))
        outstr += "`| {} |`".format('| '.join([f'{x:3}' for x in self._npc.characteristics.values()]))

        return outstr

    @property
    def talents_initial(self):
        return self._format_talents(self.__talents_applied_crossedref)

    @property
    def talents_suggested(self):
        return self._format_talents(self.__talents_suggested_crossedref)

    @property
    def talents_additional(self):
        return self._format_talents(self.__talents_additional_crossedref)
    
    @property
    def traits(self):
        return ', '.join(self._npc.traits)

    @property
    def traits_optional(self):
        return ', '.join(self._npc.optional_traits)
    
    @property
    def trappings(self):
        return ', '.join(self._npc.trappings)

    @property
    def trappings_additional(self):
        return ', '.join(self._npc.additional_trappings)
    
    @property
    def xp_spend(self) -> int:
        """XP required to build this NPC. Note that this includes the cost of the suggested
           talents but does not include XP discounts from talents such as Artistic"""
        return self._npc.xp_spend