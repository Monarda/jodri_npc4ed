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

        if random==False:
            self._npc = BuildNPC4(species=species)
            for career in careers or []:
                self._npc.add_career_rank(career[0], career[1])
        else:
            self._npc = RandomNPC4(species=species, starting_career=careers, young=young)

        self._filter = filter
        self._format()

        self._error = None

    @property
    def error(self):
        return self._error

    @property
    def known_species(self):
        self._npc.known_species

    @property
    def known_careers(self):
        return Careers4().careers

    @property
    def known_career_levels(self):
        return Careers4().career_levels

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter : str):
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
    def careername(self):
        return self._npc.careername

    @property
    def career_history_unambgious(self):
        return ' \u2192 '.join(self._npc.career_history_unambiguous)

    @property
    def characteristics(self):
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
    def trappings(self):
        return ', '.join(self._npc.trappings)

    @property
    def trappings_additional(self):
        return ', '.join(self._npc.additional_trappings)
    
    @property
    def xp_spend(self):
        return self._npc.xp_spend