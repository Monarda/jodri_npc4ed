from .src.npc4e import NPC4e

def print_npc(npc : NPC4e):
    print(f'{npc.species} ({npc.species_used}) {npc.careername}')
    print(f'{npc.career_history_unambgious}')
    print(npc.statblock)
    print(f'**Skills**: {npc.skills}')
    if npc.talents_initial: print(f'**Initial Talents: {npc.talents_initial}')
    print(f'**Suggested Talents: {npc.talents_suggested}')
    print(f'**Additional Talents: {npc.talents_additional}')
    print(f'**Traits**: {npc.traits}')
    if npc.traits_optional: print(f'**Optional Traits: {npc.traits_optional}')
    print(f'**Trappings**: {npc.trappings}')
    print(f'**Additional Trappings**: {npc.trappings_additional}')
    print(f'**XP Spend**: {npc.xp_spend}')

def main():
    npc = NPC4e(random=False, species='Ogre', careers=[('Guard',1), ('Guard',2), ('Pedlar',2)])
    print_npc(npc)

    npc = NPC4e(random=True, species='Reiklander', careers=[('Guard',1)])
    npc.filter = 'combat'
    print_npc(npc)

    for career_level in NPC4e.known_career_levels().items():
        if len(career_level[1])>1: print(career_level)
    print(NPC4e.known_species_build())
    print(NPC4e.known_species_random())

if __name__ == "__main__":
    # execute only if run as a script
    main()