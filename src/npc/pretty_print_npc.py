from . import skill_talent
from .buildNPC4 import BuildNPC4
from .skills4 import Skills4
from .talents4 import Talents4
from ..utility.convert_to_superscript import convert_to_superscript

def pretty_print_npc(npc : BuildNPC4, type=None):
    """Pretty print an NPC"""

    # Skills
    skills_list = list()
    filtered_skills_dict = Skills4().filter(npc.skills_verbose,type)

    # Talents
    t4 = Talents4()
    if npc.starting_talents:
        starting_talents = t4.filter(npc.formatted_starting_talents,type)
    else: starting_talents = {}

    suggested_talents = t4.filter(npc.suggested_talents,type)
    additional_talents = t4.filter(npc.additional_talents,type)

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

    def format_talents(talents):
        return ', '.join('{}{}'.format(convert_to_superscript(v.get('skill_ref','')),k) for k,v in talents.items())

    print("{} ({}) {}".format(npc.species, npc.species_used.title(), npc.careername))
    print("**Career History**: {}".format(' \u2192 '.join(npc.career_history_unambiguous)))
    print("`| {} |`".format('| '.join([f'{x:>3}' for x in npc.characteristics.keys()])))
    print("`| {} |`".format('| '.join([f'{x:3}' for x in npc.characteristics_base.values()])))
    print("`| {} |`".format('| '.join([f'{x:3}' for x in npc.characteristics.values()])))
    print("**Skills**: {}".format(', '.join(skills_list)))
    if starting_talents: print(f"**Starting Talents**: {format_talents(starting_talents)}")
    print(f"**Suggested Talents**: {format_talents(suggested_talents)}")
    print(f"**Additional Talents**: {format_talents(additional_talents)}")
    print("**Traits**: {}".format(', '.join(npc.traits)))
    print("**Optional Traits**: {}".format(', '.join(npc.optional_traits)))
    print("**Trappings**: {}".format(', '.join(npc.trappings)))
    print("**Additional Trappings**: {}".format(', '.join(npc.additional_trappings)))
    print("**XP Spend**: {:,}".format(npc.xp_spend))